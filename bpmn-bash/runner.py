#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from SpiffWorkflow.bpmn.workflow import BpmnWorkflow
from SpiffWorkflow.bpmn.specs.defaults import ServiceTask as BpmnServiceTask
from SpiffWorkflow.bpmn.parser.TaskParser import TaskParser
from SpiffWorkflow.camunda.parser.task_spec import CamundaTaskParser
from SpiffWorkflow.camunda.parser.CamundaParser import CamundaParser
from SpiffWorkflow.bpmn.script_engine.python_engine import PythonScriptEngine
from SpiffWorkflow.util.task import TaskState


BOOLEAN_TRUE = {"y", "yes", "true", "1"}
BOOLEAN_FALSE = {"n", "no", "false", "0"}
APPROVAL_CHOICES = {"approve", "reject"}
NUMBER_TYPES = {"long", "integer", "int", "number", "double", "float"}
STRING_TYPES = {"string", "text"}
BPMN_NS = {"bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL"}
CAMUNDA_NS_URI = "http://camunda.org/schema/1.0/bpmn"
CAMUNDA_NS = {"camunda": CAMUNDA_NS_URI}
SUPPORTED_EXPRESSION_LANGUAGES = {
    "python",
    "https://www.python.org/",
    "urn:python",
}
SUPPORTED_SERVICE_IMPLEMENTATIONS = {
    "##unspecified",
    "https://example.com/bpmn/shell-service",
}
DEFAULT_SERVICE_IMPLEMENTATION = "https://example.com/bpmn/shell-service"


@dataclass
class PromptField:
    field_id: str
    label: str
    field_type: str
    default_value: Any = None
    options: list[tuple[str, str]] | None = None


def get_camunda_attr(node: ET.Element, name: str) -> str | None:
    return node.get(f"{{{CAMUNDA_NS_URI}}}{name}")


def extract_camunda_properties(task: ET.Element) -> dict[str, str]:
    properties: dict[str, str] = {}
    for prop in task.findall(
        "./bpmn:extensionElements/camunda:properties/camunda:property",
        {**BPMN_NS, **CAMUNDA_NS},
    ):
        name = prop.get("name")
        value = prop.get("value")
        if name and value:
            properties[name] = value
    return properties


def normalize_camunda_expression(expression: str | None) -> str | None:
    if not expression:
        return None
    normalized = expression.strip()
    if (normalized.startswith("${") or normalized.startswith("#{")) and normalized.endswith("}"):
        normalized = normalized[2:-1].strip()
    if normalized.endswith("()"):
        normalized = normalized[:-2].strip()
    return normalized or None


def resolve_service_task_metadata(task: ET.Element) -> tuple[str | None, str | None]:
    implementation = task.get("implementation")
    operation_ref = task.get("operationRef")
    properties = extract_camunda_properties(task)
    camunda_type = get_camunda_attr(task, "type")

    if not implementation:
        implementation = properties.get("implementation")
    if implementation == "##WebService":
        implementation = None

    if not operation_ref:
        operation_ref = properties.get("operationRef") or properties.get("command") or properties.get("bashCommand")
    if not operation_ref:
        operation_ref = normalize_camunda_expression(get_camunda_attr(task, "expression"))
    if not operation_ref:
        operation_ref = normalize_camunda_expression(get_camunda_attr(task, "delegateExpression"))
    if not operation_ref and camunda_type == "external":
        operation_ref = get_camunda_attr(task, "topic")
    if not operation_ref:
        operation_ref = get_camunda_attr(task, "topic")

    if operation_ref and not implementation:
        implementation = DEFAULT_SERVICE_IMPLEMENTATION

    return implementation, operation_ref


def normalize_bpmn_for_runner(bpmn_file: Path) -> tuple[ET.ElementTree, bool]:
    tree = ET.parse(bpmn_file)
    root = tree.getroot()
    changed = False

    for task in root.findall(".//bpmn:serviceTask", BPMN_NS):
        implementation, operation_ref = resolve_service_task_metadata(task)
        if implementation and task.get("implementation") != implementation:
            task.set("implementation", implementation)
            changed = True
        if operation_ref and task.get("operationRef") != operation_ref:
            task.set("operationRef", operation_ref)
            changed = True

    for flow in root.findall(".//bpmn:sequenceFlow", BPMN_NS):
        expression = flow.find("bpmn:conditionExpression", BPMN_NS)
        if expression is None:
            continue
        language = expression.get("language")
        if language:
            continue
        expression.set("language", "python")
        changed = True

    return tree, changed


def validate_bpmn_execution_metadata(root: ET.Element) -> None:

    script_tasks = [task.get("id", "<unknown>") for task in root.findall(".//bpmn:scriptTask", BPMN_NS)]

    invalid_service_tasks = []
    for task in root.findall(".//bpmn:serviceTask", BPMN_NS):
        implementation, operation_ref = resolve_service_task_metadata(task)
        implementation = implementation or "##WebService"
        if implementation not in SUPPORTED_SERVICE_IMPLEMENTATIONS:
            invalid_service_tasks.append(
                (
                    task.get("id", "<unknown>"),
                    f"unsupported implementation {implementation}",
                )
            )
        elif not operation_ref:
            invalid_service_tasks.append((task.get("id", "<unknown>"), "missing operationRef"))

    missing_condition_languages = []
    invalid_condition_languages = []
    for flow in root.findall(".//bpmn:sequenceFlow", BPMN_NS):
        expression = flow.find("bpmn:conditionExpression", BPMN_NS)
        if expression is None:
            continue
        language = expression.get("language")
        if not language:
            missing_condition_languages.append(flow.get("id", "<unknown>"))
        elif language.strip().lower() not in SUPPORTED_EXPRESSION_LANGUAGES:
            invalid_condition_languages.append((flow.get("id", "<unknown>"), language))

    if script_tasks or invalid_service_tasks or missing_condition_languages or invalid_condition_languages:
        messages = []
        if script_tasks:
            details = ", ".join(script_tasks)
            messages.append(
                "Script tasks are not supported by this runner anymore. "
                f"Use bpmn:serviceTask with implementation and operationRef instead: {details}."
            )
        if invalid_service_tasks:
            supported_implementations = ", ".join(sorted(SUPPORTED_SERVICE_IMPLEMENTATIONS))
            details = ", ".join(f"{task_id} ({reason})" for task_id, reason in invalid_service_tasks)
            messages.append(
                f"Invalid serviceTask definitions: {details}. Supported implementation values: {supported_implementations}."
            )
        if missing_condition_languages:
            details = ", ".join(missing_condition_languages)
            messages.append(
                f"Missing conditionExpression language attributes on sequence flows: {details}. "
                "Declare the expression language explicitly."
            )
        if invalid_condition_languages:
            supported_languages = ", ".join(sorted(SUPPORTED_EXPRESSION_LANGUAGES))
            details = ", ".join(f"{flow_id}={language}" for flow_id, language in invalid_condition_languages)
            messages.append(
                f"Unsupported conditionExpression language values: {details}. Supported values: {supported_languages}."
            )
        raise ValueError(" ".join(messages))


class ShellServiceTask(BpmnServiceTask):
    def __init__(self, wf_spec, bpmn_id, operation_name: str, implementation: str, **kwargs):
        super().__init__(wf_spec, bpmn_id, **kwargs)
        self.operation_name = operation_name
        self.implementation = implementation

    def _execute(self, task):
        return task.workflow.script_engine.call_service(
            task,
            operation_name=self.operation_name,
            implementation=self.implementation,
        )


class ShellServiceTaskParser(CamundaTaskParser):
    def create_task(self):
        operation_name = self.node.get("operationRef")
        implementation = self.node.get("implementation", "##WebService")
        return ShellServiceTask(
            self.spec,
            self.bpmn_id,
            operation_name=operation_name,
            implementation=implementation,
            **self.bpmn_attributes,
        )


class RunnerCamundaParser(CamundaParser):
    OVERRIDE_PARSER_CLASSES = {
        **CamundaParser.OVERRIDE_PARSER_CLASSES,
        "{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask": (ShellServiceTaskParser, ShellServiceTask),
    }


class BashScriptEngine(PythonScriptEngine):
    def __init__(self, init_script: Path, custom_script: Path):
        super().__init__()
        self.init_script = init_script
        self.custom_script = custom_script

    def execute(self, task, script, external_context=None):
        return self._run_shell_command(task, script)

    def call_service(self, task, operation_name=None, implementation=None, **kwargs):
        if implementation not in SUPPORTED_SERVICE_IMPLEMENTATIONS:
            raise RuntimeError(
                f"Unsupported service implementation '{implementation}' for '{task.task_spec.name}'"
            )
        if not operation_name:
            raise RuntimeError(f"Missing operationRef for service task '{task.task_spec.name}'")
        return self._run_shell_command(task, operation_name)

    def _run_shell_command(self, task, command_body: str):
        payload = make_json_safe(dict(task.data))
        payload.setdefault("task_id", str(task.id))
        payload.setdefault("task_name", task.task_spec.name)

        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as output_file:
            output_path = Path(output_file.name)
            json.dump({}, output_file)

        env = os.environ.copy()
        env["WORKFLOW_DATA_JSON"] = json.dumps(payload)
        env["WORKFLOW_OUTPUT_PATH"] = str(output_path)
        env["TASK_ID"] = str(task.id)
        env["TASK_NAME"] = task.task_spec.name

        command = "\n".join(
            [
                "set -euo pipefail",
                f"source {self._quote(self.init_script)}",
                f"source {self._quote(self.custom_script)}",
                command_body,
            ]
        )

        completed = subprocess.run(
            ["bash", "-lc", command],
            capture_output=True,
            text=True,
            env=env,
        )

        if completed.stdout.strip():
            print(completed.stdout.rstrip())
        if completed.stderr.strip():
            print(completed.stderr.rstrip(), file=sys.stderr)

        try:
            updates = json.loads(output_path.read_text(encoding="utf-8"))
        finally:
            output_path.unlink(missing_ok=True)

        if completed.returncode != 0:
            raise RuntimeError(
                f"bash task failed for '{task.task_spec.name}' with exit code {completed.returncode}"
            )

        if updates:
            task.workflow.set_data(**updates)
            task.set_data(**updates)
        return updates

    @staticmethod
    def _quote(path: Path) -> str:
        return shlex.quote(str(path))


def make_json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): make_json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [make_json_safe(item) for item in value]
    return str(value)


class AnswerStore:
    def __init__(self, data: dict[str, Any] | None = None):
        self.data = data or {}

    @classmethod
    def from_path(cls, path: Path | None):
        if path is None:
            return cls()
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def resolve(self, task_names: list[str], field: PromptField) -> Any | None:
        for task_name in task_names:
            task_value = self.data.get(task_name)
            if isinstance(task_value, dict) and field.field_id in task_value:
                return task_value[field.field_id]
        if field.field_id in self.data:
            return self.data[field.field_id]
        return None


def get_task_label(task) -> str:
    return getattr(task.task_spec, "bpmn_name", None) or task.task_spec.name


def get_task_keys(task) -> list[str]:
    keys = [get_task_label(task), task.task_spec.name]
    return list(dict.fromkeys(key for key in keys if key))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run BPMN files with SpiffWorkflow and bash-backed task handlers.")
    parser.add_argument("bpmn_file", type=Path, help="Path to the BPMN file.")
    parser.add_argument("--process-id", help="Explicit BPMN process id. Defaults to the first process in the file.")
    parser.add_argument("--init", type=Path, default=Path("init.sh"), help="Path to the init shell file.")
    parser.add_argument("--custom", type=Path, default=Path("custom.sh"), help="Path to the custom shell file.")
    parser.add_argument("--answers", type=Path, help="Optional JSON file with predefined user-task answers.")
    parser.add_argument(
        "--dump-data",
        action="store_true",
        help="Print final workflow data as JSON when the workflow completes.",
    )
    return parser.parse_args()


def build_workflow(bpmn_file: Path, process_id: str | None, engine: BashScriptEngine) -> BpmnWorkflow:
    normalized_tree, changed = normalize_bpmn_for_runner(bpmn_file)
    validate_bpmn_execution_metadata(normalized_tree.getroot())

    parser = RunnerCamundaParser()
    if changed:
        with tempfile.NamedTemporaryFile("w", suffix=".bpmn", delete=False, encoding="utf-8") as normalized_file:
            normalized_tree.write(normalized_file, encoding="unicode", xml_declaration=True)
            normalized_path = Path(normalized_file.name)
        try:
            parser.add_bpmn_file(str(normalized_path))
        finally:
            normalized_path.unlink(missing_ok=True)
    else:
        parser.add_bpmn_file(str(bpmn_file))

    selected_process = process_id or parser.get_process_ids()[0]
    spec = parser.get_spec(selected_process)
    subprocess_specs = parser.get_subprocess_specs(selected_process)
    return BpmnWorkflow(spec, subprocess_specs=subprocess_specs, script_engine=engine)


def get_ready_manual_tasks(workflow: BpmnWorkflow) -> list[Any]:
    return [task for task in workflow.get_tasks(state=TaskState.READY) if task.task_spec.manual]


def build_prompt_fields(task) -> list[PromptField]:
    form = getattr(task.task_spec, "form", None)
    if form is not None and getattr(form, "fields", None):
        fields = []
        for field in form.fields:
            options = None
            if hasattr(field, "options"):
                options = [(option.id, option.name) for option in field.options]
            fields.append(
                PromptField(
                    field_id=field.id,
                    label=field.label or field.id,
                    field_type=(field.type or "string").lower(),
                    default_value=field.default_value,
                    options=options,
                )
            )
        return fields

    extensions = getattr(task.task_spec, "extensions", {}) or {}
    if "result_var" in extensions:
        field_type = extensions.get("prompt_type", "string").lower()
        options = None
        if field_type == "approval":
            options = [("approve", "Approve"), ("reject", "Reject")]
            field_type = "enum"
        elif field_type == "yesno":
            options = [("y", "Yes"), ("n", "No")]
            field_type = "enum"
        return [
            PromptField(
                field_id=extensions["result_var"],
                label=extensions.get("prompt_label", task.task_spec.name),
                field_type=field_type,
                default_value=extensions.get("default_value"),
                options=options,
            )
        ]

    return []


def prompt_for_value(task, field: PromptField, answers: AnswerStore) -> Any:
    supplied = answers.resolve(get_task_keys(task), field)
    if supplied is not None:
        value = coerce_value(supplied, field)
        print(f"[auto] {field.label}: {value}")
        return value

    while True:
        prompt = build_prompt_text(field)
        raw = input(prompt).strip()
        if not raw and field.default_value not in (None, ""):
            raw = str(field.default_value)
        try:
            return coerce_value(raw, field)
        except ValueError as exc:
            print(exc, file=sys.stderr)


def build_prompt_text(field: PromptField) -> str:
    suffix = ""
    if field.options:
        readable_options = "/".join(option_id for option_id, _ in field.options)
        suffix = f" [{readable_options}]"
    elif field.field_type in NUMBER_TYPES:
        suffix = " [number]"
    elif field.field_type == "boolean":
        suffix = " [y/n]"

    default_text = ""
    if field.default_value not in (None, ""):
        default_text = f" (default: {field.default_value})"
    return f"{field.label}{suffix}{default_text}: "


def coerce_value(raw: Any, field: PromptField) -> Any:
    if isinstance(raw, (int, float, bool)):
        return normalize_typed_value(raw, field)

    text = str(raw).strip()
    field_type = field.field_type

    if field.options:
        valid_options = {option_id for option_id, _ in field.options}
        lowered = text.lower()
        if field.field_id == "approval" or valid_options == APPROVAL_CHOICES:
            if lowered in APPROVAL_CHOICES:
                return lowered
            raise ValueError("Enter 'approve' or 'reject'.")
        if valid_options in ({"y", "n"}, {"yes", "no"}):
            if lowered in BOOLEAN_TRUE:
                return "y" if "y" in valid_options else "yes"
            if lowered in BOOLEAN_FALSE:
                return "n" if "n" in valid_options else "no"
            raise ValueError("Enter 'y' or 'n'.")
        if text in valid_options:
            return text
        if lowered in valid_options:
            return lowered
        raise ValueError(f"Choose one of: {', '.join(sorted(valid_options))}.")

    if field_type == "boolean":
        lowered = text.lower()
        if lowered in BOOLEAN_TRUE:
            return True
        if lowered in BOOLEAN_FALSE:
            return False
        raise ValueError("Enter y/n, yes/no, true/false, or 1/0.")

    if field_type in NUMBER_TYPES:
        if field_type in {"double", "float"}:
            return float(text)
        return int(text)

    if field_type in STRING_TYPES or field_type == "enum":
        if text == "":
            raise ValueError("A value is required.")
        return text

    if text == "":
        raise ValueError("A value is required.")
    return text


def normalize_typed_value(value: Any, field: PromptField) -> Any:
    if field.field_type == "boolean":
        return bool(value)
    if field.field_type in {"double", "float"}:
        return float(value)
    if field.field_type in NUMBER_TYPES:
        return int(value)
    return value


def handle_user_task(task, answers: AnswerStore) -> None:
    print(f"\nUser task: {get_task_label(task)}")
    fields = build_prompt_fields(task)
    updates = {}

    if not fields:
        print("No form fields were defined for this user task. Press Enter to complete it.")
        input("continue: ")
    else:
        for field in fields:
            updates[field.field_id] = prompt_for_value(task, field, answers)

    if updates:
        task.workflow.set_data(**updates)
        task.set_data(**updates)
    task.complete()


def handle_manual_task(task) -> None:
    print(f"\nManual task: {get_task_label(task)}")
    input("Press Enter to continue: ")
    task.complete()


def run_workflow(workflow: BpmnWorkflow, answers: AnswerStore) -> None:
    while not workflow.is_completed():
        workflow.do_engine_steps()
        manual_tasks = get_ready_manual_tasks(workflow)
        if not manual_tasks:
            waiting_tasks = workflow.get_tasks(state=TaskState.WAITING)
            if waiting_tasks:
                raise RuntimeError("Workflow is waiting for an external event; this runner only handles tasks and user input.")
            ready_tasks = workflow.get_tasks(state=TaskState.READY)
            if ready_tasks:
                names = ", ".join(task.task_spec.name for task in ready_tasks)
                raise RuntimeError(f"Workflow is blocked on unsupported ready tasks: {names}")
            break

        for task in manual_tasks:
            if getattr(task.task_spec, "form", None) is not None or getattr(task.task_spec, "extensions", None):
                handle_user_task(task, answers)
            else:
                handle_manual_task(task)

    workflow.do_engine_steps()


def main() -> int:
    args = parse_args()
    engine = BashScriptEngine(args.init.resolve(), args.custom.resolve())
    answers = AnswerStore.from_path(args.answers.resolve() if args.answers else None)
    workflow = build_workflow(args.bpmn_file.resolve(), args.process_id, engine)

    run_workflow(workflow, answers)

    print("\nWorkflow completed.")
    if args.dump_data:
        print(json.dumps(workflow.data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
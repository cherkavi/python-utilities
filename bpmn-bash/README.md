# SpiffWorkflow BPMN runner with bash handlers

This workspace contains a small universal runner for BPMN files using `SpiffWorkflow`.

It supports:

- Camunda Modeler BPMN exports, including service tasks configured visually and executed through bash after sourcing `init.sh` and `custom.sh`
- manual tasks completed interactively
- user tasks with these answer styles:
  - `y/n`
  - `approve/reject`
  - free text string
  - numeric input

## External tools
### [Camunda modeler](https://camunda.com/download/modeler/)
```sh
sudo chown root:root /home/soft/camunda/camunda-modeler-5.48.0-linux-x64/chrome-sandbox
sudo chmod 4755 /home/soft/camunda/camunda-modeler-5.48.0-linux-x64/chrome-sandbox
```

## Files

- `runner.py`: BPMN CLI runner
- `init.sh`: shared bash helpers used by workflow service tasks
- `custom.sh`: your custom bash functions
- `examples/approval_flow.bpmn`: sample BPMN process
- `examples/answers.json`: non-interactive answers for the sample BPMN

## Install

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## Run the sample

### Interactive:

```bash
. .venv/bin/activate
python3 runner.py examples/approval_flow.bpmn --dump-data
```

### Non-interactive with predefined answers:

```bash
. .venv/bin/activate
python3 runner.py examples/approval_flow.bpmn --answers examples/answers.json --dump-data
```

## Bash task contract

Every BPMN service task is executed as bash code after these files are sourced:

```bash
source init.sh
source custom.sh
```

The runner provides these environment variables:

- `WORKFLOW_DATA_JSON`: current workflow data as JSON
- `WORKFLOW_OUTPUT_PATH`: temporary JSON file where bash functions can write updates
- `TASK_ID`: current workflow task id
- `TASK_NAME`: current workflow task name

Use these helpers from `init.sh`:

- `wf_get key`: read a workflow variable
- `wf_set key value [string|number|boolean|json]`: write a workflow variable update
- `wf_log ...`: print a log line

Example custom function:

```bash
my_task() {
  local amount
  amount="$(wf_get final_amount)"
  wf_log "Current amount is ${amount}"
  wf_set request_status processed
}
```

Camunda Modeler exports can stay unedited. The runner normalizes these service-task shapes automatically:

- `camunda:type="expression"` with `camunda:expression="${my_task}"` or `camunda:expression="${my_task()}"`
- `camunda:delegateExpression="${my_task}"` or `camunda:delegateExpression="${my_task()}"`
- `camunda:type="external"` with `camunda:topic="my_task"`
- `camunda:properties` under `bpmn:extensionElements` with `implementation`, `operationRef`, `command`, or `bashCommand`

These all resolve to the bash function name that will be executed. The normalized internal contract still uses the shell service implementation and an `operationRef`.

Example raw Camunda export:

```xml
<bpmn:serviceTask
  id="ServiceTask_Example"
  name="Example"
  camunda:type="expression"
  camunda:expression="${my_task}" />
```

Equivalent normalized form inside the runner:

```xml
<bpmn:serviceTask
  id="ServiceTask_Example"
  name="Example"
  implementation="https://example.com/bpmn/shell-service"
  operationRef="my_task" />
```

For gateway condition expressions, Camunda exports without a `language` attribute are treated as Python. This runner still only supports Python expressions:

```xml
<bpmn:conditionExpression xsi:type="bpmn:tFormalExpression"><![CDATA[
approval == 'approve'
]]></bpmn:conditionExpression>
```

This runner still rejects BPMN script tasks. Use service tasks for bash-backed automation.

## User-task conventions

Preferred approach: use Camunda form fields in BPMN.

- `type="boolean"` gives `y/n`
- `type="enum"` with values `approve/reject` gives approval prompts
- `type="string"` gives free text input
- `type="long"`, `integer`, `double`, `number` give numeric prompts

If you do not want to use form fields, a user task may define extension properties:

- `result_var`
- `prompt_type` with `yesno`, `approval`, `string`, or `number`
- `prompt_label`
- `default_value`

## Adapting to your BPMN

1. Put shared helpers in `init.sh`.
2. Put business-specific bash functions in `custom.sh`.
3. Reference those functions in Camunda Modeler service tasks using an expression or external topic.
4. Add Camunda form fields to user tasks for typed user input.
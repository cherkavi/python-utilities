import tempfile
import subprocess
import shutil
import os
from string import Template

DEFAULT_ENCODING = "utf-8"


def __clear_binary_line__(b_line):
    next_line = b_line.decode(DEFAULT_ENCODING)
    if next_line[len(next_line)-1] == "\n":
        next_line = next_line[:-1]
    return next_line.strip()


def execute_find_response(arguments, pattern):
    process = subprocess.Popen(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = False
    for b_line in process.stderr:
        if result:
            continue
        line = __clear_binary_line__(b_line)
        # print(">>> %s" % (line) )
        if line.find(pattern) >= 0:
            result = True
    process.stdout.close()
    return result


def execute_response_to_file(arguments, output_file, current_user, new_user=None, ):
    process = subprocess.Popen(arguments, stdout=subprocess.PIPE)

    if new_user is not None:
        replaced_user_name = current_user.strip().upper() + "."
        new_user_name = new_user.strip().upper()+"."
    else:
        new_user_name = None

    with open(output_file, "w") as output:
        for b_line in process.stdout:
            output_line = __clear_binary_line__(b_line)
            if output_line == 'SET DEFINE OFF;':
                if new_user_name is not None:
                    output.write('alter session set current_schema = ' + new_user_name.strip().upper()[:-1])
                else:
                    output.write('alter session set current_schema = ' + replaced_user_name.strip().upper())
                output.write("\n")
            if new_user_name is not None:
                output.write(output_line.replace(replaced_user_name, new_user_name))
            else:
                output.write(output_line)
            output.write("\n")
    process.stdout.close()


def update_template(path_to_sql_template, user, path_to_output):
    with open(path_to_sql_template, "r") as source, open(path_to_output, "w") as destination:
        for each_line in source:
            destination.write(Template(each_line).substitute(db_create_user=user, session="$session"))
    return path_to_output


def execute_sqlplus_find_string(user, path_to_sql_template, string_to_find, temp_file_controller):
    """ execute script with dropping all connections, remove user and create it again  """
    sql_script = update_template(path_to_sql_template, user, temp_file_controller.create_temp_file())
    sqlplus_connection = "user/password@hostname:1521/stx11de"
    # return execute_and_waiting_for_string(["sqlplus", '-S', sqlplus_connection, "@"+sql_script], "Grant succeeded.")
    process = subprocess.Popen(["sqlplus", sqlplus_connection], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    with open(sql_script, "r") as source:
        for each_line in source:
            process.stdin.write(each_line.encode("utf-8"))
        process.stdin.close()
    result = process.communicate()[0]
    return __clear_binary_line__(result).find(string_to_find) > 0


def print_file(path):
    with open(path, "r") as output:
        for line in output:
            print(line, end="")


class TempFileController:
    files = list()
    folders = list()

    def create_temp_file(self):
        return_value = tempfile.TemporaryFile().name
        self.files.append(return_value)
        return return_value

    def create_temp_folder(self):
        return_value = tempfile.mkdtemp()
        self.folders.append(return_value)
        return return_value

    def delete_all_created_files(self):
        for each_file in self.files:
            try:
                os.remove(each_file)
            except FileNotFoundError:
                pass
        self.files.clear()

    def delete_all_created_folders(self):
        for each_folder in self.folders:
            try:
                shutil.rmtree(each_folder)
            except FileNotFoundError:
                pass
        self.folders.clear()

    def clear(self):
        self.delete_all_created_files()
        self.delete_all_created_folders()

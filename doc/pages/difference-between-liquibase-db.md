# difference-between-liquibase-db

## db diff

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/difference-between-liquibase-db/db-diff.py) -->
<!-- The below code snippet is automatically added from ../../python/difference-between-liquibase-db/db-diff.py -->
```py
import jirawrapper
import filesystemutils
import downloadutils
import tempfile
import cherkavi

import os
import shutil
import argparse


def main(version_1, version_2, jdbc_user, path_sql_create_user, override_user, need_to_create_jira = False):
    temp_file_controller = filesystemutils.TempFileController()
    print("downloading war file ")
    unzip_folder_ver_1 = downloadutils.download_and_extract_war_file(version_1, temp_file_controller)
    db_script_path_master = os.path.join(unzip_folder_ver_1, *("db\changelog\master.xml".split("\\")))
    print("Liquibase db-script enter point: %s for version: %s " % (db_script_path_master, version_1))

    # execute update script against DB
    if filesystemutils.execute_sqlplus_find_string(jdbc_user, path_sql_create_user, "Grant succeeded.", temp_file_controller):
        print("user was re-created")
    else:
        print("can't create/re-create user into DB")
        exit(2)

    print("downloading liquibase jar file ")
    liquibase_jar = downloadutils.download_file(
        "http://central.maven.org/maven2/org/liquibase/liquibase-core/3.5.3/liquibase-core-3.5.3.jar",
        tempfile.TemporaryFile().name)
    print("downloading oracle jdbc jar file ")
    oracle_jdbc_jar = downloadutils.download_file("http://hostname:8081/nexus/service/local/repositories/thirdparty/content/com/oracle/ojdbc6/11.2.0.4/ojdbc6-11.2.0.4.jar", tempfile.TemporaryFile().name)

    update_db_arguments = ["java", "-jar", liquibase_jar,
                           "--driver=oracle.jdbc.OracleDriver",
                           "--classpath=%s" % (oracle_jdbc_jar),
                           "--changeLogFile=%s" % (db_script_path_master),
                           "--url=jdbc:oracle:thin:@hostname:1521/stx11de",
                           "--username=%s" % (jdbc_user),  "--password=%s" % (jdbc_user),
                           "--contexts=\"default\"",
                           "update"]
    print("update Database with version: " + version_1)
    if filesystemutils.execute_find_response(update_db_arguments, "Liquibase Update Successful"):
        print("db with user: %s contains version %s" % (jdbc_user, version_1))
    else:
        print("can't update database using Liquibase script into folder: " + db_script_path_master)
        exit(2)

    shutil.rmtree(unzip_folder_ver_1)
    print("downloading war file ")
    unzip_folder_ver_2 = downloadutils.download_and_extract_war_file(version_2, temp_file_controller, unzip_folder_ver_1)
    db_script_path_master_2 = os.path.join(unzip_folder_ver_2, *("db\changelog\master.xml".split("\\")))
    print("Liquibase db-script enter point: %s for version: %s " % (db_script_path_master_2, version_2))

    update_db_arguments = ["java", "-jar", liquibase_jar,
                           "--driver=oracle.jdbc.OracleDriver", "--classpath=%s" % (oracle_jdbc_jar), "--changeLogFile=%s" % (db_script_path_master_2),
                           "--url=jdbc:oracle:thin:@hostname:1521/stx11de",
                           "--username=%s" % (jdbc_user), "--password=%s" % (jdbc_user),
                           "--contexts=\"default\"",
                           "updateSQL"]
    print("===diff between version: %s and version %s: ===" % (version_1, version_2))
    output_file = temp_file_controller.create_temp_file()
    filesystemutils.execute_response_to_file(update_db_arguments, output_file, jdbc_user, override_user)
    filesystemutils.print_file(output_file)

    if need_to_create_jira:
        jira_ticket = jirawrapper.JiraWrapper("username", cherkavi.linux_password)\
            .create_release_request(summary="app release request",
                                    description="please prepare DB using script.ini file",
                                    sql_script=output_file)
        print("JIRA ticket have been created: " + jira_ticket)
    temp_file_controller.clear()


if __name__ == "__main__":
    # input parameters
    parser = argparse.ArgumentParser(description='SQL difference between two versions of app ')
    parser.add_argument('--version1',
                        help='version of first RPM/WAR package',
                        required=True)
    parser.add_argument('--version2',
                        help='version of second RPM/WAR package',
                        required=True)
    parser.add_argument('--recreate_db_user',
                        help='user of DB to use for create DB according version 1 ( v1 argument ) of RPM/WAR ',
                        required=True)
    parser.add_argument('--destination_user',
                        help='user of DB where script should be applied ',
                        required=False, default="default_app")
    parser.add_argument('--create_user_sql',
                        help='path to file with sql file ( drop connections, drop user, create user, add permissions )',
                        required=True)
    args = parser.parse_args()

    main(args.version1, args.version2, args.recreate_db_user, args.create_user_sql, args.destination_user, True)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## downloadutils

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/difference-between-liquibase-db/downloadutils.py) -->
<!-- The below code snippet is automatically added from ../../python/difference-between-liquibase-db/downloadutils.py -->
```py
import requests
import zipwrapper
import os


def download_file(url, local_filename):
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


def unpack_archive_for_another_archive(path_to_archive, temp_file_controller, entry_name, destination_path=None):
    db_script_jar_path = temp_file_controller.create_temp_file()

    try:
        archive = zipwrapper.ZipWrapper(path_to_archive)
        migration_job_jar_db_script = archive.get_entry(entry_name)
        db_script_jar = zipwrapper.ZipWrapper(
            archive.copy_entry_to_file(migration_job_jar_db_script, db_script_jar_path))
    finally:
        archive.close()

    if not('db_script_jar' in locals()):
        exit(1)

    if destination_path is None:
        destination_path = temp_file_controller.create_temp_folder()
    db_script_jar.extract(destination_path)
    db_script_jar.close()
    os.remove(db_script_jar_path)
    return destination_path


def build_artifact_url(rpm_version):
    version = rpm_version.strip()
    return "http://hostname:8081/nexus/content/repositories/releases/com/brand/brand-server-standalone/%s/brand-server-standalone-%s.war" % (version, version)


def download_and_extract_war_file(rpm_version, temp_file_controller, destination_path=None):
    temp_file_path = temp_file_controller.create_temp_file()
    download_file(build_artifact_url(rpm_version), temp_file_path)
    # print("new war file: " + temp_file_path)
    return unpack_archive_for_another_archive(temp_file_path, temp_file_controller, "brand-db-scripts", destination_path)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## filesystemutils

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/difference-between-liquibase-db/filesystemutils.py) -->
<!-- The below code snippet is automatically added from ../../python/difference-between-liquibase-db/filesystemutils.py -->
```py
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
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## jirawrapper

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/difference-between-liquibase-db/jirawrapper.py) -->
<!-- The below code snippet is automatically added from ../../python/difference-between-liquibase-db/jirawrapper.py -->
```py
from jira import JIRA
import os
import tempfile
import zipfile


class JiraWrapper:

    def __init__(self, user_name, user_password):
        self.user_name = user_name
        self.user_password = user_password
        pass

    def create_release_request(self, summary, description, sql_script):
        options = dict()
        jac = JIRA('https://jira.sys', basic_auth=(self.user_name, self.user_password),
                   max_retries=1, options={"verify": False, "check_update": True})
        fields = dict()
        fields["project"] = "BCM"
        fields["summary"] = summary
        fields["description"] = description
        fields["issuetype"] = {'name': 'Release Request'}
        fields["fixVersions"] = [{'name': '5.0.x'}, ]
        result = jac.create_issue(fields)

        self.attach_file_as_ini(jac, result, sql_script)
        # result.fields
        return result.permalink()

    @staticmethod
    def attach_file_as_ini(jac, ticket, sql_script):
        path_to_ini = JiraWrapper.make_ini_file(zip_file_name="script.zip", sql_script_name="script.sql")
        jac.add_attachment(ticket, path_to_ini, "script.ini")

        path_to_zip = JiraWrapper.make_zip_file(path_to_content=sql_script, filename="script.sql")
        jac.add_attachment(ticket, path_to_zip, "script.zip")

        os.remove(path_to_ini)
        os.remove(path_to_zip)

    @staticmethod
    def make_ini_file(zip_file_name, sql_script_name):
        path = tempfile.TemporaryFile().name
        with open(path, "w") as output:
            output.write("[source_code_repository]\n")
            output.write("get_db_scripts_cmd        =    get_jira_attachment %s \n" % (zip_file_name))
            output.write("\n")
            output.write("[db_release]\n")
            output.write("db_script_home_dir        =    .\n")
            output.write("db_sql_script_01          =    %s\n" % (sql_script_name))
        return path

    @staticmethod
    def make_zip_file(path_to_content, filename):
        path = tempfile.TemporaryFile().name
        zf = zipfile.ZipFile(path, mode='w')
        try:
            zf.write(path_to_content, filename)
        finally:
            zf.close()
        return path
```
<!-- MARKDOWN-AUTO-DOCS:END -->



## zipwrapper

<!-- MARKDOWN-AUTO-DOCS:START (CODE:src=../../python/difference-between-liquibase-db/zipwrapper.py) -->
<!-- The below code snippet is automatically added from ../../python/difference-between-liquibase-db/zipwrapper.py -->
```py
import zipfile
import os
import tempfile
import shutil


class ZipWrapper:

    def __init__(self, path_to_file):
        self.zip_reference = zipfile.ZipFile(path_to_file, 'r')
        self.file_list = [each_entry.filename for each_entry in self.zip_reference.infolist()]

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, "zip_reference"):
            self.zip_reference.close()

    @staticmethod
    def __check_candidate__(filename, entry_name):
        if filename.find(entry_name) >= 0:
            return filename
        else:
            return None

    def get_entry(self, entry_name):
        for each_entry in self.file_list:
            candidate = self.__check_candidate__(each_entry, entry_name)
            if candidate is not None:
                return candidate
        return None

    def get_entries(self, entry_name):
        return_value = list()
        for each_entry in self.file_list:
            candidate = self.__check_candidate__(each_entry, entry_name)
            if candidate is not None:
                return_value.append(candidate)
        return return_value

    def copy_entry_to_file(self, entry_name, destination_file):
        """ :return full path to created file """
        try:
            temp_folder = tempfile.mkdtemp()
            path_to_created_file = self.zip_reference.extract(entry_name, temp_folder)
            try:
                os.remove(destination_file)
            except FileNotFoundError:
                pass
            os.rename(path_to_created_file, destination_file)
            return destination_file
        finally:
            if 'temp_folder' in locals():
                shutil.rmtree(temp_folder, True)

    def extract(self, folder):
        self.zip_reference.extractall(folder)

    def copy_entries_to_folder(self, entries, destination_folder):
        """ :return full path to created folder !!! NOT WORKING !!! """
        try:
            temp_folder = tempfile.mkdtemp()
            for each_entry in entries:
                try:
                    path_to_created_file = self.zip_reference.extract(each_entry, temp_folder)
                except KeyError:
                    continue
                path = [each for each in each_entry.split("/") if each != '']
                print(path)
                destination_file = os.path.join(destination_folder, *path)
                try:
                    os.remove(destination_file)
                except FileNotFoundError:
                    pass
                if os.path.isdir(path_to_created_file):
                    continue
                os.rename(path_to_created_file, destination_file)
            return destination_folder
        finally:
            if 'temp_folder' in locals():
                shutil.rmtree(temp_folder, True)
```
<!-- MARKDOWN-AUTO-DOCS:END -->



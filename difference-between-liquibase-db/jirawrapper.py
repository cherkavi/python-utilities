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

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
            .create_release_request(summary="BrandServer release request",
                                    description="please prepare DB using script.ini file",
                                    sql_script=output_file)
        print("JIRA ticket have been created: " + jira_ticket)
    temp_file_controller.clear()


if __name__ == "__main__":
    # input parameters
    parser = argparse.ArgumentParser(description='SQL difference between two versions of BrandServer ')
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
                        required=False, default="brand_server_data")
    parser.add_argument('--create_user_sql',
                        help='path to file with sql file ( drop connections, drop user, create user, add permissions )',
                        required=True)
    args = parser.parse_args()

    main(args.version1, args.version2, args.recreate_db_user, args.create_user_sql, args.destination_user, True)

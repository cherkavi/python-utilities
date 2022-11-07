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



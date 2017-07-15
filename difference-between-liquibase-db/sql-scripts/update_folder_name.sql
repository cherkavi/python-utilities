DECLARE
  folder_name VARCHAR2(100);
BEGIN
  select substr(dcl.FILENAME, 0, instr(dcl.FILENAME, '/db/changelog/')-1) into folder_name from DATABASECHANGELOG dcl where rownum=1;
  update DATABASECHANGELOG dcl set dcl.filename =
  replace(dcl.filename,
          folder_name,
          '${folder_name}'
           );
END;
/
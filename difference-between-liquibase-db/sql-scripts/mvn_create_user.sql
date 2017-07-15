-- kill all connections
SET SERVEROUTPUT ON;
declare
  str varchar2(100);
begin
   for S in (select sid,serial#,inst_id from gv$session where username is not null
       and username = upper('${db_create_user}'))
   loop
       str := 'alter system kill session '||chr(39)||S.sid||','||S.serial#||','|| '@' || S.inst_id||chr(39)||' IMMEDIATE';
       execute immediate str;
   end loop;
end;
/
-- Drop user (might result in an error, which is ignored by the plugin)
BEGIN
   EXECUTE IMMEDIATE 'DROP user ${db_create_user} cascade';
EXCEPTION
   WHEN OTHERS THEN
   null;
END;
/
-- Create user
create user ${db_create_user} identified by ${db_create_user};
grant all privileges to ${db_create_user};

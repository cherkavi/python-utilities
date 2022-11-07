import sys

for each_line in sys.stdin:
    e = each_line.split(";")
    # escape sql escape
    city_name=e[1].replace("'", "''").replace('\\', '\\\\')
    print(f"insert into hlm_zip_code(zip, city, state_code, country_code, latitude, longitude, timezone, daylight_saving) values "\
    f"('{e[0]}', '{city_name}', '{e[2]}', 'US', {e[3]}, {e[4]}, {e[5]}, {e[6]});")

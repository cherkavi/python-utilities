def parse_bool_value(str_value: str) -> Optional[bool]:
    if str_value.strip().lower() in ["true", "ok", "yes"]:
        return True
    if str_value.strip().lower() in ["false", "ko", "no"]:
        return False
    return None


os.environ["DISPLAY"] = ":2"

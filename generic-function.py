T = TypeVar('T')
def get_value_or_else(parse_result: ParseResult, argument_name: str, default_value: T) -> T:
    return parse_result[argument_name] if argument_name in parse_result and parse_result[argument_name] else default_value


import re


def get_parser_by_name(parser_name):
    if parser_name == 'parse_int':
        return parse_int
    elif parser_name == 'parse_int_in_scale':
        return parse_int_in_scale
    elif parser_name == 'parse_yes_or_no':
        return parse_yes_or_no
    
    raise RuntimeError(f'No such parser: {parser_name}')


def parse_int(s):
    if not s or not isinstance(s, str):
        return None
    
    number_str = ''
    for char in s:
        if char.isdigit() or (char == '-' and not number_str):
            number_str += char
        elif number_str and not char.isdigit():
            break
    
    if number_str and number_str != '-':
        try:
            return int(number_str)
        except ValueError:
            return None
    
    return None


def parse_int_in_scale(s, scale_min=None, scale_max=None):
    number = parse_int(s)
    
    if number is None:
        return None
    
    if scale_min is not None and number < scale_min:
        return None
        
    if scale_max is not None and number > scale_max:
        return None
        
    return number


def parse_yes_or_no(s, default=None):
    if not s or not isinstance(s, str):
        return default
    
    s_lower = s.strip().lower()
    
    yes_patterns = {
        'yes', 'y', 'true', 't', '1', '+',
        'ok', 'okay', 'affirmative', 'agree',
        'correct', 'right', 'confirmed',
        'positive', 'sure', 'absolutely',
        'certainly', 'definitely', 'yep',
        'yeah', 'yup', 'aye', 'roger',
        'approved', 'accept', 'allowed'
    }
    
    no_patterns = {
        'no', 'n', 'false', 'f', '0', '-',
        'cancel', 'deny', 'refuse', 'reject',
        'disagree', 'incorrect', 'wrong',
        'negative', 'never', 'nope',
        'nah', 'negative', 'veto',
        'forbidden', 'prohibited', 'banned',
        'rejected', 'declined', 'disallowed'
    }
    
    if s_lower in yes_patterns:
        return 'yes'
    elif s_lower in no_patterns:
        return 'no'
    
    for pattern in yes_patterns:
        if s_lower.startswith(pattern) and len(pattern) > 1:
            next_char = s_lower[len(pattern):len(pattern)+1] if len(s_lower) > len(pattern) else ''
            if not next_char or not next_char.isalpha():
                return 'yes'
    
    for pattern in no_patterns:
        if s_lower.startswith(pattern) and len(pattern) > 1:
            next_char = s_lower[len(pattern):len(pattern)+1] if len(s_lower) > len(pattern) else ''
            if not next_char or not next_char.isalpha():
                return 'no'
    
    return default

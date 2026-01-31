import re


_REGEX_ONLY_NUMBERS_DOT_COMMA = re.compile(r'[^\d\.\,]+')
_REGEX_DATE = re.compile(r'(\d{1,2})\sde\s(\w{3})\sde\s(\d{4})')

def extract_int_from_text(text: str) -> int:
    numbers = re.findall(r'\d+', text.replace('.', ''))
    if numbers:
        return int(''.join(numbers))
    return 0


def text_to_float(textual_number: str) -> float | None:
    parts = textual_number.strip().split(' ')
    number_str = _REGEX_ONLY_NUMBERS_DOT_COMMA.sub('', parts[0]).replace(',', '.')
    sufix = parts[-1] if len(parts) > 1 else ''

    try:
        number = float(number_str)
    except ValueError:
        return None

    if 'mil' in sufix:
        number = number * 1_000
    elif 'mi' in sufix:
        number = number * 1_000_000
    elif 'bi' in sufix:
        number = number * 1_000_000_000
    
    return number


def text_to_date(textual_date: str) -> str:
    months = {
        'jan': '01', 'fev': '02', 'mar': '03', 'abr': '04',
        'mai': '05', 'jun': '06', 'jul': '07', 'ago': '08',
        'set': '09', 'out': '10', 'nov': '11', 'dez': '12'
    }
    match = _REGEX_DATE.search(textual_date)
    if match:
        day = match.group(1).zfill(2)
        month = months.get(match.group(2).lower(), '01')
        year = match.group(3)
        return f'{year}-{month}-{day}'
    return ''

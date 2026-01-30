import re


def extract_int_from_text(text: str) -> int:
    numbers = re.findall(r'\d+', text.replace('.', ''))
    if numbers:
        return int(''.join(numbers))
    return 0

import re


def extract_identificacao_biblioteca(text: str) -> str:
    pattern = r'Identificação\sda\sbiblioteca:\s(\d+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''

def extract_periodo_veiculacao(text: str) -> str:
    pattern = r'\d{1,2}\s\w+\s\w+\s\w+\s\d{4}'
    match = re.findall(pattern, text)
    if match:
        return match
    return []

def extract_tamanho_estimado_publico(text: str) -> str:
    pattern = r'Tamanho\sestimado\sdo\spúblico:\s(.*)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''

def extract_valor_gasto(text: str) -> str:
    pattern = r'Valor\sgasto\s\(BRL\):\n(.*)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''

def extract_impressoes(text: str) -> str:
    pattern = r'Impressões:\n([^\n]+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''

def extract_pago_por(text: str) -> str:
    pattern = r'Pago\spor\s(.*)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''

def extract_texto_anuncio(text: str) -> str:
    pattern = r'Pago\spor\s.*\n([\s\S]*)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''
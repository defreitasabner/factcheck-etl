import logging
import re

from src.utils.text_helpers import text_to_float, text_to_date
from src.transform.constants import MetaAdFields


REGEX_ID_BIBLIOTECA = r'Identificação\sda\sbiblioteca:\s(\d+)'
REGEX_PERIODO_VEICULACAO = r'\d{1,2}\s\w+\s\w+\s\w+\s\d{4}(\sa\s\d{1,2}\s\w+\s\w+\s\w+\s\d{4})?'
REGEX_TAMANHO_PUBLICO = r'Tamanho\sestimado\sdo\spúblico:\s(.*)'
REGEX_VALOR_GASTO = r'Valor\sgasto\s\(BRL\):\n(.*)'
REGEX_IMPRESSOES = r'Impressões:\n([^\n]+)'
REGEX_PAGO_POR = r'Pago\spor\s(.*)'
REGEX_TEXTO_ANUNCIO = r'Pago\spor\s.*\n([\s\S]*)'


logger = logging.getLogger(__name__)


def find_identificacao_biblioteca(text: str) -> str:
    pattern = REGEX_ID_BIBLIOTECA
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''


def find_periodo_veiculacao(text: str) -> str:
    pattern = REGEX_PERIODO_VEICULACAO
    match = re.search(pattern, text)
    if match:
        return match.group(0).strip()
    return ''


def find_tamanho_estimado_publico(text: str) -> str:
    pattern = REGEX_TAMANHO_PUBLICO
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''


def find_valor_gasto(text: str) -> str:
    pattern = REGEX_VALOR_GASTO
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''


def find_impressoes(text: str) -> str:
    pattern = REGEX_IMPRESSOES
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''


def find_pago_por(text: str) -> str:
    pattern = REGEX_PAGO_POR
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''


def find_texto_anuncio(text: str) -> str:
    pattern = REGEX_TEXTO_ANUNCIO
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return ''

def transform_valor_gasto(valor_gasto_str: str) -> float | None:
    valor_gasto_str = valor_gasto_str.replace('R$', '')
    if 'a' in valor_gasto_str:
        parts = valor_gasto_str.split('a')
        min_val = text_to_float(parts[0])
        max_val = text_to_float(parts[1])
        return (min_val + max_val) / 2
    else:
        return text_to_float(valor_gasto_str)


def transform_periodo_veiculacao(periodo_str: str) -> tuple[str, str | None]:
    dates = periodo_str.split(' a ')
    if len(dates) == 2:
        start_date = text_to_date(dates[0])
        end_date = text_to_date(dates[1])
        return (start_date, end_date)
    else:
        start_date = text_to_date(dates[0])
        return (start_date, None)


def transform_tamanho_estimado_publico(tamanho_publico_str: str) -> float | None:
        tamanho_publico = tamanho_publico_str.split(' a ')
        if len(tamanho_publico) == 2:
            min_val = text_to_float(tamanho_publico[0])
            max_val = text_to_float(tamanho_publico[1])
            return (min_val + max_val) / 2
        else:
            return text_to_float(tamanho_publico[0])


def transform_impressoes(impressoes_str: str) -> float | None:
        impressoes = impressoes_str.split(' a ')
        if len(impressoes) == 2:
            min_val = text_to_float(impressoes[0])
            max_val = text_to_float(impressoes[1])
            return (min_val + max_val) / 2
        else:
            return text_to_float(impressoes[0])


def transform(meta_ads_bronze_tier_data: list[dict]) -> tuple[list[dict], dict]:
    logger.info('Starting transformation of Meta ads data')
    logger.info(f'Number of records to transform: {len(meta_ads_bronze_tier_data)}')
    transformed_data = []
    for data in meta_ads_bronze_tier_data:
        raw_ad_str = data.get('raw_text', '')
        id_biblioteca = find_identificacao_biblioteca(raw_ad_str)
        periodo_str = find_periodo_veiculacao(raw_ad_str)
        tamanho_publico = find_tamanho_estimado_publico(raw_ad_str)
        valor_gasto_str = find_valor_gasto(raw_ad_str)
        impressoes = find_impressoes(raw_ad_str)
        pago_por = find_pago_por(raw_ad_str)
        texto = find_texto_anuncio(raw_ad_str)
        
        valor_gasto_medio = transform_valor_gasto(valor_gasto_str)
        periodo_veiculacao = transform_periodo_veiculacao(periodo_str)
        tamanho_publico = transform_tamanho_estimado_publico(tamanho_publico)
        impressoes = transform_impressoes(impressoes)

        if id_biblioteca and texto:
            transformed_data.append({
                MetaAdFields.ID: id_biblioteca,
                MetaAdFields.PERIODO_INICIO: periodo_veiculacao[0],
                MetaAdFields.PERIODO_FIM: periodo_veiculacao[1],
                MetaAdFields.TAMANHO_PUBLICO: tamanho_publico,
                MetaAdFields.VALOR_GASTO: valor_gasto_medio,
                MetaAdFields.IMPRESSOES: impressoes,
                MetaAdFields.PAGO_POR: pago_por,
                MetaAdFields.TEXTO: texto
            })
        else:
            logger.warning(f'Skipping ad due to missing ID or text.')
    transform_params = {
        'fields': MetaAdFields.fields(),
        'regex_patterns': {
            'identificacao_biblioteca': REGEX_ID_BIBLIOTECA,
            'periodo_veiculacao': REGEX_PERIODO_VEICULACAO,
            'tamanho_estimado_publico': REGEX_TAMANHO_PUBLICO,
            'valor_gasto': REGEX_VALOR_GASTO,
            'impressoes': REGEX_IMPRESSOES,
            'pago_por': REGEX_PAGO_POR,
            'texto_anuncio': REGEX_TEXTO_ANUNCIO
        }
    }
    logger.info(f'Transformation completed successfully. Total transformed records: {len(transformed_data)}')
    return transformed_data, transform_params

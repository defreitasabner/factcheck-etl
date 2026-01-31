from src.transform.meta_ads import *
from src.transform.constants import MetaAdFields


def test_find_identificacao_biblioteca(sample_ad_text, another_sample_ad_text):
    """Test extraction of library identification number."""
    result = find_identificacao_biblioteca(sample_ad_text)
    assert result == '743756688282936'

    result = find_identificacao_biblioteca(another_sample_ad_text)
    assert result == '680016768176090'


def test_find_periodo_veiculacao(sample_ad_text, another_sample_ad_text):
    """Test extraction of ad circulation period."""
    result = find_periodo_veiculacao(sample_ad_text)
    assert len(result) > 0
    assert result == '10 de ago de 2025'

    result = find_periodo_veiculacao(another_sample_ad_text)
    assert len(result) > 0
    assert result == '2 de jun de 2025 a 26 de jan de 2026'


def test_find_tamanho_estimado_publico(sample_ad_text, another_sample_ad_text):
    """Test extraction of estimated audience size."""
    result = find_tamanho_estimado_publico(sample_ad_text)
    assert result == '>1 mi'

    result = find_tamanho_estimado_publico(another_sample_ad_text)
    assert result == '>1 mi'


def test_find_valor_gasto(sample_ad_text, another_sample_ad_text):
    """Test extraction of amount spent."""
    result = find_valor_gasto(sample_ad_text)
    assert result == 'R$25 mil a R$30 mil'

    result = find_valor_gasto(another_sample_ad_text)
    assert result == 'R$2 mil a R$2,5 mil'


def test_find_impressoes(sample_ad_text, another_sample_ad_text):
    """Test extraction of impressions."""
    result = find_impressoes(sample_ad_text)
    assert result == '>1 mi'

    result = find_impressoes(another_sample_ad_text)
    assert result == '>1 mi'


def test_find_pago_por(sample_ad_text, another_sample_ad_text):
    """Test extraction of who paid for the ad."""
    result = find_pago_por(sample_ad_text)
    assert result == 'Roberto Cláudio Bezerra'

    result = find_pago_por(another_sample_ad_text)
    assert result == 'Plínio Valério'


def test_find_texto_anuncio(sample_ad_text, another_sample_ad_text):
    """Test extraction of ad text content."""
    result = find_texto_anuncio(sample_ad_text)
    assert '🔴 A violência tem nome e sobrenome' in result
    assert 'O Ceará não precisa de desculpas. Precisa de ação!' in result

    result = find_texto_anuncio(another_sample_ad_text)
    assert 'É o dinheiro do povo voltando para o povo!' in result
    assert '#PlínioValério #Amazonas #SaúdeÉPrioridade #DinheiroPúblico #TrabalhoDeVerdade' in result


def test_find_identificacao_biblioteca_empty():
    """Test extraction with empty text."""
    result = find_identificacao_biblioteca('')
    assert result == ''


def test_find_periodo_veiculacao_empty():
    """Test extraction with empty text."""
    result = find_periodo_veiculacao('')
    assert result == ''


def test_find_tamanho_estimado_publico_empty():
    """Test extraction with empty text."""
    result = find_tamanho_estimado_publico('')
    assert result == ''


def test_find_valor_gasto_empty():
    """Test extraction with empty text."""
    result = find_valor_gasto('')
    assert result == ''


def test_find_impressoes_empty():
    """Test extraction with empty text."""
    result = find_impressoes('')
    assert result == ''


def test_find_pago_por_empty():
    """Test extraction with empty text."""
    result = find_pago_por('')
    assert result == ''


def test_find_texto_anuncio_empty():
    """Test extraction with empty text."""
    result = find_texto_anuncio('')
    assert result == ''


def test_transform_valor_gasto():
    """Test transformation of spent amount string to float."""
    result = transform_valor_gasto('R$25 mil a R$30 mil')
    assert result == 27500.0

    result = transform_valor_gasto('R$2 mil a R$2,5 mil')
    assert result == 2250.0

    result = transform_valor_gasto('R$1000')
    assert result == 1000.0


def test_transform_periodo_veiculacao():
    """Test transformation of circulation period string to start and end dates."""
    start_date, end_date = transform_periodo_veiculacao('10 de ago de 2025 a 15 de set de 2025')
    assert start_date == '2025-08-10'
    assert end_date == '2025-09-15'

    start_date, end_date = transform_periodo_veiculacao('2 de jun de 2025')
    assert start_date == '2025-06-02'
    assert end_date == None


def test_transform(sample_ad_text, another_sample_ad_text):
    """Test full transformation of ad text."""
    meta_ads_bronze_tier_data = [{'raw_text': sample_ad_text}, {'raw_text': another_sample_ad_text}]
    transformed_data, _ = transform(meta_ads_bronze_tier_data)
    assert transformed_data[0][MetaAdFields.ID] == '743756688282936'
    assert transformed_data[0][MetaAdFields.PERIODO_INICIO] == '2025-08-10'
    assert transformed_data[0][MetaAdFields.PERIODO_FIM] == None
    assert transformed_data[0][MetaAdFields.TAMANHO_PUBLICO] == '>1 mi'
    assert transformed_data[0][MetaAdFields.VALOR_GASTO] == 27500.0
    assert transformed_data[0][MetaAdFields.IMPRESSOES] == '>1 mi'
    assert transformed_data[0][MetaAdFields.PAGO_POR] == 'Roberto Cláudio Bezerra'
    assert '🔴 A violência tem nome e sobrenome' in transformed_data[0][MetaAdFields.TEXTO]

    assert transformed_data[1][MetaAdFields.ID] == '680016768176090'
    assert transformed_data[1][MetaAdFields.PERIODO_INICIO] == '2025-06-02'
    assert transformed_data[1][MetaAdFields.PERIODO_FIM] == '2026-01-26'
    assert transformed_data[1][MetaAdFields.TAMANHO_PUBLICO] == '>1 mi'
    assert transformed_data[1][MetaAdFields.VALOR_GASTO] == 2250.0
    assert transformed_data[1][MetaAdFields.IMPRESSOES] == '>1 mi'
    assert transformed_data[1][MetaAdFields.PAGO_POR] == 'Plínio Valério'
    assert 'É o dinheiro do povo voltando para o povo!' in transformed_data[1][MetaAdFields.TEXTO]

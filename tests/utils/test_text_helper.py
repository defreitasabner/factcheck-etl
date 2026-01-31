from src.utils.text_helpers import text_to_float, text_to_date


def test_text_to_float():
    assert text_to_float('25 mil ') == 25_000.0
    assert text_to_float('1,5 mi ') == 1_500_000.0
    assert text_to_float('2 bi') == 2_000_000_000.0
    assert text_to_float('3000') == 3_000.0
    assert text_to_float('>1 mi') == 1_000_000.0
    assert text_to_float('100') == 100
    assert text_to_float('invalid') is None


def test_text_to_date():
    assert text_to_date('10 de ago de 2025') == '2025-08-10'
    assert text_to_date('1 de jan de 2020') == '2020-01-01'
    assert text_to_date('15 de dez de 1999') == '1999-12-15'

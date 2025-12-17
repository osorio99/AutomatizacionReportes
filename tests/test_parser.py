from normaliza_csv.parser import parse_fecha


def test_parse_fecha_basic():
    assert parse_fecha('12/29/2024 11:54:01 PM') is not None
    assert parse_fecha('29/12/2024') is not None
    assert parse_fecha('2024-12-29 23:54:01') is not None
    assert parse_fecha('') is None
    assert parse_fecha(None) is None


def test_parse_spanish_month():
    assert parse_fecha('25 Dic 2024') is not None
    assert parse_fecha('25 dic 2024') is not None

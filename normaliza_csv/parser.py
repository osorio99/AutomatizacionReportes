from datetime import datetime
from typing import Optional
from .config import FORMATOS_CANDIDATOS

MESES_ES = {
    'ene': 'Jan', 'feb': 'Feb', 'mar': 'Mar', 'abr': 'Apr', 'may': 'May', 'jun': 'Jun',
    'jul': 'Jul', 'ago': 'Aug', 'sep': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'dic': 'Dec'
}


def normaliza_mes_es(texto: str) -> str:
    """Reemplaza meses en español por abreviatura inglesa para facilitar parseos con %b."""
    if not isinstance(texto, str):
        return texto
    t = f" {texto} "
    for es, en in MESES_ES.items():
        t = t.replace(f" {es} ", f" {en} ")
        t = t.replace(f" {es.capitalize()} ", f" {en} ")
    return t.strip()


def parse_fecha(texto: str) -> Optional[datetime]:
    """Intenta convertir un string a datetime probando múltiples formatos.

    Devuelve datetime o None si no pudo parsear.
    """
    if texto is None:
        return None
    t = str(texto).strip()
    if not t:
        return None

    # Normaliza separadores y meses en español
    t = t.replace('-', '/')
    t = normaliza_mes_es(t)

    # Intentos directos con lista de formatos
    for fmt in FORMATOS_CANDIDATOS:
        try:
            return datetime.strptime(t, fmt)
        except Exception:
            continue

    # Intento flexible: si trae AM/PM y separador '/', usar %m/%d/%Y heurístico
    try:
        parts = t.split()
        if len(parts) >= 2 and (parts[-1].upper().endswith('AM') or parts[-1].upper().endswith('PM') or 'AM' in parts[-1] or 'PM' in parts[-1]):
            for fmt in ("%m/%d/%Y %I:%M:%S %p", "%m/%d/%Y %I:%M %p"):
                try:
                    return datetime.strptime(t, fmt)
                except Exception:
                    pass
    except Exception:
        pass

    # Último recurso: intentos con fromisoformat (solo soporta 24h y formato ISO)
    try:
        return datetime.fromisoformat(t.replace('/', '-'))
    except Exception:
        return None

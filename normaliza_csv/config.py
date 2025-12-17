from typing import Set

# Configuración de salida
SALIDA_CON_HORA = True  # True: conserva hora si existe; False: siempre solo fecha
FORMATO_FECHA = "%d/%m/%Y"
FORMATO_FECHA_HORA = "%d/%m/%Y %H:%M:%S"

# Columnas objetivo (exactamente como aparecen en el encabezado del CSV)
COLUMNAS_FECHA_OBJETIVO: Set[str] = {
    "Created Date",
    "Activated Date",
    "Closed Date",
    "Changed Date",
    "State Change Date",
}

# Formatos que intentaremos parsear
FORMATOS_CANDIDATOS = [
    "%m/%d/%Y %I:%M:%S %p",
    "%m/%d/%Y %I:%M %p",
    "%m/%d/%Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d",
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y",
    "%d-%m-%Y %H:%M:%S",
    "%d-%m-%Y",
    "%d %b %Y %H:%M:%S",
    "%d %b %Y",
]


# -*- coding: utf-8 -*-
"""
Script: normaliza_fechas_csv_forzado.py
Autor: M365 Copilot

Descripción:
  - Procesa todos los .csv de una carpeta (o un archivo .csv).
  - Fuerza normalización en columnas específicas: 
    ["Created Date", "Activated Date", "Closed Date", "Changed Date", "State Change Date"].
  - Acepta formatos comunes: 'mm/dd/yyyy hh:mm:ss AM/PM', 'mm/dd/yyyy', 'yyyy-mm-dd hh:mm:ss', etc.
  - Guarda la salida en 'salida/' con el mismo nombre del archivo.
  - No requiere pandas (usa csv + datetime).

Salida por defecto:
  - Si la celda tiene fecha y hora -> 'dd/mm/yyyy HH:MM:SS' (24h)
  - Si solo tiene fecha -> 'dd/mm/yyyy'

Para dejar solo fecha siempre, cambia SALIDA_CON_HORA = False.

Uso:
  py normaliza_fechas_csv_forzado.py --entrada "C:/ruta/carpeta" [--delimitador ";" ] [--salida "C:/ruta/salida"] [--verbose]
"""

import os
import csv
import argparse
from datetime import datetime

# Configuración de salida
SALIDA_CON_HORA = True  # True: conserva hora si existe; False: siempre solo fecha
FORMATO_FECHA = "%d/%m/%Y"
FORMATO_FECHA_HORA = "%d/%m/%Y %H:%M:%S"

# Columnas objetivo (exactamente como aparecen en el encabezado del CSV)
COLUMNAS_FECHA_OBJETIVO = {
    "Created Date",
    "Activated Date",
    "Closed Date",
    "Changed Date",
    "State Change Date",
}

# Formatos que intentaremos parsear
FORMATOS_CANDIDATOS = [
    # US con AM/PM (lo más probable según tu captura)
    "%m/%d/%Y %I:%M:%S %p",
    "%m/%d/%Y %I:%M %p",
    "%m/%d/%Y",

    # ISO y variantes
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d",

    # Otros formatos comunes
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y",
    "%d-%m-%Y %H:%M:%S",
    "%d-%m-%Y",
]

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

def parse_fecha(texto: str):
    """Intenta convertir un string a datetime probando múltiples formatos."""
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
    # Ej: 12/29/2024 11:54:01 PM
    try:
        parts = t.split()
        if len(parts) >= 2 and ('AM' in parts[-1] or 'PM' in parts[-1]):
            # Hora en 12h; intentemos sin segundos también
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

def detecta_delimitador(path_csv, preferido=None):
    """Auto-detecta el delimitador entre ',' y ';' (si no se especifica)."""
    if preferido in (',', ';'):
        return preferido
    try:
        with open(path_csv, 'r', encoding='utf-8') as f:
            muestra = f.read(4096)
    except UnicodeDecodeError:
        with open(path_csv, 'r', encoding='latin-1') as f:
            muestra = f.read(4096)
    comas = muestra.count(',')
    puntosycoma = muestra.count(';')
    return ';' if puntosycoma > comas else ','

def lee_csv(path_csv, delimitador, verbose=False):
    """Lee CSV tolerando UTF-8 y latin-1."""
    filas = []
    try:
        with open(path_csv, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f, delimiter=delimitador)
            for fila in reader:
                filas.append(fila)
    except UnicodeDecodeError:
        with open(path_csv, 'r', encoding='latin-1', newline='') as f:
            reader = csv.reader(f, delimiter=delimitador)
            for fila in reader:
                filas.append(fila)
    except Exception as e:
        print(f"[ERROR] No se pudo leer '{path_csv}': {e}")
        return None
    if verbose:
        print(f"[INFO] Leídas {len(filas)} filas con delimitador '{delimitador}'")
    return filas

def procesa_csv(path_csv, out_dir, delimitador_opt, verbose=False):
    if verbose:
        print(f"[INFO] Procesando: {path_csv}")
    delim = detecta_delimitador(path_csv, preferido=delimitador_opt)
    if verbose:
        print(f"[INFO] Delimitador usado: '{delim}'")

    filas = lee_csv(path_csv, delimitador=delim, verbose=verbose)
    if not filas:
        print(f"[WARN] Archivo vacío o delimitador incorrecto: {path_csv}")
        return

    encabezados = filas[0]
    data = filas[1:]
    if verbose:
        print(f"[INFO] Encabezados ({len(encabezados)}): {encabezados}")
        print(f"[INFO] Filas de datos: {len(data)}")

    # Mapa: nombre -> índice
    nombre_a_indice = {h: i for i, h in enumerate(encabezados)}

    # Columnas objetivo presentes en el archivo
    cols_objetivo = [nombre_a_indice[h] for h in COLUMNAS_FECHA_OBJETIVO if h in nombre_a_indice]
    if verbose:
        print(f"[INFO] Columnas objetivo presentes: {[(encabezados[i], i) for i in cols_objetivo]}")

    if not cols_objetivo:
        print(f"[INFO] No se encontraron columnas objetivo en '{os.path.basename(path_csv)}'. Se guarda igual.")
    else:
        # Normalizar celdas en esas columnas
        convertidas = {i: 0 for i in cols_objetivo}
        for fila in data:
            for col_idx in cols_objetivo:
                if col_idx < len(fila):
                    dt = parse_fecha(fila[col_idx])
                    if dt:
                        fila[col_idx] = dt.strftime(FORMATO_FECHA_HORA if SALIDA_CON_HORA else FORMATO_FECHA)
                        convertidas[col_idx] += 1
        if verbose:
            for col_idx in cols_objetivo:
                print(f"[INFO] '{encabezados[col_idx]}': {convertidas[col_idx]} celdas convertidas.")

    # Guardar salida SIEMPRE
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, os.path.basename(path_csv))
    try:
        with open(out_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=delim)
            writer.writerow(encabezados)
            writer.writerows(data)
        print(f"[OK] Guardado: {out_path}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar '{out_path}': {e}")

from normaliza_csv.cli import main

if __name__ == '__main__':
    # Backwards-compatible wrapper to the new package
    main()
    
#py "C:/Nueva carpeta/normaliza_fechas_csv_forzado.py" --entrada "C:/Nueva carpeta/ADM_CAPACIDADEXTERNA" --delimitador "," --verbose
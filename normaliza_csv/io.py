import os
import csv
from pathlib import Path
from typing import List, Optional
from .config import COLUMNAS_FECHA_OBJETIVO, FORMATO_FECHA, FORMATO_FECHA_HORA, SALIDA_CON_HORA
from .parser import parse_fecha


def detecta_delimitador(path_csv: str, preferido: Optional[str] = None) -> str:
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


def lee_csv(path_csv: str, delimitador: str) -> Optional[List[List[str]]]:
    """Lee CSV tolerando UTF-8 y latin-1 y devuelve filas como listas."""
    filas: List[List[str]] = []
    try:
        with open(path_csv, 'r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f, delimiter=delimitador)
            filas = [row for row in reader]
    except UnicodeDecodeError:
        with open(path_csv, 'r', encoding='latin-1', newline='') as f:
            reader = csv.reader(f, delimiter=delimitador)
            filas = [row for row in reader]
    except Exception as e:
        print(f"[ERROR] No se pudo leer '{path_csv}': {e}")
        return None
    return filas


def escribe_csv(path_csv: str, filas: List[List[str]], delimitador: str) -> bool:
    """Escribe filas a CSV con encoding UTF-8."""
    try:
        with open(path_csv, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=delimitador)
            for row in filas:
                writer.writerow(row)
        return True
    except Exception as e:
        print(f"[ERROR] No se pudo guardar '{path_csv}': {e}")
        return False


def procesa_csv(path_csv: str, out_dir: str, delimitador_opt: Optional[str] = None, verbose: bool = False) -> None:
    """Normaliza las columnas objetivo del CSV y guarda la copia en out_dir."""
    if verbose:
        print(f"[INFO] Procesando: {path_csv}")
    delim = detecta_delimitador(path_csv, preferido=delimitador_opt)
    if verbose:
        print(f"[INFO] Delimitador usado: '{delim}'")

    filas = lee_csv(path_csv, delimitador=delim)
    if not filas:
        print(f"[WARN] Archivo vacío o delimitador incorrecto: {path_csv}")
        return

    encabezados = filas[0]
    data = filas[1:]
    nombre_a_indice = {h: i for i, h in enumerate(encabezados)}
    cols_objetivo = [nombre_a_indice[h] for h in COLUMNAS_FECHA_OBJETIVO if h in nombre_a_indice]

    if verbose:
        print(f"[INFO] Encabezados ({len(encabezados)}): {encabezados}")
        print(f"[INFO] Filas de datos: {len(data)}")
        print(f"[INFO] Columnas objetivo presentes: {[(encabezados[i], i) for i in cols_objetivo]}")

    if cols_objetivo:
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
    else:
        print(f"[INFO] No se encontraron columnas objetivo en '{os.path.basename(path_csv)}'. Se guarda igual.")

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, os.path.basename(path_csv))
    if escribe_csv(out_path, [encabezados] + data, delimitador=delim):
        print(f"[OK] Guardado: {out_path}")

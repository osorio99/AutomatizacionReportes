import os
import argparse
from pathlib import Path
from .io import procesa_csv


def main(argv=None):
    parser = argparse.ArgumentParser(description="Normaliza fechas en CSV a 'dd/mm/yyyy' (opcional hora 24h).")
    parser.add_argument('--entrada', required=True, help="Ruta a carpeta con .csv o a un archivo .csv")
    parser.add_argument('--salida', default='salida', help="Carpeta de salida (por defecto 'salida')")
    parser.add_argument('--delimitador', default=None, help="Delimitador preferido: ',' o ';' (si no se indica, se auto-detecta)")
    parser.add_argument('--verbose', action='store_true', help="Muestra detalles del proceso")
    args = parser.parse_args(argv)

    ruta = args.entrada.replace('\\', '/')
    if os.path.isdir(ruta):
        archivos = [os.path.join(ruta, f) for f in os.listdir(ruta) if f.lower().endswith('.csv')]
        print(f"[INFO] Carpeta detectada: {ruta}")
        print(f"[INFO] .csv encontrados: {len(archivos)}")
        if not archivos:
            print("[WARN] No se encontraron archivos .csv en la carpeta indicada.")
            return
        for a in archivos:
            procesa_csv(a, out_dir=args.salida, delimitador_opt=args.delimitador, verbose=args.verbose)
    else:
        if not ruta.lower().endswith('.csv'):
            print("[ERROR] La ruta indicada no es una carpeta ni un archivo .csv. Use una carpeta o un .csv.")
            return
        procesa_csv(ruta, out_dir=args.salida, delimitador_opt=args.delimitador, verbose=args.verbose)


if __name__ == '__main__':
    main()

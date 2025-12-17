# normaliza_csv ✅

Herramienta ligera para normalizar campos de fecha en archivos CSV (sin pandas).

## 🔧 Qué hace

- Detecta y normaliza columnas de fecha (por defecto: `Created Date`, `Activated Date`, `Closed Date`, `Changed Date`, `State Change Date`).
- Acepta múltiples formatos (MM/DD/YYYY con AM/PM, ISO, dd/mm/yyyy, meses en español, etc.).
- Auto-detecta delimitador (`,` o `;`) y codificación (UTF-8 / latin-1).
- Guarda la salida en la carpeta `salida/` por defecto manteniendo el nombre original.

---

## ▶️ Uso (ejemplos)

Procesar una carpeta con todos los CSV:

```powershell
py "C:/Nueva carpeta/normaliza_fechas_csv_forzado.py" --entrada "C:/Nueva carpeta/ADM_CAPACIDADEXTERNA" --delimitador "," --verbose
```

Procesar un archivo CSV individual:

```powershell
py "C:/Nueva carpeta/normaliza_fechas_csv_forzado.py" --entrada "C:/ruta/mi_archivo.csv" --verbose
```

Usar el paquete directamente (p. ej. desde Python):

```py
python -m normaliza_csv.cli --entrada "C:/ruta" --salida "salida" --verbose
```

---

## ⚙️ Configuración

- Formato de salida y columnas objetivo están definidos en `normaliza_csv/config.py`.
- Cambia `SALIDA_CON_HORA` a `False` si quieres siempre `dd/mm/YYYY` sin hora.
- Añade formatos de parseo en `FORMATOS_CANDIDATOS` si tienes un formato extra.

---

## 🧪 Tests

Hay pruebas básicas en `tests/test_parser.py` (requiere `pytest` para ejecutarlas):

```bash
py -m pip install pytest
py -m pytest -q
```

---

## 💡 Notas

- Algunos CSV pueden no convertir celdas si el formato no se reconoce; puedes enviar ejemplos para que añada heurísticas.
- Mantengo compatibilidad con el script `normaliza_fechas_csv_forzado.py` como wrapper sencillo.

---

## Contribuciones

Pull requests y issues bienvenidos. Si añades formatos o mejoras, agrega pruebas que cubran los casos nuevos.

---

License: MIT (por defecto) — edítala según necesites.

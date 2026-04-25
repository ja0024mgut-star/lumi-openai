"""
leer_datos.py - Lumi
Lee datos desde Google Sheets y genera datos_colegio.py
Ejecutar: python leer_datos.py
"""
import urllib.request
import csv
import io

# ── Links de Google Sheets ────────────────────────────────────
SHEETS = {
    "Estudiantes":  "https://docs.google.com/spreadsheets/d/e/2PACX-1vRlv5wwLwxItimnvbc2cRZmyvMCR9pd2JNERaQXKmB7m33qgQsVJ3mf3KrNufieUkfhsv9s-BK6BN-A/pub?gid=0&single=true&output=csv",
    "Horarios":     "https://docs.google.com/spreadsheets/d/e/2PACX-1vRlv5wwLwxItimnvbc2cRZmyvMCR9pd2JNERaQXKmB7m33qgQsVJ3mf3KrNufieUkfhsv9s-BK6BN-A/pub?gid=694022457&single=true&output=csv",
    "Tareas":       "https://docs.google.com/spreadsheets/d/e/2PACX-1vRlv5wwLwxItimnvbc2cRZmyvMCR9pd2JNERaQXKmB7m33qgQsVJ3mf3KrNufieUkfhsv9s-BK6BN-A/pub?gid=248742090&single=true&output=csv",
    "Profesores":   "https://docs.google.com/spreadsheets/d/e/2PACX-1vRlv5wwLwxItimnvbc2cRZmyvMCR9pd2JNERaQXKmB7m33qgQsVJ3mf3KrNufieUkfhsv9s-BK6BN-A/pub?gid=1604430808&single=true&output=csv",
    "Asistencias":  "https://docs.google.com/spreadsheets/d/e/2PACX-1vRlv5wwLwxItimnvbc2cRZmyvMCR9pd2JNERaQXKmB7m33qgQsVJ3mf3KrNufieUkfhsv9s-BK6BN-A/pub?gid=195400202&single=true&output=csv",
    "Analytics":    "https://docs.google.com/spreadsheets/d/e/2PACX-1vRlv5wwLwxItimnvbc2cRZmyvMCR9pd2JNERaQXKmB7m33qgQsVJ3mf3KrNufieUkfhsv9s-BK6BN-A/pub?gid=1455504577&single=true&output=csv",
}


def leer_sheet(nombre, url):
    """Lee una hoja de Google Sheets saltando la fila de titulo."""
    try:
        with urllib.request.urlopen(url.strip()) as r:
            contenido = r.read().decode("utf-8")

        # Linea 0 = titulo, Linea 1 = encabezados, Linea 2+ = datos
        lineas = contenido.split("\n")
        sin_titulo = "\n".join(lineas[1:])

        reader = csv.DictReader(io.StringIO(sin_titulo))
        filas = []
        for row in reader:
            fila = {}
            for k, v in row.items():
                if k and k.strip():
                    valor = v.strip().replace(",", ".")
                    fila[k.strip()] = valor
            if any(fila.values()):
                filas.append(fila)
        print(f"  {nombre}: {len(filas)} filas leidas")
        return filas
    except Exception as e:
        print(f"  ERROR en {nombre}: {e}")
        return []

def generar_texto():
    texto = ""

    # ── ESTUDIANTES ───────────────────────────────────────────
    datos = leer_sheet("Estudiantes", SHEETS["Estudiantes"])
    texto += "ESTUDIANTES REGISTRADOS:\n"
    for r in datos:
        if not r.get("Codigo"):
            continue
        texto += (
            f"\n- Codigo: {r.get('Codigo')} | "
            f"Nombre: {r.get('Nombre Completo')} | "
            f"Grado: {r.get('Grado')} | "
            f"Jornada: {r.get('Jornada')}\n"
            f"  Acudiente: {r.get('Acudiente')} | "
            f"Tel: {r.get('Tel Acudiente')} | "
            f"Ruta: {r.get('Ruta')}\n"
            f"  Notas -> Mat:{r.get('Mat')} | "
            f"Esp:{r.get('Esp')} | "
            f"Cie:{r.get('Cie')} | "
            f"Ing:{r.get('Ing')} | "
            f"Soc:{r.get('Soc')} | "
            f"Promedio:{r.get('Promedio')}\n"
        )

    # ── HORARIOS ──────────────────────────────────────────────
    datos = leer_sheet("Horarios", SHEETS["Horarios"])
    texto += "\nHORARIOS DE CLASES:\n"
    grado_actual = ""
    for r in datos:
        if not r.get("Grado"):
            continue
        if r["Grado"] != grado_actual:
            grado_actual = r["Grado"]
            texto += f"\nGrado {grado_actual}:\n"
        if r.get("Materia", "").upper() == "DESCANSO":
            texto += f"  {r.get('Hora Inicio')}-{r.get('Hora Fin')} → DESCANSO\n"
        else:
            texto += (
                f"  {r.get('Hora Inicio')}-{r.get('Hora Fin')} → "
                f"{r.get('Materia')} | "
                f"{r.get('Profesor')} | "
                f"{r.get('Dia')}\n"
            )

    # ── TAREAS ────────────────────────────────────────────────
    datos = leer_sheet("Tareas", SHEETS["Tareas"])
    texto += "\nTAREAS Y EVALUACIONES PENDIENTES:\n"
    grado_actual = ""
    for r in datos:
        if not r.get("Grado"):
            continue
        if r["Grado"] != grado_actual:
            grado_actual = r["Grado"]
            texto += f"\nGrado {grado_actual}:\n"
        texto += (
            f"  [{r.get('Tipo')}] {r.get('Materia')}: "
            f"{r.get('Descripcion')} | "
            f"Entrega: {r.get('Fecha Entrega')} | "
            f"Profesor: {r.get('Profesor')} | "
            f"Estado: {r.get('Estado')}\n"
        )

    # ── PROFESORES ────────────────────────────────────────────
    datos = leer_sheet("Profesores", SHEETS["Profesores"])
    texto += "\nDIRECTORIO DE PROFESORES:\n"
    for r in datos:
        if not r.get("Nombre"):
            continue
        texto += (
            f"\n- {r.get('Nombre')} | "
            f"Materia: {r.get('Materia')} | "
            f"Grados: {r.get('Grados que Dicta')}\n"
            f"  Aula: {r.get('Aula')} | "
            f"Email: {r.get('Email')} | "
            f"Atencion padres: {r.get('Horario Atencion Padres')}\n"
        )

    # ── ASISTENCIAS ───────────────────────────────────────────
    datos = leer_sheet("Asistencias", SHEETS["Asistencias"])
    texto += "\nREGISTRO DE ASISTENCIAS:\n"

    # Agrupar registros por estudiante
    por_estudiante = {}
    for r in datos:
        if not r.get("Codigo"):
            continue
        codigo = r.get("Codigo")
        if codigo not in por_estudiante:
            por_estudiante[codigo] = {
                "nombre":    r.get("Nombre"),
                "grado":     r.get("Grado"),
                "registros": []
            }
        por_estudiante[codigo]["registros"].append({
            "fecha":  r.get("Fecha"),
            "estado": r.get("Estado"),
            "excusa": r.get("Excusa", "")
        })

    for codigo, info in por_estudiante.items():
        registros  = info["registros"]
        total      = len(registros)
        presentes  = sum(1 for x in registros if x["estado"] == "Presente")
        ausentes   = sum(1 for x in registros if x["estado"] == "Ausente")
        tardes     = sum(1 for x in registros if x["estado"] == "Tarde")
        con_excusa = sum(1 for x in registros if x["estado"] == "Ausente" and x["excusa"] == "Si")
        sin_excusa = sum(1 for x in registros if x["estado"] == "Ausente" and x["excusa"] == "No")
        porcentaje = round((presentes / total) * 100) if total > 0 else 0

        texto += (
            f"\n- Codigo: {codigo} | "
            f"Nombre: {info['nombre']} | "
            f"Grado: {info['grado']}\n"
            f"  Asistencia: {presentes}/{total} dias ({porcentaje}%) | "
            f"Ausencias: {ausentes} | "
            f"Tardanzas: {tardes}\n"
            f"  Ausencias con excusa: {con_excusa} | "
            f"Sin excusa: {sin_excusa}\n"
            f"  Detalle por fecha:\n"
        )
        for reg in registros:
            excusa_txt = f"(excusa: {reg['excusa']})" if reg["estado"] != "Presente" else ""
            texto += f"    * {reg['fecha']}: {reg['estado']} {excusa_txt}\n"

    return texto


# ── Generar datos_colegio.py ──────────────────────────────────
print("Leyendo datos desde Google Sheets...")
contexto = generar_texto()

codigo = f'''# AUTO-GENERADO por leer_datos.py
# No edites este archivo directamente.
# Edita el Google Sheet y vuelve a correr: python leer_datos.py

def generar_contexto_completo():
    return """{contexto}"""
'''

with open("datos_colegio.py", "w", encoding="utf-8") as f:
    f.write(codigo)

print("\ndatos_colegio.py generado correctamente.")
print("Ahora corre: streamlit run app.py")

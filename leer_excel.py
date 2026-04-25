"""
leer_excel.py
Ejecuta este script cada vez que actualices datos_colegio.xlsx
Genera automaticamente datos_colegio.py para que el chatbot lo use.
Uso: python leer_excel.py
"""

import pandas as pd

ARCHIVO = "datos_colegio.xlsx"

print("Leyendo Excel...")

# ── Leer hojas ────────────────────────────────────────────────
estudiantes = pd.read_excel(ARCHIVO, sheet_name="Estudiantes", header=1)
horarios    = pd.read_excel(ARCHIVO, sheet_name="Horarios",    header=1)
tareas      = pd.read_excel(ARCHIVO, sheet_name="Tareas",      header=1)
profesores  = pd.read_excel(ARCHIVO, sheet_name="Profesores",  header=1)

# Limpiar NaN
estudiantes = estudiantes.dropna(subset=["Codigo"])
horarios    = horarios.dropna(subset=["Grado"])
tareas      = tareas.dropna(subset=["Grado"])
profesores  = profesores.dropna(subset=["Nombre"])

# ── Construir texto de contexto ───────────────────────────────
def generar_texto():
    texto = ""

    # ESTUDIANTES
    texto += "ESTUDIANTES REGISTRADOS:\n"
    for _, row in estudiantes.iterrows():
        promedio = row.get("Promedio", "N/A")
        texto += (
            f"\n- Codigo: {int(row['Codigo'])} | Nombre: {row['Nombre Completo']} | "
            f"Grado: {row['Grado']} | Jornada: {row['Jornada']}\n"
            f"  Acudiente: {row['Acudiente']} | Tel: {row['Tel Acudiente']} | Ruta: {row['Ruta']}\n"
            f"  Notas -> Mat:{row['Mat']} Esp:{row['Esp']} Cie:{row['Cie']} Ing:{row['Ing']} Soc:{row['Soc']}"
            f" | Promedio: {round(float(promedio),1) if pd.notna(promedio) else 'N/A'}\n"
        )

    # HORARIOS
    texto += "\nHORARIOS DE CLASES:\n"
    for grado in horarios["Grado"].unique():
        texto += f"\nGrado {grado}:\n"
        bloque = horarios[horarios["Grado"] == grado]
        for _, r in bloque.iterrows():
            if str(r["Materia"]).upper() == "DESCANSO":
                texto += f"  {r['Hora Inicio']}-{r['Hora Fin']} → DESCANSO\n"
            else:
                texto += f"  {r['Hora Inicio']}-{r['Hora Fin']} → {r['Materia']} | {r['Profesor']} | {r['Dia']}\n"

    # TAREAS
    texto += "\nTAREAS Y EVALUACIONES PENDIENTES:\n"
    for grado in tareas["Grado"].unique():
        texto += f"\nGrado {grado}:\n"
        bloque = tareas[tareas["Grado"] == grado]
        for _, r in bloque.iterrows():
            texto += (
                f"  [{r['Tipo']}] {r['Materia']}: {r['Descripcion']} "
                f"| Entrega: {r['Fecha Entrega']} | {r['Profesor']} | Estado: {r['Estado']}\n"
            )

    # PROFESORES
    texto += "\nDIRECTORIO DE PROFESORES:\n"
    for _, r in profesores.iterrows():
        texto += (
            f"\n- {r['Nombre']} | Materia: {r['Materia']}\n"
            f"  Grados: {r['Grados que Dicta']} | Aula: {r['Aula']}\n"
            f"  Email: {r['Email']} | Atencion padres: {r['Horario Atencion Padres']}\n"
        )

    return texto


# ── Guardar datos_colegio.py ──────────────────────────────────
contexto = generar_texto()

codigo_python = f'''# AUTO-GENERADO por leer_excel.py
# No edites este archivo directamente.
# Edita datos_colegio.xlsx y vuelve a correr: python leer_excel.py

def generar_contexto_completo():
    return """{contexto}"""
'''

with open("datos_colegio.py", "w", encoding="utf-8") as f:
    f.write(codigo_python)

print("datos_colegio.py generado correctamente.")
print(f"  Estudiantes: {len(estudiantes)}")
print(f"  Filas horario: {len(horarios)}")
print(f"  Tareas: {len(tareas)}")
print(f"  Profesores: {len(profesores)}")
print("\nYa puedes correr: streamlit run app.py")

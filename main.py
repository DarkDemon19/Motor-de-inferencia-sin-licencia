from parser_es import parsear_regla, ErrorAnalisis
from atomos import TablaAtomos
from tableau import construir_arbol, mostrar_arbol
from normalizar import dividir_reglas

def main():
    print("=" * 66)
    print(" ANALIZADOR DE REGLAS EN ESPAÑOL Y ÁRBOLES SEMÁNTICOS")
    print("=" * 66)
    print("Escribe una regla por línea. Línea vacía para terminar.")
    print("Ejemplo: Si es de día, entonces voy a trabajar")
    print("Puedes usar: y, o, no, si... entonces, si y solo si.")
    print("Escribe 'fin' en una línea vacía para procesar.")
    lineas = []
    while True:
        try:
            linea = input(f"R{len(lineas)+1}> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not linea or linea.lower() == "fin":
            break
        lineas.append(linea)

    reglas = dividir_reglas(lineas)
    if not reglas:
        print("No se introdujeron reglas.")
        return

    tabla = TablaAtomos()
    formulas = []
    print("\n1) ANÁLISIS Y FORMALIZACIÓN")
    for i, regla in enumerate(reglas, 1):
        try:
            formula = parsear_regla(regla, tabla)
            formulas.append(formula)
            print(f"R{i}: {regla}")
            print(f"    Fórmula: {formula}")
        except ErrorAnalisis as exc:
            print(f"\nNo pude interpretar R{i}: {regla}")
            print(f"Detalle: {exc}")
            print("Reformula la regla con conectores explícitos (y, o, no, si... entonces, si y solo si).")
            return

    print("\n2) TABLA DE ÁTOMOS")
    for letra, significado in tabla.items():
        print(f"  {letra} = {significado}")

    print("\n3) ÁRBOL SEMÁNTICO")
    arbol = construir_arbol(formulas)
    print(mostrar_arbol(arbol))

    abiertas = [r for r in arbol if r.abierta]
    cerradas = [r for r in arbol if r.cerrada]
    print("\n4) RESULTADO")
    print(f"Ramas abiertas: {len(abiertas)}")
    print(f"Ramas cerradas: {len(cerradas)}")
    if abiertas:
        print("La base de conocimiento es SATISFACIBLE.")
        for i, rama in enumerate(abiertas, 1):
            valores = rama.asignacion()
            print(f"  Modelo {i}: " + ", ".join(f"{k} = {'V' if v else 'F'}" for k, v in valores.items()))
    else:
        print("La base de conocimiento es INSATISFACIBLE: todas las ramas se cerraron.")

if __name__ == "__main__":
    main()

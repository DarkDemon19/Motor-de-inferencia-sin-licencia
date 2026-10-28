from dataclasses import dataclass, field
from logica import Formula

@dataclass
class Rama:
    formulas: list = field(default_factory=list)
    aplicadas: set = field(default_factory=set)
    cerrada: bool = False
    abierta: bool = False
    motivo: str = ""

    def asignacion(self):
        valores = {}
        for f in self.formulas:
            signo, letra = literal(f)
            if letra:
                valores[letra] = signo
        return dict(sorted(valores.items()))

def literal(f):
    if f.op == "atom":
        return True, f.atom
    if f.op == "not" and f.izquierda.op == "atom":
        return False, f.izquierda.atom
    return None, None

def contradiccion(formulas):
    vistos = {}
    for f in formulas:
        signo, letra = literal(f)
        if letra is not None:
            if letra in vistos and vistos[letra] != signo:
                return letra
            vistos[letra] = signo
    return None

def expandir(formula):
    """Devuelve (tipo, listas): tipo 'una' o 'dos'; cada lista es un conjunto de fórmulas."""
    op = formula.op
    if op == "atom":
        return None
    if op == "not":
        a = formula.izquierda
        if a.op == "atom":
            return None
        if a.op == "not": return ("una", [[a.izquierda]])
        if a.op == "and": return ("dos", [[neg(a.izquierda)], [neg(a.derecha)]])
        if a.op == "or": return ("una", [[neg(a.izquierda), neg(a.derecha)]])
        if a.op == "imp": return ("una", [[a.izquierda, neg(a.derecha)]])
        if a.op == "iff": return ("dos", [[a.izquierda, neg(a.derecha)], [neg(a.izquierda), a.derecha]])
    if op == "and": return ("una", [[formula.izquierda, formula.derecha]])
    if op == "or": return ("dos", [[formula.izquierda], [formula.derecha]])
    if op == "imp": return ("dos", [[neg(formula.izquierda)], [formula.derecha]])
    if op == "iff": return ("dos", [[formula.izquierda, formula.derecha], [neg(formula.izquierda), neg(formula.derecha)]])
    return None

def neg(f):
    if f.op == "not":
        return f.izquierda
    return Formula("not", izquierda=f)

def construir_arbol(formulas):
    """Construye un tableau por expansión de todas las fórmulas en una misma raíz."""
    pendientes = [Rama(formulas=list(formulas))]
    terminadas = []
    while pendientes:
        rama = pendientes.pop()
        conflicto = contradiccion(rama.formulas)
        if conflicto:
            rama.cerrada = True
            rama.motivo = f"contiene {conflicto} y ¬{conflicto}"
            terminadas.append(rama)
            continue
        candidato = None
        expansion = None
        for idx, f in enumerate(rama.formulas):
            if idx in rama.aplicadas:
                continue
            exp = expandir(f)
            if exp is not None:
                candidato, expansion = idx, exp
                # Heurística: preferir reglas de una rama para reducir bifurcaciones.
                if exp[0] == "una":
                    break
        if candidato is None:
            rama.abierta = True
            terminadas.append(rama)
            continue
        rama.aplicadas.add(candidato)
        tipo, alternativas = expansion
        if tipo == "una":
            rama.formulas.extend(alternativas[0])
            pendientes.append(rama)
        else:
            for alternativa in reversed(alternativas):
                nueva = Rama(
                    formulas=list(rama.formulas) + alternativa,
                    aplicadas=set(rama.aplicadas)
                )
                pendientes.append(nueva)
    return terminadas

def mostrar_arbol(ramas):
    """Vista textual compacta de las ramas finales y su estado."""
    lineas = []
    for i, rama in enumerate(ramas, 1):
        estado = "CERRADA ✕" if rama.cerrada else "ABIERTA ✓"
        lineas.append(f"Rama final {i} — {estado}")
        lineas.append("  " + " ; ".join(str(f) for f in rama.formulas))
        if rama.motivo:
            lineas.append("  Motivo: " + rama.motivo)
        lineas.append("")
    return "\n".join(lineas).rstrip()

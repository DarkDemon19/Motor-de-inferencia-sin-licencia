from dataclasses import dataclass

@dataclass(frozen=True)
class Formula:
    op: str
    izquierda: object = None
    derecha: object = None
    atom: str = None

    def __str__(self):
        if self.op == "atom":
            return self.atom
        if self.op == "not":
            return f"¬{self.izquierda}"
        simbolos = {"and": "∧", "or": "∨", "imp": "→", "iff": "↔"}
        return f"({self.izquierda} {simbolos[self.op]} {self.derecha})"

def Atomo(letra): return Formula("atom", atom=letra)
def Negar(a): return Formula("not", izquierda=a)
def Binaria(op, a, b): return Formula(op, a, b)

def atomos_en(formula):
    if formula.op == "atom":
        return {formula.atom}
    if formula.op == "not":
        return atomos_en(formula.izquierda)
    return atomos_en(formula.izquierda) | atomos_en(formula.derecha)

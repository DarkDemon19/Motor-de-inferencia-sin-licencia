import re
from logica import Atomo, Negar, Binaria
from normalizar import normalizar

class ErrorAnalisis(ValueError):
    pass

# El lexer conserva las frases normales como tokens atómicos y separa conectores.
PATRON = re.compile(
    r"\s*(\bsi\s+y\s+solo\s+si\b|\bsi\b|\bentonces\b|\by\b|\bo\b|\bno\b|,|\(|\))\s*",
    re.IGNORECASE
)

def tokenizar(texto):
    texto = normalizar(texto)
    partes = PATRON.split(texto)
    tokens = []
    for parte in partes:
        p = parte.strip()
        if not p or p == ",":
            continue
        tokens.append(p)
    return tokens

class Parser:
    def __init__(self, tokens, tabla):
        self.tokens = tokens
        self.i = 0
        self.tabla = tabla

    def actual(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def aceptar(self, valor):
        if self.actual() is not None and self.actual().lower() == valor:
            self.i += 1
            return True
        return False

    def exigir(self, valor):
        if not self.aceptar(valor):
            raise ErrorAnalisis(f"Se esperaba '{valor}' cerca de '{self.actual()}'.")

    def parsear(self):
        f = self.iff()
        if self.actual() is not None:
            raise ErrorAnalisis(f"Texto no reconocido al final: '{' '.join(self.tokens[self.i:])}'.")
        return f

    def iff(self):
        izquierda = self.imp()
        while self.aceptar("si y solo si"):
            derecha = self.imp()
            izquierda = Binaria("iff", izquierda, derecha)
        return izquierda

    def imp(self):
        # Forma condicional natural: «si antecedente, entonces consecuente».
        if self.aceptar("si"):
            antecedente = self.or_expr()
            self.exigir("entonces")
            consecuente = self.imp()
            return Binaria("imp", antecedente, consecuente)
        izquierda = self.or_expr()
        if self.aceptar("entonces"):
            derecha = self.imp()
            return Binaria("imp", izquierda, derecha)
        return izquierda

    def or_expr(self):
        izquierda = self.and_expr()
        while self.aceptar("o"):
            derecha = self.and_expr()
            izquierda = Binaria("or", izquierda, derecha)
        return izquierda

    def and_expr(self):
        izquierda = self.unario()
        while self.aceptar("y"):
            derecha = self.unario()
            izquierda = Binaria("and", izquierda, derecha)
        return izquierda

    def unario(self):
        if self.aceptar("no"):
            return Negar(self.unario())
        if self.aceptar("("):
            f = self.iff()
            self.exigir(")")
            return f
        return self.atom()

    def atom(self):
        # Junta palabras hasta hallar un conector o paréntesis.
        inicio = self.i
        while self.actual() is not None and self.actual().lower() not in {
            "si", "entonces", "y", "o", "no", "si y solo si", "(", ")"
        }:
            self.i += 1
        if self.i == inicio:
            raise ErrorAnalisis(f"Se esperaba una proposición simple; se encontró '{self.actual()}'.")
        frase = " ".join(self.tokens[inicio:self.i]).strip()
        if not frase:
            raise ErrorAnalisis("Se encontró una proposición vacía.")
        return Atomo(self.tabla.obtener(frase))

def parsear_regla(texto, tabla):
    tokens = tokenizar(texto)
    if not tokens:
        raise ErrorAnalisis("La regla está vacía.")
    return Parser(tokens, tabla).parsear()

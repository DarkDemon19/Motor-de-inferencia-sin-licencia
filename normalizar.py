import re
import unicodedata

def sin_acentos(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto) if unicodedata.category(c) != "Mn")

def normalizar(texto: str) -> str:
    texto = texto.strip().lower()
    texto = re.sub(r"\s+", " ", texto)
    texto = texto.replace("¿", "").replace("?", "").replace("¡", "").replace("!", "")
    return texto.strip(" .;")

def dividir_reglas(lineas):
    """Una regla por línea; también permite separar reglas unidas por punto y coma."""
    reglas = []
    for linea in lineas:
        reglas.extend(x.strip() for x in re.split(r"[;\n]+", linea) if x.strip())
    return reglas

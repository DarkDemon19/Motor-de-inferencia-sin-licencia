from normalizar import normalizar

class TablaAtomos:
    def __init__(self):
        self._significado_a_letra = {}
        self._letra_a_significado = {}

    def obtener(self, significado: str) -> str:
        significado = normalizar(significado)
        if significado not in self._significado_a_letra:
            letra = chr(ord("p") + len(self._significado_a_letra))
            if len(self._significado_a_letra) >= 10:
                letra = f"p{len(self._significado_a_letra)-9}"
            self._significado_a_letra[significado] = letra
            self._letra_a_significado[letra] = significado
        return self._significado_a_letra[significado]

    def items(self):
        return self._letra_a_significado.items()

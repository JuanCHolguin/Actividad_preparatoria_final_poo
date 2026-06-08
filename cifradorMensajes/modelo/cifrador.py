from abc import ABC, abstractmethod
from cifradorMensajes.modelo.errores import ContieneNumero, ContieneNoAscii, SinLetras, NoTrim, DobleEspacio


class ReglaCifrado(ABC):
    def __init__(self, token: int):
        self.token: int = token

    @abstractmethod
    def encriptar (self, mensaje: str) -> str:
        pass

    @abstractmethod
    def desencriptar (self, mensaje: str) -> str:
        pass

    @abstractmethod
    def mensaje_valido (self, mensaje: str) -> bool:
        pass

    def encontrar_numeros_mensaje(self, mensaje: str) -> list:
        return [
            (i,c)
            for (i,c) in enumerate(mensaje)
            if c.isdigit()
        ]
    def encontrar_no_ascii_mensaje(self, mensaje: str) -> list:
        return[
            (i,c)
            for (i,c) in enumerate(mensaje)
            if not c.isascii()
        ]

class ReglaCifradoTraslacion(ReglaCifrado):

    def __init__(self, token: int):
        super().__init__(token)

    def mensaje_valido (self, mensaje: str) -> bool:
        mensaje = mensaje.lower()
        errores = []

        numeros = self.encontrar_numeros_mensaje(mensaje)
        caracteres_invalidos = self.encontrar_no_ascii_mensaje(mensaje)

        if numeros:
            errores.append(ContieneNumero(str(numeros)))

        if caracteres_invalidos:
            errores.append(ContieneNoAscii(str(caracteres_invalidos)))

        mensaje_espacios = mensaje.strip()
        if not mensaje_espacios or not any(c.isalpha() for c in mensaje):

            errores.append(SinLetras(str(mensaje_espacios)))

        if errores:
            raise ExceptionGroup(
                "ContieneNumero"
                "ContieneNoAscii"
                "SinLetras",
                errores
            )
        return True

    def encriptar(self, mensaje: str) -> str:
        mensaje = mensaje.lower()
        self.mensaje_valido(mensaje)

        resultado = ""

        for c in mensaje:
            if c.isalpha():
                posicion = ord(c) - ord('a')
                nueva_posicion = (posicion + self.token) % 26
                nueva_letra = chr(nueva_posicion + ord('a'))
                resultado += nueva_letra
            else:
                resultado += c
        return resultado

    def desencriptar(self, mensaje: str) -> str:
        mensaje = mensaje.lower()

        resultado = ""

        for c in mensaje:
            if c.isalpha():
                posicion = ord(c) - ord('a')
                nueva_posicion = (posicion - self.token) % 26
                nueva_letra = chr(nueva_posicion + ord('a'))
                resultado += nueva_letra
            else:
                resultado += c
        return resultado

class ReglaCifradoNumerico (ReglaCifrado):

    def __init__(self, token: int):
        super().__init__(token)

    def mensaje_valido(self, mensaje: str) -> bool:
        mensaje = mensaje.lower()

        numero = self.encontrar_numeros_mensaje(mensaje)
        errores = []

        if numero:
            errores.append(ContieneNumero(str(numero)))

        if mensaje != mensaje.strip():
                errores.append(NoTrim(str(mensaje)))

        if "  " in mensaje:
            errores.append(DobleEspacio(str(" ")))

        if errores:
            raise ExceptionGroup(
                "ContieneNumero"
                "NoTrim"
                "DobleEspacio",
                errores
            )
        return True

    def encriptar(self, mensaje: str) -> str:
        mensaje = mensaje.lower()
        self.mensaje_valido(mensaje)

        resultado = []
        for c in mensaje:
            if c.isascii():
                caracter = ord(c) * self.token
                resultado.append(str(caracter))
        return " ".join(resultado)


    def desencriptar(self, mensaje: str) -> str:
        mensaje = mensaje.lower()
        self.mensaje_valido(mensaje)

        resultado = []
        mensaje = mensaje.split()
        for c in mensaje:
            caracter = int(c) / self.token
            nuevo_caracter = chr(int(caracter))
            resultado += nuevo_caracter

        return "".join(resultado)


class Cifrador:

    def __init__(self, agente: ReglaCifrado):
        self.agente = agente

    def encriptar(self, mensaje: str) -> str:
        return self.agente.encriptar(mensaje)

    def desencriptar(self, mensaje: str) -> str:
        return self.agente.desencriptar(mensaje)





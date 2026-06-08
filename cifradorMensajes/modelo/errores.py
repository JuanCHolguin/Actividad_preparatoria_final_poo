class ErrorFormato(Exception):
    pass
class DobleEspacio(ErrorFormato):
    pass
class SinLetras(ErrorFormato):
    pass
class NoTrim(ErrorFormato):
    pass
class ErrorContenido(Exception):
    pass
class ContieneNumero(ErrorContenido):
    pass
class ContieneNoAscii(ErrorContenido):
    pass



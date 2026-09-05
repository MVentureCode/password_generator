import secrets
import string


CARACTERES_ESPECIALES = "!@#$%^&*"


def generar_contrasena(
    longitud=12,
    mayusculas=True,
    minusculas=True,
    numeros=True,
    especiales=True,
):
    """Genera una contraseña con al menos un carácter de cada tipo elegido."""
    grupos = []
    if mayusculas:
        grupos.append(string.ascii_uppercase)
    if minusculas:
        grupos.append(string.ascii_lowercase)
    if numeros:
        grupos.append(string.digits)
    if especiales:
        grupos.append(CARACTERES_ESPECIALES)

    if not grupos:
        raise ValueError("Debe seleccionar al menos un tipo de carácter.")
    if not 8 <= longitud <= 32:
        raise ValueError("La longitud debe estar entre 8 y 32 caracteres.")
    if longitud < len(grupos):
        raise ValueError("La longitud es insuficiente para los tipos seleccionados.")

    caracteres = "".join(grupos)
    contrasena = [secrets.choice(grupo) for grupo in grupos]
    contrasena.extend(
        secrets.choice(caracteres) for _ in range(longitud - len(contrasena))
    )
    secrets.SystemRandom().shuffle(contrasena)
    return "".join(contrasena)


def calcular_fuerza(contrasena):
    """Calcula una fuerza básica de 0 a 100 para una contraseña."""
    puntuacion = min(len(contrasena) * 2, 40)
    criterios = (
        any(caracter in string.ascii_uppercase for caracter in contrasena),
        any(caracter in string.ascii_lowercase for caracter in contrasena),
        any(caracter in string.digits for caracter in contrasena),
        any(caracter in CARACTERES_ESPECIALES for caracter in contrasena),
    )
    puntuacion += sum(criterios) * 15
    return min(puntuacion, 100)

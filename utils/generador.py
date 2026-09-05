import secrets
import string


CARACTERES_ESPECIALES = "!@#$%^&*"
CARACTERES_AMBIGUOS = "O0Il1"


def _quitar_caracteres_ambiguos(caracteres):
    return "".join(
        caracter for caracter in caracteres if caracter not in CARACTERES_AMBIGUOS
    )


def generar_contrasena(
    longitud=12,
    mayusculas=True,
    minusculas=True,
    numeros=True,
    especiales=True,
    evitar_ambiguos=True,
):
    """Genera una contraseña con al menos un carácter de cada tipo elegido."""
    grupos_caracteres = []
    if mayusculas:
        grupos_caracteres.append(string.ascii_uppercase)
    if minusculas:
        grupos_caracteres.append(string.ascii_lowercase)
    if numeros:
        grupos_caracteres.append(string.digits)
    if especiales:
        grupos_caracteres.append(CARACTERES_ESPECIALES)

    if not grupos_caracteres:
        raise ValueError("Debe seleccionar al menos un tipo de carácter.")
    if not 8 <= longitud <= 32:
        raise ValueError("La longitud debe estar entre 8 y 32 caracteres.")
    if longitud < len(grupos_caracteres):
        raise ValueError("La longitud es insuficiente para los tipos seleccionados.")

    if evitar_ambiguos:
        grupos_caracteres = [
            _quitar_caracteres_ambiguos(grupo) for grupo in grupos_caracteres
        ]

    conjunto_caracteres = "".join(grupos_caracteres)
    contrasena = [
        secrets.choice(grupo_caracteres) for grupo_caracteres in grupos_caracteres
    ]
    contrasena.extend(
        secrets.choice(conjunto_caracteres)
        for _ in range(longitud - len(contrasena))
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

Password Generator:

Aplicación de escritorio desarrollada en Python y Tkinter para generar contraseñas seguras y personalizables.


Descripción:

password_generator permite al usuario generar contraseñas indicando la longitud y los tipos de caracteres que desea utilizar.

La aplicación incorpora diferentes funcionalidades orientadas a mejorar la seguridad y la experiencia de uso, como el indicador de fuerza, la copia al portapapeles, el historial de contraseñas y la generación masiva.

Funcionalidades:
- Generación de contraseñas aleatorias.
- Selección de longitud entre 8 y 32 caracteres.
- Uso de:
Mayúsculas.
Minúsculas.
Números.
Caracteres especiales.
Indicador visual de la fuerza de la contraseña.
Copia de la contraseña al portapapeles.
Guardado del historial en un archivo .txt con fecha y hora.
Gestión de errores mediante mensajes de aviso.
Exclusión de caracteres ambiguos como O, 0, I, l y 1.
- Generación masiva de entre 5 y 10 contraseñas.
- Copia de todas las contraseñas generadas.
- Guardado de todas las contraseñas en un archivo .txt.
- Panel resumen de los criterios utilizados en la generación.

Tecnologías utilizadas:
- Python 3
- Tkinter para la interfaz gráfica.
- Git para el control de versiones.
- GitHub para el almacenamiento del repositorio.

Estructura del proyecto:
password_generator/
│
├── main.py
├── utils/
│   └── generador.py
├── historial.txt
├── .gitignore
└── README.md

Instalación
Clonar el repositorio:
git clone URL_DEL_REPOSITORIO

Acceder a la carpeta del proyecto:
cd password_generator

Crear y activar un entorno virtual:
python3 -m venv .venv
source .venv/bin/activate

Ejecutar la aplicación:
python3 main.py

Uso:
Seleccionar la longitud de la contraseña.
Elegir los tipos de caracteres que se desean utilizar.
Seleccionar, si se desea, la opción para evitar caracteres ambiguos.
Generar una contraseña individual o varias contraseñas de forma masiva.
Consultar el indicador de fuerza y el resumen de criterios aplicados.
Copiar o guardar las contraseñas generadas.
Control de versiones

El proyecto utiliza Git y GitHub para gestionar las diferentes versiones del código y mantener una copia del proyecto en un repositorio remoto.

Autor
María Victoria Galzadet
Proyecto desarrollado como parte de una actividad práctica de programación en Python.
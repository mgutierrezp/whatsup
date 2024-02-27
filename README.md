*** ENGLISH VERSION BELOW ***


INTRODUCCIÓN
==============
Busca entre tus objetos astronómicos favoritos y averigua de un vistazo cuáles de ellos son visibles justo ahora, a medianoche, o en la fecha y hora que quieras. Muestra sólo aquellos cuya altitud sea superior a un valor especificado, o los que estén alejados de la luna unos grados determinados. Ten una visión más realista y deja que whatsup realice un recorrido en Stellarium con los objetos seleccionados

INICIO RÁPIDO
==============
*** binarios precompilados disponibles para linux y windows ***
*** Sólo tienes que copiar el binario correspondiente de la carpeta "binaries".
*** copia el archivo conf 'whatsup.config.xml' junto al ejecutable. Personalícelo según sea necesario.

*** Instalación manual a continuación: ***

- Instalar Python >= 3.12

- Cree un nuevo entorno virtual y actívelo (asegúrese de que está ejecutando python v3 y no v2):

        $ python -m venv whatsup_venv

        # usuarios linux:

                $ source whatsup_env/bin/activate

        # usuarios de windows:

                # si usa powershell

                        $ whatsup_env\Scripts\Activate.ps1

                # Si utiliza un símbolo del sistema normal

                        $ whatsup_env\Scripts\activate.bat


- Instale las librerías python en su nuevo entorno virtual

        $ pip install -r requisitos.txt


USO
==============
opciones:

  -h, --help mostrar este mensaje de ayuda y salir
  -v escribir información de depuración. Opcional
  -V, --version mostrar el número de versión del programa y salir
  --objects OBJECTS Obligatorio. Fichero de texto con objetos o una lista separada por comas
  --datetime DATETIME, --dt DATETIME
                        Opcional. Fecha y hora de observación. Se aceptan múltiples formatos. Véase la biblioteca dateutil.parser python. Un formato común es "AAAA-MM-DD HH:MM". Por defecto: crepúsculo astronómico u hora actual si es posterior.
  --minalt MINALT Opcional. Altitud mínima ([0-90] grados). Por defecto 0
  --moon-separation MOON_SEPARATION, --ms MOON_SEPARATION
                        Opcional. Separación mínima a la luna ([0-360] grados). Por defecto 0
  --stellarium-tour, --st
                        Opcional. Realiza un stellarium tour


--objects
        simplemente especifique la lista de objetos que desee. Puede escribir una lista de objetos separada por comas. Más fácil, puede especificar el nombre de un archivo de texto que contenga dichos objetos, uno por línea. Tenga cuidado de entrecomillar el argumento en los espacios están presentes.

        Ejemplos:
                whatsup --objects M31,M42,NGC1499
                whatsup --objects ./miArchivoObjetos.txt
                whatsup --objects "M 31, M 42"

--datetime, --dt FECHA
        fecha y hora de observación. Consulte los formatos compatibles: https://dateutil.readthedocs.io/en/stable/parser.html. Si no se especifica, se establece automáticamente el próximo crepúsculo astronómico, o la hora actual si es posterior.
        Normalmente debería ser suficiente con "AAAA-MM-DD HH:MM" o simplemente "HH:MM".
        Si se especifica el formato "HH:MM", se añadirá un día extra si la hora es posterior a medianoche.

        Ejemplos:
                whatsup --objects M31.M42 --dt "2024-02-27 21:00"
                whatsup --objects M31,M42 --dt 01:00 # se traducirá a "2024-02-28 01:00"


--minalt MINALT
        filtra por objetos con una altitud superior a MINALT en la FECHA especificada

--separación_luna, --ms MOON_SEPARATION
        filtra los objetos que están a más de grados MOON_SEPARATION de la luna en la FECHA especificada

--stellarium, --st
        si se establece, hace un bucle sobre los resultados y enfoca cada objeto en Stellarium. Necesitas configurar Stellarium y el archivo de configuración de whatsup. Ver más abajo


Este es un ejemplo de ejecución muy típico

        whatsup.py --objects=M31,M42,NGC1499 --dt "20:00"  --ms 50 --minalt 40 --st

        2024/02/27 16:49:11 - INFO - --- STARTING ---
        2024/02/27 16:49:11 - INFO - running whatsup version 1.0a
        2024/02/27 16:49:12 - INFO - location: Madrid (Europe/Madrid)
        2024/02/27 16:49:12 - INFO - date/time: 2024-02-27 20:00:00+01:00
        2024/02/27 16:49:12 - INFO - moon illumination is 91%
        2024/02/27 16:49:12 - INFO - searching

        Starting stellarium tour

        object    rise time (above horizon)    meridian side    set time (below 40 deg)    moon separation    altitude @time
        --------  ---------------------------  ---------------  -------------------------  -----------------  ----------------
        M42       2024-02-27 14:42:05+01:00    east             2024-02-27 21:49:50+01:00  108d43m01.62s      43d54m27.85s
        NGC1499   2024-02-27 10:16:37+01:00    west             2024-02-27 23:11:18+01:00  126d54m48.23s      76d00m08.51s
        M31       2024-02-28 06:14:00+01:00    west             2024-02-26 20:06:17+01:00  144d26m54.70s      40d24m23.34s



ARCHIVO DE CONFIGURACIÓN
==============
Se proporciona un archivo de configuración whatsup.config.xml. Eche un vistazo
Este archivo debe residir en la misma carpeta que la aplicación whatsup.
Tendrá que cambiar el valor de "nombre de ubicación" y establecer la que está observando desde. Cambie la "zona horaria" en consecuencia.
Si quieres que whatsup realice un tour de Stellarium (ver parámetro --st arriba) necesitas habilitar el Control Remoto dentro de Stellarium: https://stellarium.org/doc/0.16/remoteControlDoc.html
Normalmente el host, esquema y puerto por defecto deberían funcionar. Cambia si es necesario







==========================================================================================



INTRODUCTION
==============

Search among your favorites astronomical objects and figure out at a glance which of them are visible just right now, at midnight, or whatever date and time you want. Show only those which an altitude greater than a specified value, or those far away from the moon some specified degrees. Have a more realistic view and let whatsup to perform a tour in Stellarium with the selected objects


QUICK START
==============

*** precompiled binaries available for linux and windows ***

*** just copy the corresponding binary from 'binaries' folder ***

*** copy the conf file 'whatsup.config.xml' alongside the executable. Customize as needed  ***




*** manual installation below: ***

- Install Python >= 3.12

- Create a new virtual environment and activate it (ensure you are executing python v3 and not v2!):
	$ python -m venv whatsup_venv
	# linux users:
		$ source whatsup_env/bin/activate
	# windows users:
		# if using powershell
			$ whatsup_env\Scripts\Activate.ps1
		# if using a regular command prompt
			$ whatsup_env\Scripts\activate.bat

- Install python libraries within your new virtual environment
	$ pip install -r requirements.txt



USAGE
==============
options:
  -h, --help            show this help message and exit
  -v                    write some debug info. Optional
  -V, --version         show program's version number and exit
  --objects OBJECTS     Mandatory. Text file with objects or a comma separated list
  --datetime DATETIME, --dt DATETIME
                        Optional. Observation date and time. Multiple formats accepted. See dateutil.parser python library. A common format is "YYYY-MM-DD HH:MM". Default: astronomical twilight or current time if later
  --minalt MINALT       Optional. Minimum altitude ([0-90] degrees). Default 0
  --moon-separation MOON_SEPARATION, --ms MOON_SEPARATION
                        Optional. Minimum separation to the moon ([0-360] degrees). Default 0
  --stellarium-tour, --st
                        Optional. Perform a stellarium tour


--objects
	simply specify the desired list of objects of your choice. You can type a comma-separated list of objects. Easier, you can specify the name of a text file containing such objects, one per line. Take care to quote the argument in spaces are present.
	Examples:
		whatsup --objects M31,M42,NGC1499
		whatsup --objects ./myObjectsFile.txt
		whatsup --objects "M 31, M 42"

--datetime, --dt DATETIME
	observation date and time. Have a look to supported formats: https://dateutil.readthedocs.io/en/stable/parser.html. If not specified, next astronomical twilight is automatically set, or the current time if later
	Normally it should be enough with "YYYY-MM-DD HH:MM" or simply "HH:MM"
	If format "HH:MM" is specified, an extra day will be added if the time is after midnight.
	Examples:
		whatsup --objects M31.M42 --dt "2024-02-27 21:00"
		whatsup --objects M31,M42 --dt 01:00       # will be translated to "2024-02-28 01:00"

--minalt MINALT
	filter by objects with an altitude higher than MINALT at the specified DATETIME

--moon-separation, --ms MOON_SEPARATION
	filter by objects that are more than MOON_SEPARATION degrses from the moon at the specified DATETIME

--stellarium, --st
	if set, loops over the results and focus each object on Stellarium. You need to setup Stellarium and whatsup config file. See below


This is a very typical execution example:

	whatsup.py --objects=M31,M42,NGC1499 --dt "20:00"  --ms 50 --minalt 40 --st

	2024/02/27 16:49:11 - INFO - --- STARTING ---
	2024/02/27 16:49:11 - INFO - running whatsup version 1.0a
	2024/02/27 16:49:12 - INFO - location: Madrid (Europe/Madrid)
	2024/02/27 16:49:12 - INFO - date/time: 2024-02-27 20:00:00+01:00
	2024/02/27 16:49:12 - INFO - moon illumination is 91%
	2024/02/27 16:49:12 - INFO - searching

	Starting stellarium tour

	object    rise time (above horizon)    meridian side    set time (below 40 deg)    moon separation    altitude @time
	--------  ---------------------------  ---------------  -------------------------  -----------------  ----------------
	M42       2024-02-27 14:42:05+01:00    east             2024-02-27 21:49:50+01:00  108d43m01.62s      43d54m27.85s
	NGC1499   2024-02-27 10:16:37+01:00    west             2024-02-27 23:11:18+01:00  126d54m48.23s      76d00m08.51s
	M31       2024-02-28 06:14:00+01:00    west             2024-02-26 20:06:17+01:00  144d26m54.70s      40d24m23.34s





CONFIG FILE
==============
A whatsup.config.xml config file is provided. Have a look

This file must reside on the same folder as whatsup application.

You will need to change the "location name" value and set the one you are observing from. Change the "timezone" accordingly.

If you want to whatsup to perform a Stellarium tour (see parameter --st above) you need to enable the Remote Control within Stellarium: https://stellarium.org/doc/0.16/remoteControlDoc.html
Usually the default host, scheme and port should work. Change if needed

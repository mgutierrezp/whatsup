INTRODUCCIÓN
==============
Busca entre tus objetos astronómicos favoritos y averigua de un vistazo cuáles de ellos son visibles justo ahora, a medianoche, o en la fecha y hora que quieras. Muestra sólo aquellos cuya altitud sea superior a un valor especificado, o los que estén alejados de la luna unos grados determinados. Ten una visión más realista y deja que whatsup realice un recorrido en Stellarium con los objetos seleccionados

INICIO RÁPIDO (recomendado)
==============
La forma más rápida es descargar los binarios precompilados disponibles para linux y windows.  
Sólo tienes que copiar el binario correspondiente de la carpeta "binaries".  
Copia el archivo conf 'whatsup.config.xml' junto al ejecutable. Edítelo y personalícelo según sea necesario.

INSTALACIÓN MANUAL (no recomendado)
==============
- Instalar Python >= 3.12
- Cree un nuevo entorno virtual y actívelo (asegúrese de que está ejecutando python v3 y no v2):

        $ python -m venv whatsup_venv
        # usuarios linux:

                $ source whatsup_env/bin/activate

        # usuarios de windows:
                # si usa powershell

                        $ whatsup_env\Scripts\Activate.ps1

                # si utiliza un símbolo del sistema normal

                        $ whatsup_env\Scripts\activate.bat

- Instale las librerías python en su nuevo entorno virtual

        $ pip install -r requirements.txt


USO
==============
opciones:

-h, --help  
&nbsp; &nbsp; Mostrar este mensaje de ayuda y salir  
-v  
&nbsp; &nbsp; Escribir información de depuración. Opcional  
-V, --version  
&nbsp; &nbsp; Mostrar el número de versión del programa y salir  
--objects OBJETOS  
&nbsp; &nbsp; Especifique la lista de objetos que desee. Puede escribir una lista de objetos separada por comas. Más fácil, puede especificar el nombre de un archivo de texto que contenga dichos objetos, uno por línea. Tenga cuidado de entrecomillar el argumento si hay espacios presentes.

        Ejemplos:
                whatsup --objects M31,M42,NGC1499
                whatsup --objects ./miArchivoDeObjetos.txt
                whatsup --objects "M 31, M 42"
--datetime, --dt FECHA
&nbsp; &nbsp; fecha y hora de observación. Consulte los formatos compatibles: https://dateutil.readthedocs.io/en/stable/parser.html. Si no se especifica, se establece automáticamente el próximo crepúsculo astronómico, o la hora actual si es posterior.  
        Normalmente debería ser suficiente con "AAAA-MM-DD HH:MM" o simplemente "HH:MM".
        Si se especifica el formato "HH:MM", se añadirá un día extra si la hora es posterior a medianoche.

        Ejemplos a día 27-02-2024:
                whatsup --objects M31,M42 --dt "2024-02-27 21:00"
                whatsup --objects M31,M42 --dt 01:00 # se traducirá a "2024-02-28 01:00"
--minalt MINALT  
&nbsp; &nbsp; Filtra por objetos con una altitud superior a MINALT (grados) en la FECHA especificada  
--moon-separation, --ms MOON_SEPARATION  
&nbsp; &nbsp; Filtra por objetos que están a más de MOON_SEPARATION grados de la luna en la FECHA especificada  
--stellarium, --st  
&nbsp; &nbsp; Si se establece, hace un bucle sobre los resultados y enfoca cada objeto en Stellarium. Necesitas configurar Stellarium y el archivo de configuración de whatsup. Ver más abajo  
--nina-hrz, --nh  
&nbsp; &nbsp; Si se establece, lee el archivo de horizontes de N.I.N.A. (.hrz) especificado en el xml (ver más abajo) y lo toma en cuenta para descartar objetos fuera del horizonte definido


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
Tendrá que cambiar el valor de "location" y establecer desde donde se está observando. Cambie la zona horaria "timezone" en consecuencia.  
Si quieres que whatsup realice un tour de Stellarium (ver parámetro --st arriba) necesitas habilitar el plugin Remote Control dentro de Stellarium: https://stellarium.org/doc/0.16/remoteControlDoc.html  
Normalmente el host, esquema y puerto por defecto deberían funcionar. Cámbielo si es necesario  
Se ha añadido también soporte para leer un archivo de horizontes de N.I.N.A. Descomente el tag 'nina horizon' y especifique el path donde reside dicho archivo. Después, al ejecutar WhatsUp, especifique la opción 'nina-hrz' para tener en cuenta este valor. Para que un objeto no sea descartado debe tener la altitud mínima 'minAlt' y estar debajo de este horizonte

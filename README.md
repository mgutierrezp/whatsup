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

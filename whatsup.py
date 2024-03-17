#!/usr/bin/env python3

VERSION="1.0c"

import sys,argparse,logging,os,traceback,xmltodict,pytz,urllib,ephem,platform,dateutil.parser,astropy,astroplan,warnings

if platform.system().lower() == "linux":
	from simple_term_menu import TerminalMenu

from tabulate import tabulate
import datetime as dt
from pathlib import Path
from astropy import units as u                                                                                                                                                                                                        
from astropy.coordinates import SkyCoord, AltAz, Angle
from functools import cmp_to_key
from tqdm import tqdm 
from astroplan import Observer, FixedTarget
from astropy.coordinates import EarthLocation
from astropy.time import Time

warnings.filterwarnings('ignore')

SCRIPT_DIR=Path(sys.argv[0]).parent
CONFIG_FILE=SCRIPT_DIR.joinpath(Path(Path(sys.argv[0]).stem).with_suffix(".config.xml"))
SCRIPT_NAME = Path(sys.argv[0]).stem


def loadConfig():
	if not os.path.exists(CONFIG_FILE):
		logger.critical("config file not found: %s" % CONFIG_FILE)
		sys.exit(1)

	try:
		with open(CONFIG_FILE, "r") as f:
			p=xmltodict.parse(f.read(), force_list=('zone'))
			
			EarthLocation.of_address(p["config"]["general"]["location"]["@name"])
			pytz.timezone(p["config"]["general"]["location"]["@timezone"])
			
			if options.nina_hrz:
				try:
					p["config"]["general"]["nina"]["@horizon"]
				except:
					logger.critical("N.I.N.A. horizon option has been specified, but no config exists. Please review!")
					sys.exit()
				if not os.path.exists(p["config"]["general"]["nina"]["@horizon"]) and options.nina_hrz:
					logger.critical("N.I.N.A. horizon file does not exist: %s" % p["config"]["general"]["nina"]["@horizon"])
					sys.exit()

	except Exception as e:
		logger.critical("error while parsing config file. Find below the original exception; most likely due to a syntax error in your config file")
		traceback.print_exc()
		sys.exit(1)

	return p

def checkMoonSeparation(sep):
	int(sep)
	if int(sep) < 0 or int(sep) > 360:
		raise ValueError
	else:
		return sep

def checkAltitude(sep):
	int(sep)
	if int(sep) < 0 or int(sep) > 90:
		raise ValueError
	else:
		return sep

def checkDatetime(d):
	dateutil.parser.parse(d)
	return d


def parse_options():
	usage = "%(prog)s"

	parser = argparse.ArgumentParser(usage=usage)
	parser.add_argument("-v", dest="verbose", action="store_true", help="write some debug info. Optional")
	parser.add_argument("-V", "--version", action="version", version=VERSION)
	parser.add_argument("--objects", action="store", help="Mandatory. Text file with objects or a comma separated list", required=True)
	parser.add_argument("--datetime", "--dt", type=checkDatetime, action="store", help="Optional. Observation date and time. Multiple formats accepted. See dateutil.parser python library. A common format is \"YYYY-MM-DD HH:MM\". Default: astronomical twilight or current time if later ", required=False)
	parser.add_argument("--minalt", action="store", type=checkAltitude, help="Optional. Minimum altitude ([0-90] degrees). Default 0", default=0)
	parser.add_argument("--moon-separation", "--ms", action="store", type=checkMoonSeparation, help="Optional. Minimum separation to the moon ([0-360] degrees). Default 0", default=0)
	parser.add_argument("--stellarium-tour", "--st", action="store_true", help="Optional. Perform a stellarium tour", default=False)
	parser.add_argument("--nina-hrz", "--nh", action="store_true", help="Optional. Set a N.I.N.A. horizon file to limit objects altitude (set file on xml config)", required=False, default=False)
	

	return parser

def setup_custom_logger(name, options):
    logger = logging.getLogger(name)

    formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

    if options.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def setStellariumFocus(target):
	urllib.request.urlopen("%s://%s:%s/api/main/focus" % (config["config"]["general"]["stellarium"]["@scheme"],config["config"]["general"]["stellarium"]["@host"],config["config"]["general"]["stellarium"]["@port"]),data=b"target=%b" % bytes(target,'utf-8'))

def setStellariumFocus2(target):
	urllib.request.urlopen("%s://%s:%s/api/main/focus" % (config["config"]["general"]["stellarium"]["@scheme"],config["config"]["general"]["stellarium"]["@host"],config["config"]["general"]["stellarium"]["@port"]),data=b"target=%b" % bytes(target.split()[0],'utf-8'))
	
def setStellariumTime(t):
	urllib.request.urlopen("%s://%s:%s/api/main/time" % (config["config"]["general"]["stellarium"]["@scheme"],config["config"]["general"]["stellarium"]["@host"],config["config"]["general"]["stellarium"]["@port"]),data=b"time=%b" % bytes(t,'utf-8'))


def checkStellariumStatus():
	try:
		urllib.request.urlopen("%s://%s:%s/api/main/status" % (config["config"]["general"]["stellarium"]["@scheme"],config["config"]["general"]["stellarium"]["@host"],config["config"]["general"]["stellarium"]["@port"]))
	except Exception as e:
		return e
	
	return True
	
def getTransit(stime, coords):
	return observer.target_meridian_transit_time(stime, coords).to_datetime(pytz.timezone(tz))

def mikSort(x, y):
	if x["meridian_side"] == y["meridian_side"]:
		if x["meridian_side"] == "east":
			return -1 if x["coordsAltAz"].alt < y["coordsAltAz"].alt else 1
		else:
			return -1 if x["coordsAltAz"].alt > y["coordsAltAz"].alt else 1
	
	return -1 if x["meridian_side"] == "east" else 1

def loadNinaHorizon():
	with open(config["config"]["general"]["nina"]["@horizon"]) as f:
		lines = [s.strip() for s in f.readlines()]
	hrz=list(filter(lambda x: x is not None, (map(lambda x: list(map(lambda y:Angle(y+"d"), x.split())) if not x.startswith("#") else None, lines))))
	hrz.sort(key=lambda x:x[0], reverse=False)
	return hrz

def getAltFromNinaHorizon(az, nina_hrz):
	prevPair=None
	for pair in nina_hrz:
		if pair[0] < az:
			prevPair=pair
			continue
		else:
			break
	
	if prevPair is None:
		return None
	pair1=prevPair
	pair2=pair
	
	return pair1[1]+((pair2[1]-pair1[1])/(pair2[0]-pair1[0]))*(az-pair1[0])
		
#####################################################################################


parser = parse_options()
options = parser.parse_args()

logger = setup_custom_logger('root', options)

logger.info("--- STARTING ---")
logger.info("running %s version %s" % (SCRIPT_NAME, VERSION))

config=loadConfig()
if options.nina_hrz:
	logger.info("loading N.I.N.A. horizon file: %s" % config["config"]["general"]["nina"]["@horizon"])
	nina_hrz=loadNinaHorizon()

location=config["config"]["general"]["location"]["@name"]
tz=config["config"]["general"]["location"]["@timezone"]
logger.info("location: %s (%s)" % (location, tz))

observatory_location = EarthLocation.of_address(location)
observer = Observer(location=observatory_location, name="Observer")

if not options.datetime:
	now=dt.datetime.now()
	#stime=now.astimezone(pytz.timezone(tz))
	stime=pytz.timezone(tz).localize(now)
	twilight=observer.twilight_evening_astronomical(astropy.time.Time(now.replace(hour=12))).to_datetime(pytz.timezone(tz))
	stime=twilight if stime < twilight else stime
	#stime = stime if stime != "[--]" else dt.datetime.now().astimezone(pytz.timezone(tz))
	stime = stime if stime != "[--]" else pytz.timezone(tz).localize(now)
else:
	#stime=dateutil.parser.parse(options.datetime).astimezone(pytz.timezone(tz))
	stime=pytz.timezone(tz).localize(dateutil.parser.parse(options.datetime))
	#stime = stime if stime > dt.datetime.now().astimezone(pytz.timezone(tz)) else  stime + dt.timedelta(days=1)
	stime = stime if stime > pytz.timezone(tz).localize(dt.datetime.now()) else  stime + dt.timedelta(days=1)
	
logger.info("date/time: %s" % stime)	
illum=round(astroplan.moon_illumination(astropy.time.Time(stime))*100)
logger.info("moon illumination is %s%%" % illum)
	
if os.path.exists(options.objects):
	with open(options.objects) as f:
		objects = [s.strip() for s in f.readlines()]
else:
	objects=options.objects.split(",")

visibleObjects=[]
moonAltAz = observer.moon_altaz(stime)
moonAlt, moonAz = moonAltAz.alt, moonAltAz.az
logger.debug("moon AltAz coords: alt %s az %s" %(moonAlt, moonAz))

objects=[] if len(objects) ==1 and objects[0]=='' else objects
logger.info("searching")
bar=tqdm(total=len(objects))
nonResolvedObjects=[]

for oobject in objects:
	bar.update()
	logger.debug("object: %s" % oobject)
	try:
		try:
			coords=SkyCoord.from_name(oobject)
		except astropy.coordinates.name_resolve.NameResolveError:
			nonResolvedObjects.append(oobject)
		coordsAltAz = coords.transform_to(AltAz(obstime=stime,location=observatory_location))
		moonSeparation=moonAltAz.separation(coords)
		logger.debug(" alt: %s" % coordsAltAz.alt)
		logger.debug(" az: %s"% coordsAltAz.az)
		logger.debug(" moon separation: %s" % moonSeparation)
		if options.nina_hrz: 
			minAltFromNinaHrz = getAltFromNinaHorizon(coordsAltAz.az, nina_hrz)
			logger.debug(" minimum altitude from nina horizon: %s" % minAltFromNinaHrz)
			
		if coordsAltAz.alt > Angle(str(options.minalt)+"d") and moonSeparation > Angle(str(options.moon_separation)+"d") \
		and (True if not options.nina_hrz else coordsAltAz.alt > minAltFromNinaHrz):
			transit = getTransit(stime, coords)
			meridianside = "west" if transit < stime else "east"
			logger.debug(" object meridian side: %s" % meridianside)
			logger.debug(" including")
			target_coordinates = SkyCoord.from_name(oobject)
			target = FixedTarget(coord=target_coordinates, name=oobject)
			#rise_time = observer.target_rise_time(astropy.time.Time(stime), target)
			rise_time = observer.target_rise_time(astropy.time.Time(stime), target, horizon=astropy.units.Quantity(options.minalt, unit='degree'))
			set_time = observer.target_set_time(astropy.time.Time(stime), target, horizon=astropy.units.Quantity(options.minalt, unit='degree'))
			visibleObjects.append({"object": oobject, "rise_time": rise_time, "meridian_side": meridianside, "coords": coords, "coordsAltAz": coordsAltAz, "transit": transit, 'moon_separation': moonSeparation, "set_time": set_time })
	except Exception as e:
		logger.warning(e)
		pass

bar.close()

if len(nonResolvedObjects) > 0: logger.warning("the following objects names could not be resolved: %s" % nonResolvedObjects)
	
print()
visibleObjects=sorted(visibleObjects, key=cmp_to_key(mikSort))

headers=["object","rise time (above %s deg)" % options.minalt, "meridian side", "set time (below %s deg)" % options.minalt, "moon separation", "altitude @time"]
t=[]

for visibleObject in visibleObjects:
	sanitizedRiseTime = visibleObject["rise_time"].to_datetime(pytz.timezone(tz)).isoformat(timespec='seconds', sep=" ") if not isinstance(visibleObject["rise_time"].to_datetime(pytz.timezone(tz)), astropy.utils.masked.core.MaskedNDArray) else "always above horizon"
	sanitizedSetTime = visibleObject["set_time"].to_datetime(pytz.timezone(tz)).isoformat(timespec='seconds', sep=" ") if not isinstance(visibleObject["set_time"].to_datetime(pytz.timezone(tz)), astropy.utils.masked.core.MaskedNDArray) else "--"
	t.append([visibleObject["object"], sanitizedRiseTime, visibleObject["meridian_side"], sanitizedSetTime, visibleObject['moon_separation'].to_string(precision=2), visibleObject["coordsAltAz"].alt.to_string(precision=2)])

if len(t) > 0:
	print()

	st=checkStellariumStatus()
	if st is not True and options.stellarium_tour:
		logger.warning("stellarium is not available. Please check host and port config and make sure the 'Remote Control' plugin in Stellarium is enabled and properly configured. Original exception follows:")
		print(st)

	if options.stellarium_tour and st is True:
		print()
		print("Starting stellarium tour")
		print()
		
		setStellariumTime(str(ephem.julian_date(ephem.Date(stime))))
		
		if platform.system().lower() == "linux":
			tt=tabulate(t, headers=headers).split("\n")
			print("  "+tt[0])
			print("  "+tt[1])
			terminal_menu = TerminalMenu(tt[2:], preview_command=setStellariumFocus2, preview_size=0.1, clear_menu_on_exit = False)
			menu_entry_index = terminal_menu.show()
		else:
			i=1
			print(tabulate(t, headers = headers))
			print()
			print("press ENTER for next object. CTRL-C to exit")
			while True:
				print()
				print("Iteration #%s" % i)
				i+=1
				for visibleObject in visibleObjects:
					print(visibleObject["object"])
					setStellariumFocus(visibleObject["object"])
					input()
	else:
		print(tabulate(t, headers = headers))
else:
	print("no results")

print()

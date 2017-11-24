#!/usr/bin/python
# author: braindead
# requirements: exiftool, python-geopy
# usage: python exif-gps.py [-h] file

import sys, argparse, os.path, socket, random, subprocess
from geopy.geocoders import Nominatim
geolocator = Nominatim()

# Get command arguments
parser = argparse.ArgumentParser(description="Generate random GPS coordinates and write them to a file as EXIF metadata. If you have an internet connection, the geolocation of the coordinates is verified.")
parser.add_argument('file', help="The file you want to update. Exiftool must be able to write EXIF data to that file type.")
args = parser.parse_args()

# Validate file path
if not os.path.isfile(args.file):
        print "Please provide a valid file path."
        sys.exit()

# Test internet connection
def internet(host="8.8.8.8", port=53, timeout=3):
	try:
		socket.setdefaulttimeout(timeout)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
		return True
	except Exception as ex:
		print ex.message
		return False

# Generate a location
geoloc = False
while True:
	# Generate random latitude and longitude
	lat = round(random.uniform(-90,90),6)
	long = round(random.uniform(-180,180),6)
	# Make sure it has a geographic location (unless there's no internet connection)
	if not internet():
		break;
	geoloc = geolocator.reverse(str(lat)+", "+str(long))
	if "error" not in geoloc.raw:
		break;
print "Generated latitude "+str(lat)+" and longitude "+str(long)+"."
if geoloc:
	print "Location is "+geoloc.address+"."

# Remove existing EXIF GPS tags from the file
print "Removing existing GPS tags..."
result = subprocess.Popen('/usr/bin/exiftool -GPS*= '+args.file, shell=True, stdout=subprocess.PIPE).stdout.read()
if result:
	print result

# Write EXIF GPS tags to the file
print "Writing new GPS tags..."
result = subprocess.Popen('/usr/bin/exiftool -GPSLatitude="'+str(lat)+'" -GPSLatitudeRef="'+str(lat)+'" -GPSLongitude="'+str(long)+'" -GPSLongitudeRef="'+str(long)+'" '+args.file, shell=True, stdout=subprocess.PIPE).stdout.read()
if result:
	print result
result = subprocess.Popen('/usr/bin/exiftool -GPS* '+args.file, shell=True, stdout=subprocess.PIPE).stdout.read()
if result:
	print result

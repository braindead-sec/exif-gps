# exif-gps
Generate random GPS coordinates and write them to a file as EXIF metadata. If you have an internet connection, the geolocation of the coordinates is verified.
## Usage
python exif-gps.py [-h] file
## Requirements
exiftool, python-geopy
## Arguments
-h, --help (optional): Show a help message and exit.

file (required): The file you want to update. Exiftool must be able to write EXIF data to that file type.

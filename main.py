from datetime import datetime, timedelta,date
from solar import Sun
import argparse

def get_all_days(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days)]

parser = argparse.ArgumentParser(description="Get whole year sun events in following format: 20261128 08:23 16:35",epilog="example: python3 ./main.py --lat=52.22 --lon=4.54 --utc_offset=1 --year=2026")

# Add arguments
parser.add_argument("-t","--lat", help="Latitude (default=52.24)", default=52.24, type=float,metavar="")
parser.add_argument("-n","--lon", help="Longitude (default=16.56)", default=16.56, type=float,metavar="")
parser.add_argument("-u","--utc_offset", help="UTC offset (default 1)",default=1, type=int,metavar="")
parser.add_argument("-y","--year", help="year (default now)", default=date.today().year , type=int,metavar="")

args = parser.parse_args()

print(f"Latitude={args.lat}, Longitude={args.lon}, UTC offset={args.utc_offset}, Year={args.year}")

days2025 = get_all_days(args.year)

sun = Sun(args.lat, args.lon)

utc = timedelta(hours=args.utc_offset)

for d in days2025:
      sr=sun.get_sunrise_time(d,utc)
      ss=sun.get_sunset_time(d,utc)
      print(f"{d.strftime('%Y%m%d')} {sr.strftime('%H:%M')} {ss.strftime('%H:%M')}")
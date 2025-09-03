from datetime import datetime, timedelta, date, timezone
from solar import Sun
import argparse
from zoneinfo import ZoneInfo, available_timezones


def get_all_days(year):
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days)]


def is_valid_timezone(timezone_str):
    """Check if timezone exists in available timezones"""
    return timezone_str in available_timezones()


parser = argparse.ArgumentParser(
    description="Get whole year sun events in following format: 20261128 08:23 16:35",
    epilog="python3 ./main.py --lat=52.22 --lon=4.54 --utc_offset=1 --year=2026 --sunset_offset=15 --sunrise_offset=15 --timezone=Europe/Amsterdam",
)

# Add arguments
parser.add_argument(
    "--lat", help="Latitude (default=52.24)", default=52.24, type=float, metavar=""
)
parser.add_argument(
    "--lon", help="Longitude (default=16.56)", default=16.56, type=float, metavar=""
)
parser.add_argument(
    "--utc_offset", help="UTC offset (default 1)", default=1, type=int, metavar=""
)
parser.add_argument(
    "--year", help="year (default now)", default=date.today().year, type=int, metavar=""
)
parser.add_argument(
    "--sunset_offset",
    help="sunset offset in minutes (default 0)",
    default=0,
    type=int,
    metavar="",
)
parser.add_argument(
    "--sunrise_offset",
    help="sunrise offset in minutes (default 0)",
    default=0,
    type=int,
    metavar="",
)
parser.add_argument(
    "--timezone",
    help="IANA standard timezone",
    default="Europe/Amsterdam",
    type=str,
    metavar="",
)
parser.add_argument(
    "--no_european_dst",
    help="do not use (European) daylight summertime",
    default=False,
    action="store_true",
)

args = parser.parse_args()

"""Timezone check"""
if not is_valid_timezone(args.timezone):
    print(
        f"\033[91mWrong timezone name `{args.timezone}` enter any listed below!\033[0m"
    )
    for tz in sorted(available_timezones()):
        print(tz)
    print(
        f"\033[91mwrong timezone name `{args.timezone}` enter any listed above!\033[0m"
    )
    exit(1)
tz = ZoneInfo(args.timezone)
""""""

print(
    f"\033[94mLatitude={args.lat}, Longitude={args.lon}, Year={args.year} Timezone={args.timezone}, UTC offset according timezone={tz.utcoffset()}\033[0m"
)

days2025 = get_all_days(args.year)

sun = Sun(args.lat, args.lon)

utc = timedelta(hours=args.utc_offset)
sunrise_offset = timedelta(minutes=args.sunrise_offset)
sunset_offset = timedelta(minutes=args.sunset_offset)
# no_european_dst = args.no_european_dst


for d in days2025:
    sr = sun.get_sunrise_time(d, utc, sunrise_offset, tz)
    ss = sun.get_sunset_time(d, utc, sunset_offset, tz)
    print(f"{d.strftime('%Y%m%d')} {sr.strftime('%H:%M')} {ss.strftime('%H:%M')}")

# with open('sun_events.json', 'w') as f:
#     for d in days2025:
#         sr=sun.get_sunrise_time(d,utc,sunrise_offset)
#         ss=sun.get_sunset_time(d,utc,sunset_offset)
#         # print(f"{d.strftime('%Y%m%d')} {sr.strftime('%H:%M')} {ss.strftime('%H:%M')}")

#         still_true = sr - timedelta(minutes=1)
#         msg = f"""
#             {{
#               "time": "{d.strftime('%Y%m%d')}052900",
#               "on": false,
#               "index": 2
#             }},
#             {{
#               "time": "{d.strftime('%Y%m%d')}053000",
#               "on": true,
#               "index": 2
#             }},
#             {{
#               "time": "{d.strftime('%Y%m%d')}{still_true.strftime('%H%M')}00",
#               "on": true,
#               "index": 2
#             }},
#             {{
#               "time": "{d.strftime('%Y%m%d')}{sr.strftime('%H%M')}00",
#               "on": false,
#               "index": 2
#             }},
#             """
#         f.write(msg)

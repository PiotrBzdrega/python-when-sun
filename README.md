```shell
$ sudo apt install python3.12-venv

$ python3 -m venv .venv

$ source .venv/bin/activate

$ python3 main.py --help

$ python3 ./main.py --lat=52.22 --lon=4.54 --utc_offset=1 --year=2026
Latitude=52.22, Longitude=4.54, UTC offset=1, Year=2026
20260101 08:51 16:39
20260102 08:51 16:40
20260103 08:50 16:42
20260104 08:50 16:43
20260105 08:50 16:44
20260106 08:50 16:45
20260107 08:49 16:46
20260108 08:49 16:48
20260109 08:48 16:49
(...)
```
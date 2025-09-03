import math
from datetime import datetime, timedelta, time, timezone
from zoneinfo import ZoneInfo

# CONSTANT
TO_RAD = math.pi / 180.0
TO_HOUR = 12.0 / math.pi


class Sun:
    """
    Approximated calculation of sunrise and sunset datetimes. Adapted from:
    https://web.archive.org/web/20161202180207/http://williams.best.vwh.net/sunrise_sunset_algorithm.htm
    """

    def __init__(self, lat, lon):
        self._lat = lat
        self._lon = lon

        self.lngHour = self._lon / 15

    def get_sunrise_time(self, at_date, utc_offset, sunrise_offset, tz: ZoneInfo):
        """
        :param at_date: Reference date. datetime.now() if not provided.
        :param time_zone: pytz object with .tzinfo() or None
        :return: sunrise datetime.
        :raises: SunTimeException when there is no sunrise and sunset on given location and date.
        """
        time_delta = self.get_sun_timedelta(at_date, is_rise_time=True)
        time_delta += datetime.combine(at_date, time(tzinfo=timezone.utc))
        time_delta += sunrise_offset
        time_delta = time_delta.astimezone(tz)

        # print(f"utc={dt}\nreg={region}")

        return time_delta

    def get_sunset_time(self, at_date, utc_offset, sunset_offset, tz: ZoneInfo):
        """
        Calculate the sunset time for given date.
        :param at_date: Reference date. datetime.now() if not provided.
        :param time_zone: pytz object with .tzinfo() or None
        :return: sunset datetime.
        :raises: SunTimeException when there is no sunrise and sunset on given location and date.
        """
        time_delta = self.get_sun_timedelta(at_date, is_rise_time=False)
        time_delta += datetime.combine(at_date, time(tzinfo=timezone.utc))
        time_delta += sunset_offset
        time_delta = time_delta.astimezone(tz)

        return time_delta

    def get_sun_timedelta(self, at_date, is_rise_time=True):
        """
        Calculate sunrise or sunset date.
        :param at_date: Reference date
        :param time_zone: pytz object with .tzinfo() or None
        :param is_rise_time: True if you want to calculate sunrise time.
        :param zenith: Sun reference zenith
        :return: timedelta showing hour, minute, and second of sunrise or sunset
        """

        # 1. first get the day of the year
        N = at_date.timetuple().tm_yday

        # 2. convert the longitude to hour value and calculate an approximate time
        if is_rise_time:
            t = N + ((6 - self.lngHour) / 24)
        else:  # sunset
            t = N + ((18 - self.lngHour) / 24)

        # 3. calculate the Sun's mean anomaly
        M = (0.9856 * t) - 3.289

        # 4. calculate the Sun's true longitude
        L = (
            M
            + (1.916 * math.sin(TO_RAD * M))
            + (0.020 * math.sin(TO_RAD * 2 * M))
            + 282.634
        )
        L = self._force_range(L, 360)  # NOTE: L adjusted into the range [0,360)

        # 5a. calculate the Sun's right ascension
        RA = (1 / TO_RAD) * math.atan(0.91764 * math.tan(TO_RAD * L))
        RA = self._force_range(RA, 360)  # NOTE: RA adjusted into the range [0,360)

        # 5b. right ascension value needs to be in the same quadrant as L
        Lquadrant = (math.floor(L / 90)) * 90
        RAquadrant = (math.floor(RA / 90)) * 90
        RA = RA + (Lquadrant - RAquadrant)
        # 5c. right ascension value needs to be converted into hours
        RA = RA / 15

        # 6. calculate the Sun's declination
        sinDec = 0.39782 * math.sin(TO_RAD * L)
        cosDec = math.cos(math.asin(sinDec))

        # 7a. calculate the Sun's local hour angle
        sunLocalAngle = (
            math.cos((math.pi + 108 * math.pi) / 216)
            - (sinDec * math.sin(TO_RAD * self._lat))
        ) / (cosDec * math.cos(TO_RAD * self._lat))
        # sunLocalAngle = (math.cos((math.pi + 108 * math.pi) / 216) - (sinDec * math.sin(TO_RAD*self._lat))) / (cosDec * math.cos(TO_RAD*self._lat))
        if sunLocalAngle > 1:
            return None  # The sun never rises on this location (on the specified date)
        if sunLocalAngle < -1:
            return None  # The sun never sets on this location (on the specified date)

        # 7b. finish calculating H and convert into hours
        if is_rise_time:
            # H = 360 - (1/TO_RAD) * math.acos(sunLocalAngle)
            H = TO_HOUR * (2 * math.pi - math.acos(sunLocalAngle))
        else:  # setting
            # H = (1/TO_RAD) * math.acos(sunLocalAngle)
            H = TO_HOUR * math.acos(sunLocalAngle)

        # 6. calculate local mean time of rising/setting
        T = H + RA - (0.06571 * t) - 6.622
        # 7a. adjust back to UTC
        UT = T - self.lngHour
        # if time_zone:
        #     # 7b. adjust back to local time
        #     UT += time_zone.utcoffset(at_date).total_seconds() / 3600
        # 7c. rounding and impose range bounds
        # UT = round(UT, 2)
        # if is_rise_time:
        #     UT = self._force_range(UT, 24)
        # 8. return timedelta
        # print(f"{UT}")
        UT = self._force_range(UT, 24)
        # print(f"{UT}")

        return timedelta(hours=UT)

    @staticmethod
    def _force_range(v, max):
        # force v to be >= 0 and < max
        if v < 0:
            return v + max
        elif v >= max:
            return v - max
        return v

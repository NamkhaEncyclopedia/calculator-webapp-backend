from datetime import datetime
import logging
import uuid
from decimal import Decimal

import pytz
from timezonefinder import TimezoneFinder

from .models import NamkhaData, CalculationData, TZResponse

log = logging.getLogger("namkha.calculation")
finder = TimezoneFinder()


def get_tz_info(lat: Decimal, lon: Decimal, date: datetime):
    tz = finder.timezone_at(lat=float(lat), lng=float(lon))
    pytz_timezone = pytz.timezone(tz)
    datetime_with_tzinfo = pytz_timezone.localize(date.replace(tzinfo=None))
    offset = int(datetime_with_tzinfo.utcoffset().total_seconds())
    return TZResponse(tz=tz, offset=Decimal(offset/3600))


def calculate(namkha_data: NamkhaData) -> CalculationData:
    log.debug('Start Namkha calculation by %s', namkha_data)
    data = CalculationData(id=str(uuid.uuid4()), created=datetime.now())

    return data

import os
import tempfile
from datetime import datetime, timezone
import logging
import uuid
from decimal import Decimal
from pathlib import Path

import pys
import pytz
from timezonefinder import TimezoneFinder

from .models import NamkhaData, CalculationData, TZResponse

log = logging.getLogger("namkha.calculation")
finder = TimezoneFinder()

ENV_NAMKHA_PATH = 'NAMKHA_PATH'


def _get_namkha_path():
    return os.environ.get(ENV_NAMKHA_PATH, tempfile.gettempdir())


def _get_storage():
    p = Path(_get_namkha_path())
    storage = pys.file_storage(p)
    log.debug('Initialize file storage at %s', p)
    return storage


def get_tz_info(lat: Decimal, lon: Decimal, date: datetime):
    tz = finder.timezone_at(lat=float(lat), lng=float(lon))
    pytz_timezone = pytz.timezone(tz)
    datetime_with_tzinfo = pytz_timezone.localize(date.replace(tzinfo=None))
    offset = int(datetime_with_tzinfo.utcoffset().total_seconds())
    return TZResponse(tz=tz, offset=Decimal(offset/3600))


def calculate(namkha_data: NamkhaData) -> CalculationData:
    storage = _get_storage()
    while True:
        # Find unused ID
        _id = str(uuid.uuid4())
        calc = storage.load(CalculationData, _id)
        if not calc:
            break

    calc = CalculationData(
        id=_id,
        namkha_data=namkha_data,
        created=datetime.now(timezone.utc).astimezone()
    )
    storage.save(calc)

    # todo: run Namkha calculations

    return calc


def get_calculation_data(calc_id: str) -> CalculationData:
    storage = _get_storage()
    calc = storage.load(CalculationData, calc_id)
    return calc

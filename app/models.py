import enum
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

import pys


class Method(str, Enum):
    classic = 'classic'
    rinpoche = 'rinpoche'


class Fraction(str, Enum):
    year = 'year'
    month = 'month'
    day = 'day'
    hour = 'hour'


class Gender(str, Enum):
    male = 'male'
    female = 'female'


@dataclass
class Location:
    __slots__ = ('lat', 'lon')
    lat: Decimal
    lon: Decimal


@pys.saveable
@dataclass
class NamkhaData:
    fraction: Fraction
    name: Optional[str]
    gender: Gender
    datetime: datetime
    location: Location
    method: Method = Method.rinpoche


class CalculationStatus(str, enum.Enum):
    new = 'new'
    in_progress = 'in progress'
    done = 'done'
    failed = 'failed'


@dataclass
class CalculationResult:
    page1: str
    page2: str
    pdf: str


@pys.saveable
@dataclass
class CalculationData:
    id: str
    created: datetime
    namkha_data: NamkhaData
    status: CalculationStatus = CalculationStatus.new
    finished: Optional[datetime] = None
    result: Optional[CalculationResult] = None


@dataclass
class TZResponse:
    tz: str
    offset: Decimal

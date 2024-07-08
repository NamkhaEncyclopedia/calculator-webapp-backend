import enum
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class Method(Enum):
    classic = 'classic'
    rinpoche = 'rinpoche'


class Fraction(Enum):
    year = 'year'
    month = 'month'
    day = 'day'
    hour = 'hour'


class Gender(Enum):
    male = 'male'
    female = 'female'


@dataclass
class Location:
    __slots__ = ('lat', 'lon')
    lat: Decimal
    lon: Decimal


@dataclass
class NamkhaData:
    fraction: Fraction
    name: Optional[str]
    gender: Gender
    datetime: datetime
    location: Location
    method: Method = Method.rinpoche


class CalculationStatus(enum.Enum):
    new = 'new'
    in_progress = 'in progress'
    done = 'done'
    failed = 'failed'


@dataclass
class CalculationResult:
    page1: str
    page2: str
    pdf: str


@dataclass
class CalculationData:
    id: str
    created: datetime
    status: CalculationStatus = CalculationStatus.new
    finished: Optional[datetime] = None
    result: Optional[CalculationResult] = None


@dataclass
class TZResponse:
    tz: str
    offset: Decimal

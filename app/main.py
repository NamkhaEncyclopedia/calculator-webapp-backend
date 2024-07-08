import logging
import traceback
from datetime import datetime
from decimal import Decimal
from logging.config import dictConfig
from pathlib import Path

import yaml
from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from . import namkha
from .models import NamkhaData

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

dictConfig(yaml.safe_load((Path(__file__).parent / 'logging.yaml').read_text()))
log = logging.getLogger("namkha.api")


@app.exception_handler(Exception)
async def uvicorn_exception_handler(request: Request, exc: Exception):
    format_exc = traceback.format_exc()
    log.exception('Request %s is failed', request, exc_info=True)
    return Response(media_type='application/json',
                    content=format_exc,
                    status_code=status.HTTP_400_BAD_REQUEST)


@app.get('/status', response_class=Response, status_code=status.HTTP_204_NO_CONTENT,
         summary='Check status of API backend', description='Returns HTTP 204 if all is OK')
async def check_status():
    pass


@app.get('/tz', summary='Get time zone by lat, lon and date')
async def tz(lat: Decimal, lon: Decimal, date: datetime):
    tz_response = namkha.get_tz_info(lat, lon, date)
    log.debug('/tz (lat=%s, lon=%s, date=%s) = %s', lat, lon, date, tz_response)
    return tz_response


@app.post('/calculate', summary='Request Namkha calculation')
async def calculate(namkha_data: NamkhaData):
    calc = namkha.calculate(namkha_data)
    log.debug('Calculate namkha (%s) -> %s', namkha_data, calc)
    return calc


@app.get('/calculate/{calculation_id}', summary='Get Namkha calculations results')
async def calculate(calculation_id: str):
    calc = namkha.get_calculation_data(calculation_id)
    if not calc:
        log.debug('Calculation id=%s is not found', calculation_id)
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    log.debug('Get calculation status by  id=%s: %s', calculation_id, calc)
    return calc

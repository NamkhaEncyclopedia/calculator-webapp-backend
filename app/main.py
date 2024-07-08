import traceback
import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.models import NamkhaData, CalculationData

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def uvicorn_exception_handler(request: Request, exc: Exception):
    format_exc = traceback.format_exc()
    return Response(media_type='application/json',
                    content=format_exc,
                    status_code=status.HTTP_400_BAD_REQUEST)


@app.get('/status', response_class=Response, status_code=status.HTTP_204_NO_CONTENT,
         summary='Check status of API backend', description='Returns HTTP 204 if all is OK')
async def check_status():
    pass


@app.get('/tz', summary='Get time zone by lat, lon and date')
async def tz(lat: Decimal, lon: Decimal, date: Optional[datetime]=None):
    return 'UTC'


@app.post('/calculate', summary='Request Namkha calculation')
async def calculate(namkha_data: NamkhaData):
    print(f'Calculate namkha: {namkha_data}')
    return CalculationData(id=str(uuid.uuid4()), created=datetime.now())


@app.get('/calculate/{id}', summary='Get Namkha calculations results')
async def calculate(id: str):
    return CalculationData(id=id, created=datetime.now())

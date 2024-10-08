from fastapi.responses import JSONResponse
from fastapi import Request, APIRouter
from data import get_data, post_data
from schemas import FlightDataRow


router = APIRouter()



@router.get("/flightdata", response_class=JSONResponse)
async def get_flight_data(request: Request) -> list[FlightDataRow]:
    data = await get_data()
    return data


@router.post("/flightdata", response_class=JSONResponse)
async def post_flight_data(request: list[FlightDataRow]) -> dict:
    await post_data(request)
    return {"status" : "ok"}
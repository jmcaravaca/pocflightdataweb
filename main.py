from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import router as brouter
from frontend import router as frouter



app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5555",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(brouter)
app.include_router(frouter)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5555)
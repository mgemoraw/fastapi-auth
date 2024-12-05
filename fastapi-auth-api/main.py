from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import routes



app = FastAPI()



origins = [
    "http://localhost:3000", # agust the port if your frontend runs on different port
    "https://yourfrontenddomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, #Allows all origins from the list
    allow_credentials=True,
    allow_methods=['*'], # Allows all methods
    allow_headers = ['*'], # Allows all headers
)

app.include_router(routes.router)

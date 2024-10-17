from typing import Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None, min_length=3
    ),
):
    results = {"q" : q}
    return results
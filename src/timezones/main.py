from fastapi import FastAPI

from timezones.common import WORKING_DIR

app = FastAPI()


@app.get("/")
def read_root():
    """
    This is awesome
    """
    return {"Hello": "World"}

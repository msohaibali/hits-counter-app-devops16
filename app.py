import time
from fastapi import FastAPI
import uvicorn
import redis

cache = redis.Redis(host="redis", port=6379, db=0)
app = FastAPI()


def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr("hits")
        except redis.exceptions.ConnectionError as e:
            if retries == 0:
                raise e
            retries -= 1
            time.sleep(0.5)


@app.get("/")
async def index():
    return {"version": "1.0.0"}


@app.get("/hits")
async def hit():
    count = get_hit_count()
    return f"I have been hit {count} times."


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

import os
from flask import Flask
import redis

app = Flask(__name__)

# Redis host is read from REDIS_HOST (defaults to localhost for local development)
r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=6379,
    decode_responses=True,
)

@app.route("/")
def index():
    n = r.incr("compteur")
    return f"Cette page a été vue {n} fois\n"

@app.route("/health")
def health():
    return "ok\n"
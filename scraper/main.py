from flask import Flask, request
import scraper.helpers.constants as constants
from scraper.helpers.response_wrapper import wrap_response

app = Flask(__name__)

@app.route('/')
def index():
    return wrap_response(200, False, f"Python scraper running at {request.remote_addr}")
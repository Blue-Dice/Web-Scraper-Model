from flask import Flask, request
import logging
from flask_wtf.csrf import CSRFProtect
from decouple import config
from scraper.helpers.response_wrapper import wrap_response
from scraper.helpers.driver_operations import driver_controller

app = Flask(__name__)
app.secret_key = config('SECRET_KEY')
app.config['WTF_CSRF_ENABLED'] = (config('CSRF_ENABLED') == 'True')
csrf = CSRFProtect(app)

# Create log file
if config('CREATE_RECORD_LOG') == 'True':
    logging.basicConfig(filename='record.log', level=logging.DEBUG)

driver_instance = driver_controller()
@app.route('/')
def index():
    return wrap_response(200, False, f"Python scraper running at {request.remote_addr}")

@app.route('/driver', methods=['GET', 'POST'])
def driver():
    driver = driver_instance.get_driver
    driver.get("https://knowledge.broadcom.com/external/article/196472/webdriver-selenium-server-ips.html")
    return wrap_response(200, False, f"Python scraper running at {request.remote_addr}")
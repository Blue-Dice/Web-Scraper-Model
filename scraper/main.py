from flask import Flask, request
import logging
from flask_wtf.csrf import CSRFProtect
from decouple import config
from scraper.helpers.response_wrapper import wrap_response
from scraper.helpers.driver_controller import DriverController

app = Flask(__name__)
app.secret_key = config('SECRET_KEY')
app.config['WTF_CSRF_ENABLED'] = (config('CSRF_ENABLED') == 'True')
csrf = CSRFProtect(app)

# Create log file
if config('CREATE_RECORD_LOG') == 'True':
    logging.basicConfig(filename='record.log', level=logging.DEBUG)

driver_instance = DriverController()
@app.route('/')
def index():
    return wrap_response(200, False, f"Python scraper running at {request.remote_addr}")

@app.route('/driver', methods=['GET', 'POST'])
def driver():
    driver = driver_instance.get_driver(security='undetected', multi_driver=True)
    # driver.get('https://api.ipify.org/')
    # driver.get('https://nowsecure.nl')
    # driver.get('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
    driver.get('https://webscraping.pro/wp-content/uploads/2021/02/testresult2.html')
    # driver.save_screenshot("zhello.png")
    return wrap_response(200, False, f"Python scraper running at {request.remote_addr}")
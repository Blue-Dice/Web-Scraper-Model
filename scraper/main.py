from flask import Flask, request
import time
import logging
from flask_wtf.csrf import CSRFProtect
from decouple import config
from scraper.helpers.response_wrapper import wrap_response
from scraper.helpers.driver_controller import DriverController
from selenium.webdriver.common.by import By

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
    return wrap_response(200, False, f'Python scraper running at {request.remote_addr}')

@app.route('/driver/ip', methods=['GET', 'POST'])
def driver_ip():
    try:
        example_driver = DriverController()
        driver = example_driver.get_driver(silent=True)
        driver.get('https://api.ipify.org/')
        data = {
            'driver ip': driver.find_element(By.TAG_NAME,'body').text
        }
        example_driver.dispose_driver()
        return wrap_response(200, False, 'External IP of the driver successfully located', data)
    except Exception :
        return wrap_response(500, True, 'Server Error')

@app.route('/driver/security', methods=['GET', 'POST'])
def driver_security():
    try:
        example_driver = DriverController()
        if '_security' in request.args:
            security = request.args.get('_security')
            security = None if security == "none" else security
        else:
            security = 'manual'
        if '_silent' in request.args:
            silent = request.args.get('_silent')
            silent = True if silent == "true" else False
        else:
            silent = False
        driver = example_driver.get_driver(security=security, silent=silent)
        # For checking cloudfare bypass
        # driver.get('https://nowsecure.nl')
        
        # For checking driver features that include automation features
        # Basic security log
        driver.get('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
        
        # Advanced security log
        # driver.get('https://webscraping.pro/wp-content/uploads/2021/02/testresult2.html')
        
        # To check result in headless mode
        # if silent:
        # driver.save_screenshot('zhello.png')
        time.sleep(10)
        example_driver.dispose_driver()
        return wrap_response(200, False)
    except Exception:
        return wrap_response(500, True, 'Server Error')
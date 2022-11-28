from flask import Flask
import logging
from flask_wtf.csrf import CSRFProtect
from decouple import config

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static',
)
app.secret_key = config('SECRET_KEY')
app.config['WTF_CSRF_ENABLED'] = (config('CSRF_ENABLED') == 'True')
csrf = CSRFProtect(app)

# Create log file
if config('CREATE_RECORD_LOG') == 'True':
    logging.basicConfig(filename='record.log', level=logging.DEBUG)
from scraper.main import app
from decouple import config

port = config('PORT')
host = config('HOST')
debug = config('DEBUG_MODE') == "True"

if __name__ == "__main__":
    app.run(debug=debug, host=host, port=port)
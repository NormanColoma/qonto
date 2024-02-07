import logging
from flask import Flask
from infraestructure.config.config import Config
from infraestructure.rest.http.account_controller import account_controller
from infraestructure.rest.http.error_handler import handle_exception

app = Flask(__name__)
app.register_blueprint(account_controller)
app.register_error_handler(Exception, handle_exception)

logging.basicConfig(level=logging.INFO, format='{"dateTime": "%(asctime)s", "level": "info", "message": "%(message)s"}',
                    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.APP_PORT)


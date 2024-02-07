import os


class Config(object):
    MYSQL_URI = os.getenv("MYSQL_URI")
    APP_PORT = os.getenv('APP_PORT') or 5001
    RABBITMQ_URI = os.getenv('RABBITMQ_URI')


class RunConfig(Config):
    pass


class TestConfig(Config):
    MONGO_URI = 'Fake_Uri'
    RABBITMQ_URI = 'Fake_Uri'


app_config = {
    'test': TestConfig,
    'run': RunConfig,
}

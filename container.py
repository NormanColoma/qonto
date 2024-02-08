import os

import pika
import pinject
import sqlalchemy

from application.process_transfers.process_transfers import ProcessTransfers
from infraestructure.bus.event.rabbit_handler import RabbitMQHandler
from infraestructure.bus.event.rabbitmq_event_bus import RabbitMqEventBus
from infraestructure.config.config import app_config
from infraestructure.persistence.mysql.database_handler import SqlAlchemyHandler
from infraestructure.persistence.mysql.mysql_account_parser import MySqlAccountParser
from infraestructure.persistence.mysql.mysql_account_repository import MysqlAccountRepository


class DatabaseHandlerInstance(pinject.BindingSpec):
    def provide_database_handler(self):
        return obj_graph.provide(SqlAlchemyHandler)


class Config(pinject.BindingSpec):
    def provide_config(self):
        env = os.getenv('ENV') or 'run'
        return app_config[env]


class RabbitClient(pinject.BindingSpec):
    def provide_rabbit_client(self):
        return pika

class SqlClient(pinject.BindingSpec):
    def provide_sql_client(self):
        return sqlalchemy

class RabbitHandler(pinject.BindingSpec):
    def provide_rabbit_handler(self):
        return obj_graph.provide(RabbitMQHandler)


class EventBusService(pinject.BindingSpec):
    def provide_event_bus(self):
        return obj_graph.provide(RabbitMqEventBus)


class ProcessTransfersAppService(pinject.BindingSpec):
    def provide_process_transfers(self):
        return obj_graph.provide(ProcessTransfers)


class AccountRepository(pinject.BindingSpec):
    def provide_account_repository(self):
        return obj_graph.provide(MysqlAccountRepository)


class AccountParser(pinject.BindingSpec):
    def provide_account_parser(self):
        return obj_graph.provide(MySqlAccountParser)


obj_graph = pinject.new_object_graph(modules=None,
                                     binding_specs=[DatabaseHandlerInstance(), Config(), EventBusService(),
                                                    ProcessTransfersAppService(), AccountRepository(), RabbitHandler(),
                                                    RabbitClient(), AccountParser(), SqlClient()])

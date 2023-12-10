from .client_server_repo import ClientServerAPI
from config import config

client_server_api = ClientServerAPI(host=config.MKD_CLIENT_HOST)
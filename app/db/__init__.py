import motor.motor_asyncio
import sys

from ..utils import server_path

client = motor.motor_asyncio.AsyncIOMotorClient(server_path, serverSelectionTimeoutMS=5000)

"""
def check_connection(_client):
    try:
        print("*********************************************")
        print(_client.server_info())
    except Exception:
        print("Unable to connect to the server.")
        sys.exit(1)
"""
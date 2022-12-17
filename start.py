"""
Start server.py and client.py
"""
import subprocess
import threading
import time

class Child():
    """ Child process class """
    def __init__(self, waitsec):
        server = threading.Thread(target=self._server)
        server.start()
        time.sleep(waitsec)
        client = threading.Thread(target=self._client)
        client.start()

    def _server(self):
        process = subprocess.Popen(["python3", "./server.py"])
        while True:
            _ = process.communicate()
            process = subprocess.Popen(["python3", "./server.py"])

    def _client(self):
        process = subprocess.Popen(["python3", "./client.py"])
        while True:
            _ = process.communicate()
            process = subprocess.Popen(["python3", "./client.py"])

if __name__ == "__main__":
    Child(1)

# Copyright 2025 Rina
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import threading
import signal
import socket
import sys

class Request(object):
    """
    Represents an HTTP request.

    Attributes:
        request_data (bytes): The raw data of the HTTP request.
    """
    def __init__(self, request_data: bytes):
        pass
    
class Response(object):
    """
    Response class for handling and creating HTTP responses.
    Methods:
        __init__(response_data: bytes):
            Initializes a Response object with the given response data.
        make_response(data: str | bytes):
            Creates a response object from the provided data, which can be either a string or bytes.
        make_internal_error_response(message: str = "Internal Server Error"):
            Generates a response object representing an internal server error with an optional custom message.
    """
    def __init__(self, response_data: bytes):
        pass
    
    def make_response(data: str | bytes):
        pass
    
    def make_internal_error_response(message: str = "Internal Server Error"):
        pass

class Tenkyuu(object):
    """
    Tenkyuu is a proxy server class that provides functionality to run and manage a proxy server.
    Methods:
        __init__():
            Initializes the Tenkyuu instance.
        shutdown(signum: int, frame: FrameType) -> None:
            Gracefully shuts down the proxy server. This method is typically triggered by a signal
            and is responsible for closing the proxy server and exiting the program.
        run(handler: callable[[Request], Response | str | bytes | None], host: str = "127.0.0.1", port: int = 80) -> None:
            Starts the proxy server and listens for incoming client connections.
    """        
    def __init__(self):
        pass
    
    def shutdown(self, signum, frame):
        """
        Gracefully shuts down the proxy server.
        Normally, this method is triggered by a signal and is responsible for closing the
        proxy server and exiting the program.
        Args:
            signum (int): The signal number that triggered the shutdown.
            frame (FrameType): The current stack frame (unused in this method).
        Returns:
            None
        """
        
        self.proxy_server.close()
        sys.exit(signum)
        
    def run(self, handler: callable[[Request], Response | str | bytes | None], host: str = "127.0.0.1", port: int = 80) -> None:
        """
        Run the proxy server.
        Args:
            handler (callable): The function to handle incoming client connections.
            host (str): The host to bind the proxy server to.
            port (int): The port to bind the proxy server to.
        Returns:
            None
        """
        signal.signal(signal.SIGINT, self.shutdown)
        
        self.proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        logging.info(f"Starting proxy server at {host}:{port}")
        
        while True:
            client_socket, addr = self.proxy_server.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()
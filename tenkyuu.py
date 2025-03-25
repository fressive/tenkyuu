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

from typing import Union

class Request(object):
    """
    Represents an HTTP request.

    Attributes:
        request_data (bytes): The raw data of the HTTP request.
    """
    def __init__(self, request_data: bytes):
        lines = request_data.splitlines()
        
        self.method, self.path, self.protocol = [i.decode() for i in lines[0].split()]
        
        split_index = lines.index(b"")
        self.headers = self._parse_headers(lines[1:split_index])
        
        body_index = request_data.find(b"\r\n\r\n") + 4
        self.body = request_data[body_index:]
    
    def _parse_headers(self, lines: list) -> None:
        """
        Parses the headers from the request data.
        Args:
            lines (list): The lines of the request data.
        Returns:
            None
        """
        
        headers = {}
        for line in lines:
            key, value = [i.decode() for i in line.split(b": ", 1)]
            
            # Convert the key to lowercase
            key = key.lower()
            
            headers[key] = value
        
        return headers
    
    def header(self, key: str) -> str:
        """
        Returns the value of the header with the given key.
        Args:
            key (str): The key of the header.
        Returns:
            str: The value of the header.
        """
        
        return self.headers[key.lower()]
    
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
        lines = response_data.splitlines()
        
        
    
    def make_response(data: Union[str, bytes]):
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
    def __init__(self, handler: callable):
        self.handler = handler
    
    def handle_client(self, client_socket: socket.socket) -> None:
        """
        Handles an incoming client connection.
        Args:
            client_socket (socket.socket): The client socket connection.
        Returns:
            None
        """

        request_data = client_socket.recv(4096)
        request = Request(request_data)
        response = self.handler(request)
        
        if response is None:
            response = Response.make_internal_error_response()
        elif isinstance(response, str) or isinstance(response, bytes):
            response = Response.make_response(response)
        
        if not isinstance(response, Response):
            # Invalid response type
            raise ValueError("Invalid response type")
        
        client_socket.sendall(response.response_data)
        client_socket.close()
        
    def shutdown(self, signum: int = 0, frame = None) -> None:
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
        
    def run(
        self,
        host: str = "127.0.0.1", 
        port: int = 80
    ) -> None:
        """
        Run the proxy server.
        Args:
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
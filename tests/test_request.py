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

import pytest

from tenkyuu import Request

class TestRequest():
    def test_parser_firstline(self):
        request_data = b"GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: curl/7.68.0\r\nAccept: */*\r\n\r\n"
        request = Request(request_data)
        
        assert request.method == "GET"
        assert request.path == "/"
        assert request.protocol == "HTTP/1.1"
    
    def test_parser_headers(self):
        request_data = b"GET / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: curl/7.68.0\r\nAccept: */*\r\n\r\n"
        request = Request(request_data)
        
        assert request.header("Host") == "localhost"
        assert request.header("User-Agent") == "curl/7.68.0"
        assert request.header("Accept") == "*/*"
        
    def test_parser_body(self):
        request_data = b"POST / HTTP/1.1\r\nHost: localhost\r\nUser-Agent: curl/7.68.0\r\nAccept: */*\r\n\r\nHello, world!"
        request = Request(request_data)
        
        assert request.body == b"Hello, world!"
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

from tenkyuu import Tenkyuu, Response
import requests

app = Tenkyuu(verbose = True)

def ssrf_proxy(req):
    # The req param is an object that contains the information of HTTP Request(s)

    # The req.gopherize() function will convert HTTP Request Packet 
    # to `gopher://...` protocol automatically
    gopherized_url = req.gopherize() 
    
    # Assume that the server has a ssrf vulunerale entrance
    # and supports gopher:// protocol, responsing with data 
    # in JSON format
    resp = requests.get("http://vulunerable.com/ssrf.php", params = {
        "url": gopherized_url
    }).json()

    if resp["status"] != "OK":
        return Response.make_internal_error_response(resp["message"])

    return resp["data"]

if __name__ == "__main__":
    app.run(
        handler = ssrf_proxy,
        host = "127.0.0.1", 
        port = 8088
    )
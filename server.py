import socketserver
import web



PORT = 8000

socketserver.TCPServer.allow_reuse_address = True

Handler = web.testHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)


print("serving at port", PORT)

httpd.serve_forever()

#Copyright [2017] [Jorge Tarancon Rey]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

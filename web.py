import http.client
import http.server
import json


class OpenFDAClient():
    OPENFDA_API_URL = 'api.fda.gov'
    OPENFDA_API_EVENT = '/drug/event.json'

    def get_medicinalproduct(self,company):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET', self.OPENFDA_API_EVENT + '?search=companynumb:'+company+'&limit=10')

        r1=conn.getresponse()

        print (r1.status,r1.reason)

        data1 = r1.read()

        data = data1.decode('utf8')
        events = json.loads(data)
        return events

    def get_med(self,drug):
        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET', self.OPENFDA_API_EVENT + '?search=patient.drug.medicinalproduct:'+drug+'&limit=10')

        r1=conn.getresponse()

        print (r1.status,r1.reason)

        data1 = r1.read()

        data = data1.decode('utf8')
        events = json.loads(data)
        return events

    def get_events(self,limit):


        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET', self.OPENFDA_API_EVENT + '?limit='+ limit)

        r1=conn.getresponse()

        print (r1.status,r1.reason)

        data1 = r1.read()

        data = data1.decode('utf8')
        events = json.loads(data)
        return events

class OpenFDAParser():
    def get_Gender(self,events):
        gender=[]
        for event in events['results']:
            gender+=[event['patient']['patientsex']]
        return gender

    def get_drug(self,events):
        medicamentos=[]
        for event in events['results']:
            medicamentos+=[event['patient']['drug'][0]['medicinalproduct']]
        return (medicamentos)

    def get_company_numb(self,events):
        com_numb=[]
        for event in events['results']:
            com_numb+=[event['companynumb']]
        return com_numb

class OpenFDAHTML():
    def get_main_page(self):
        html='''
        <html>
            <head>
            <title>BUSCADOR DE SUCESOS MEDICOS</title>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method='get' action='listDrugs'>
                    <input type='submit' value='List Drugs'></input>
                    Limit:<input type='text' name='limit'></input>

                </form>
                <form method='get' action='searchDrug'>
                    <input type='text' name='drug'> </input>
                    <input type='submit' value='Search Drug'></input>
                </form>

                <form method='get' action='listCompanies'>
                    <input type='submit' value='List companies'></input>
                    Limit:<input type='text' name='limit'></input>
                </form>

                <form method='get' action='searchCompany'>
                    <input type='text' name='company'> </input>
                    <input type='submit' value='Search company'></input>
                </form>

                <form method='get' action='listGender'>
                    <input type='submit' value='List Gender'></input>
                    Limit:<input type='text' name='limit'></input>
                </form>


            </body>
        </html>
        '''
        return html

    def drug_page(self,medicamentos):
        s=''
        for drug in medicamentos:
            s+= '<li>'+drug+'</li>'
        html= '''
        <html>
            <head></head>
                <body>
                    <ol>
                        %s
                    </ol>
                </body>
        </html>
        '''%(s)
        return html

    def errorhtml(self):
        html='''
        <html>
            <head></head>
            <body><h1>ERROR 404 FILE NOT FOUND</h1></body>
        </html>
        '''
        return html

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        client = OpenFDAClient()
        HTML = OpenFDAHTML()
        Parser = OpenFDAParser()

        if self.path == '/':
            html = HTML.get_main_page()
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(html,'utf8'))

        elif 'listDrugs' in self.path:
            limit = self.path.split('=')[1]
            events = client.get_events(limit)
            medicamentos = Parser.get_drug(events)
            html = HTML.drug_page(medicamentos)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(html,'utf8'))


        elif 'searchDrug' in self.path:
            drug = self.path.split('=')[1]
            events = client.get_med(drug)
            com_num = Parser.get_company_numb(events)
            html = HTML.drug_page(com_num)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(html,'utf8'))


        elif 'listCompanies' in self.path:
            limit = self.path.split('=')[1]
            events = client.get_events(limit)
            company = Parser.get_company_numb(events)
            html = HTML.drug_page(company)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(html,'utf8'))

        elif 'searchCompany' in self.path:
            company = self.path.split('=')[1]
            events = client.get_medicinalproduct(company)
            med = Parser.get_drug(events)
            html = HTML.drug_page(med)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(html,'utf8'))

        elif 'listGender' in self.path:
            limit = self.path.split('=')[1]
            events = client.get_events(limit)
            gend = Parser.get_Gender(events)
            html = HTML.drug_page(gend)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(html,'utf8'))

        elif 'secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate','basic Realm=simple')
            self.end_headers()

        elif 'redirect' in self.path:
            self.send_response(302)
            self.send_header('location','http://localhost:8000')
            self.end_headers()


        else:
            html = HTML.errorhtml()
            self.send_response(404)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes(html,'utf8'))



        return



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

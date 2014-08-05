import httplib2
import time
from SignatureBuilder import SignatureBuilder
from json import dumps

class UpdateTarget:

    accessKey = "[ server access key ]";
    secretKey = "[ server secret key ]";

    targetId = "[ target id ]";

    headers = {}
    requestBody = {}

    url = "https://vws.vuforia.com"
    path = "/targets/"
    method = "PUT"

    def updateTarget(self):
        h = httplib2.Http('.cache')
        self.setRequestBody()
        self.setHeaders(self.headers)

        body = str(self.requestBody).replace(' ', '').replace('\'', '"').lower()

        response, content = h.request(self.url + self.path + self.targetId,
                                    self.method,
                                    body=body,
                                    headers=self.headers)
        print response
        print content

    def setRequestBody(self):
        self.requestBody["active_flag"] = True

    def setHeaders(self, headers):
        sb = SignatureBuilder()
        headers.update({'Date' : time.strftime('%a, %d %b %Y %H:%M:%S GMT',
                                 time.gmtime(time.time()))})
        headers.update({'Content-Type' : "application/json"})
        headers.update({'Authorization' : "VWS " +
                         self.accessKey + ":" +
                         sb.tmsSignature(headers,
                                         self.method,
                                         self.requestBody,
                                         self.path + self.targetId,
                                         self.secretKey)})

g = UpdateTarget()
g.updateTarget()


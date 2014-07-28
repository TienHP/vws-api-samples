import httplib2
import time
from SignatureBuilder import SignatureBuilder

class GetTarget:

    accessKey = "[ server access key ]";
    secretKey = "[ server secret key ]";

    targetId = "[ target id ]";

    headers = {}

    url = "https://vws.vuforia.com"
    path = "/targets/"
    method = "GET"

    def getTarget(self):
        h = httplib2.Http('.cache')
        self.setHeaders(self.headers)

        response, content = h.request(self.url + self.path + self.targetId,
                                    self.method,
                                    headers=self.headers)
        print response
        print content

    def setHeaders(self, headers):
        sb = SignatureBuilder()
        headers.update({'Date' : time.strftime('%a, %d %b %Y %H:%M:%S GMT',
                                 time.gmtime(time.time()))})
        headers.update({'Authorization' : "VWS " +
                         self.accessKey + ":" +
                         sb.tmsSignature(headers,
                                         self.method,
                                         self.path + self.targetId,
                                         self.secretKey)})

g = GetTarget()
g.getTarget()


import httplib2
import time
from SignatureBuilder import SignatureBuilder

class GetSummary:
    accessKey = "[ server access key ]";
    secretKey = "[ server secret key ]";

    headers = {}

    url = "https://vws.vuforia.com"
    path = "/summary"
    method = "GET"

    def getSummary(self):
        h = httplib2.Http('.cache')
        self.setHeaders(self.headers)

        response, content = h.request(self.url + self.path,
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
                                         None,
                                         self.path,
                                         self.secretKey)})

if __name__ == "__main__":
    g = GetSummary()
    g.getSummary()


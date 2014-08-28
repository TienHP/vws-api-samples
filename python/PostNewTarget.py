import httplib2
import time
from SignatureBuilder import SignatureBuilder
from TargetStatusListener import TargetStatusListener
from TargetStatusPoller import TargetStatusPoller
import json

class PostNewTarget(TargetStatusListener):

    accessKey = "[ server access key ]";
    secretKey = "[ server secret key ]";

    targetName = "[ target name ]";

    imageLocation = "[ image path ]";

    requestBody = {}

    url = "https://vws.vuforia.com"
    path = "/targets"
    method = "POST"

    pollingIntervalMinutes = 1 * 60
    targetStatusPoller = None

    def postTarget(self):
        h = httplib2.Http('.cache')
        headers = {}
        self.setRequestBody()
        self.setHeaders(headers)

        body = str(self.requestBody)\
                .replace(' ', '')\
                .replace('\'', '"')\
                .replace('\\n', '')

        response, content = h.request(self.url + self.path,
                                    self.method,
                                    body=body,
                                    headers=headers)

        print response
        print content
        jobj = json.loads(content)

        uniqueTargetId = jobj["target_id"] if jobj.has_key("target_id") else ""
        print "Created target with id: " + uniqueTargetId

        return uniqueTargetId

    def setRequestBody(self):
        try:
            image = open(self.imageLocation).read()
        except Exception as e:
            print e
            return None

        self.requestBody["name"] = self.targetName
        self.requestBody["width"] = 320
        self.requestBody["image"] = image.encode('base64')[:-1]
        self.requestBody["active_flag"] = 1
        self.requestBody["application_metadata"] = str(
                        bytearray("Vuforia test metadata".encode('base64')
                    ).decode('utf-8')
                )[:-1]

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
                                         self.path,
                                         self.secretKey)})

    def postTargetThenPollStatus(self):
        createdTargetId = self.postTarget()
        if createdTargetId != None and createdTargetId != '':
            self.targetStatusPoller = TargetStatusPoller(
                    self.pollingIntervalMinutes,
                    createdTargetId,
                    self.accessKey,
                    self.secretKey,
                    self)
            self.targetStatusPoller.startPolling()

    def OnTargetStatusUpdate(self, target_state):
        if target_state.hasState:

            status = target_state.m_status

            if target_state.m_activeFlag == True and\
               status.lower() == "success":

                self.targetStatusPoller.stopPolling()

                try:
                    print "Target is now in 'success' status"
                except Exception as e:
                    print "Error ontargetstatusupdate: " + str(e)

if __name__ == "__main__":
    g = PostNewTarget()
    g.postTargetThenPollStatus()


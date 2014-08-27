import httplib2
import time
from SignatureBuilder import SignatureBuilder
from TargetStatusListener import TargetStatusListener
from TargetStatusPoller import TargetStatusPoller
from json import dumps

class DeleteTarget(TargetStatusListener):

    accessKey = "[ server access key ]";
    secretKey = "[ server secret key ]";

    targetId = "[ target id ]";

    requestBody = {}

    url = "https://vws.vuforia.com"
    path = "/targets/"
    updateMethod = "PUT"
    deleteMethod = "DELETE"

    pollingIntervalMinutes = 60
    targetStatusPoller = None

    def deleteTarget(self):
        h = httplib2.Http('.cache')
        headers = {}
        self.setHeaders(headers, self.deleteMethod)

        response, content = h.request(self.url + self.path + self.targetId,
                                    self.deleteMethod,
                                    headers=headers)
        print response
        print content

    def updateTargetActivation(self, activeFlag):
        h = httplib2.Http('.cache')
        self.setRequestBody(activeFlag)
        headers = {}
        self.setHeaders(headers, self.updateMethod)

        body = str(self.requestBody).replace(' ', '').replace('\'', '"').lower()

        response, content = h.request(self.url + self.path + self.targetId,
                                    self.updateMethod,
                                    body=body,
                                    headers=headers)
        print response
        print content

    def setRequestBody(self, activeFlag):
        self.requestBody["active_flag"] = activeFlag

    def setHeaders(self, headers, method):
        sb = SignatureBuilder()
        headers.update({'Date' : time.strftime('%a, %d %b %Y %H:%M:%S GMT',
                                 time.gmtime(time.time()))})

        if method == 'PUT':
            headers.update({'Content-Type' : "application/json"})

        headers.update({'Authorization' : "VWS " +
                         self.accessKey + ":" +
                         sb.tmsSignature(headers,
                                         method,
                                         self.requestBody if method == 'PUT' else None,
                                         self.path + self.targetId,
                                         self.secretKey)})

    def deactivateThenDeleteTarget(self):
        self.updateTargetActivation(False)
        self.targetStatusPoller = TargetStatusPoller(self.pollingIntervalMinutes,
                                                self.targetId,
                                                self.accessKey,
                                                self.secretKey,
                                                self)
        self.targetStatusPoller.startPolling()

    def OnTargetStatusUpdate(self, target_state):
        if target_state.hasState:

            if target_state.m_activeFlag == False and\
               (target_state.m_status).lower() == "success":

                    self.targetStatusPoller.stopPolling()

                    try:
                        print ".. deleting target .."
                        self.deleteTarget()
                    except Exception as e:
                        print "Error ontargetstatusupdate: " + str(e)

g = DeleteTarget()
g.deactivateThenDeleteTarget()


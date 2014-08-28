import httplib2
import time
from SignatureBuilder import SignatureBuilder
from threading import Timer
from TargetState import TargetState

class TargetStatusPoller:

    headers = {}

    url = "https://vws.vuforia.com"
    path = "/targets/"
    method = "GET"

    intervalInMinutes = 0.0
    targetId = ""
    accessKey = ""
    secretKey = ""

    continuePolling = True
    targetStatusListener = None
    timer = None

    times = 0

    def __init__(self, interval_minutes,
                        target_id,
                        server_access_key,
                        server_secret_key,
                        target_listener):
        self.intervalInMinutes = interval_minutes
        self.targetId = target_id
        self.accessKey = server_access_key
        self.secretKey = server_secret_key
        self.targetStatusListener = target_listener

    def startPolling(self):
        print "Initiate polling for target: " +  self.targetId
        self.timer = Timer(self.intervalInMinutes, self.pollerTask)
        self.timer.start()

    def stopPolling(self):
        self.continuePolling = False;
        self.timer.cancel(); # Terminate the timer thread

    def pollAgain(self):
        if self.continuePolling:
            print ".. polling again .. "

            self.timer = Timer(self.intervalInMinutes, self.pollerTask)
            self.timer.start()

    def pollerTask(self):
        print "New poller task created..."
        try:
            targetState = TargetState.createFromJSON( self.getTarget() )
            if targetState != None:
                self.targetStatusListener.OnTargetStatusUpdate( targetState )
            else:
                print "Target state not reached"
        except Exception as e:
            print "Error creating poller task: " + str(e)
            self.timer.cancel()
            self.times += 1
            if self.times == 3:
                return

        self.pollAgain()

    def getTarget(self):
        h = httplib2.Http('.cache')
        self.setHeaders(self.headers)

        print "Calling getTarget()..."

        response, content = h.request(self.url + self.path + self.targetId,
                                    self.method,
                                    headers=self.headers)
        print "response: " + str(response)
        print "content: " + str(content)
        return content

    def setHeaders(self, headers):
        sb = SignatureBuilder()
        headers.update({'Date' : time.strftime('%a, %d %b %Y %H:%M:%S GMT',
                                 time.gmtime(time.time()))})
        headers.update({'Authorization' : "VWS " +
                         self.accessKey + ":" +
                         sb.tmsSignature(headers,
                                         self.method,
                                         None,
                                         self.path + self.targetId,
                                         self.secretKey)})


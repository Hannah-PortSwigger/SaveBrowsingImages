from burp import IBurpExtender, IProxyListener, IHttpListener, IResponseInfo
from java.io import PrintWriter
from datetime import datetime

class BurpExtender(IBurpExtender, IProxyListener, IHttpListener, IResponseInfo):
    def registerExtenderCallbacks( self, callbacks):
        extName = "Save Images"
        # keep a reference to our callbacks object and add helpers
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()

        # set our extension name
        callbacks.setExtensionName(extName)

        # obtain our output streams
        self._stdout = PrintWriter(callbacks.getStdout(), True)
        self._stderr = PrintWriter(callbacks.getStderr(), True)

        # register ourselves as a Proxy listener
        callbacks.registerHttpListener(self)

        # print extension name
        self._stdout.println(extName)

        return

    def processHttpMessage(self, toolflag, messageIsRequest, messageInfo):
        if (messageIsRequest == False):
            response = messageInfo.getResponse()
            responseInfo = self._helpers.analyzeResponse(response)
            # Find out if image
            inferredMime = responseInfo.getInferredMimeType()
            statedMime = responseInfo.getStatedMimeType()
            # Build list to compare against
            imageMimeTypes = ["JPEG", "PNG"]
            if (statedMime in imageMimeTypes) or (inferredMime in imageMimeTypes):
                # Build file path
                filePathBase = "/PLEASE/REPLACE/ME/"
                fileName = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                fileExtension = "." + inferredMime.lower()
                # Write to file
                f = open(filePathBase + fileName + fileExtension, "wb")
                f.write(response)
                f.close()
        return

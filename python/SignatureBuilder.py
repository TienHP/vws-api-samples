import hmac
from hashlib import sha1
import base64

class SignatureBuilder:
    def tmsSignature(self, headers, method, requestPath, secretKey):
        contentType = ""
        hexDigest = "d41d8cd98f00b204e9800998ecf8427e"

        dateValue = headers['Date']
        toDigest = method + "\n" +\
                hexDigest + "\n" +\
                contentType + "\n" +\
                dateValue + "\n" +\
                requestPath

        shaHashed = self.calculateRFC2104HMAC(secretKey, toDigest)
        return shaHashed

    def calculateRFC2104HMAC(self, key, data):
        try:
            result = hmac.new(key, data, sha1).digest().encode('base64')[:-1]
        except Exception as e:
            print e

        return result

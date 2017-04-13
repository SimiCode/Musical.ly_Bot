










import requests
import hashlib
import random
import time
import json
import urllib

session = requests.Session()

class MusicallyFame2():

    #Function to get siugnature
    def get_signature(self, signing_server, signature_data):
        payload = {"data": json.dumps(signature_data)}
        response = session.get(signing_server, data = payload)
        try:
            return json.loads(response.text)["signature"]
        except ValueError:
            return "signature not received"

    #function to generate get request Id
    def get_unique_id(self):
        request_id = hashlib.md5(str(random.random())).hexdigest()
        request_id = request_id[:8]+"-"+request_id[8:12]+"-"+request_id[12:16]+"-"+request_id[16:20]+"-"+request_id[20:]
        return request_id

    #function for time stamp
    def get_time_stamp(self):
        a = time.time()*1000
        return "%.0f"%a


# def register_user():
magic_obj = MusicallyFame2()

# getting request id
request_id = magic_obj.get_unique_id()
#getting time stamp
timestamp = magic_obj.get_time_stamp()
#common headers
headers = {
    "os": "android 4.1.2",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Musical.ly/2016020601 (Android; LAVA LAVA 4.1.2;rv:16)",
    "language": "en_US",
    "build": "2016020601",
    "Connection": "close",
    "network": "WiFi",
    "mobile": "LAVA Iris 501",
    "version": "4.7.5",
    # "X-Request-Sign2": request_signature,
    "X-Request-ID": request_id,
    "Host": "www.musical.ly",
    "Accept-Encoding": "gzip",
    }
# setting headers to current session
session.headers = headers
signing_server = "http://45.55.203.163:8888/sign"
#preparing signature data
signature_data = {"app":{"-r":"Gvt1","os":"android 4.1.2","method":"POST","url":"https:\/\/www.musical.ly\/rest\/v2\/users\/register","X-Request-ID":request_id,"version":"4.7.5"},"ostype":"and","imei":"51a4454f","mac":"4C:3C:16:82:EE:F3","model":"SM-G730V","sdk":"19","serviceTime":timestamp}
print signature_data
#receiving signature data
request_signature = magic_obj.get_signature(signing_server, signature_data)
#update header
session.headers["X-Request-Sign2"] = request_signature
#prepare data for POST request
handle = "test25krishna"
email = handle+"@gmail.com"
password = handle[::-1]
user = '''{"handle":"%s","email":"%s","password":"%s"}'''%(handle,email,password)
post_url = "http://www.musical.ly/rest/v2/users/register"
BOUNDARY = "27c8b11a-9b7e-4849-a665-7f1a04edf2b7"
data = (
"""
--%(boundary)s
Content-Disposition: form-data; name="user"
Content-Type: application/json; charset=utf-8
Content-Length: %(content_length)s
\r\n%(user)s
--%(boundary)s--
""" % {
        "boundary" : BOUNDARY,
        "content_length" : len(user),
        "user" : user
    }).replace("\n", "\r\n") # HTTP uses DOS-style line endings.


#update current headers
session.headers["Content-Type"] = "multipart/mixed; boundary=\"%s\"" % BOUNDARY
session.headers["MIME-Version"] = "1.0"
session.headers["Host"] = "www.musical.ly"

#make a post request

response = session.post(post_url, data = data, headers=session.headers)
print session.headers
print data
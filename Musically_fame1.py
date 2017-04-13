import csv
import hashlib
import json
import lxml.html
import random
import requests
import time


class MusicallyFame():
    phone_profiles = [
        "lava",
        "samsung",
        "oneplusone",
        "htc",
        "nexus"
    ]
    phone_details = {
        "lava": {
            "os": "android 4.1.2",
            "User-Agent":  "Musical.ly/2016020601 (Android; LAVA LAVA 4.1.2;rv:16)",
            "build": "2016020601",
            "mobile": "LAVA Iris 501",
            "model": "SM-G730V",
            "sdk": "19"
        },
        "samsung": {
            "os": "android 5.1.1",
            "User-Agent":  "Musical.ly/2016040101 (Android; Samsung Galaxy J3 5.1.1;rv:22)",
            "build": "2016040101",
            "mobile": "Samsung Galaxy J3 SM-J320Y",
            "model": "SM-J320Y",
            "sdk": "22"
        },
        "oneplusone": {
            "os": "android 5.1.1",
            "User-Agent":  "Musical.ly/2016040101 (Android; OnePlus A0001 5.1.1;rv:22)",
            "build": "2016040101",
            "mobile": "OnePlus A0001",
            "model": "A0001",
            "sdk": "22"
        },
        "nexus": {
            "os": "android 6.0.1",
            "User-Agent":  "Musical.ly/2016040101 (Android; LGE Nexus 5 6.0.1;rv:23)",
            "build": "2016040101",
            "mobile": "LGE Nexus 5",
            "model": "Nexus 5",
            "sdk": "22"
        },
        "htc": {
            "os": "android 5.1.1",
            "User-Agent":  "Musical.ly/2016040101 (Android; HTC One A9 5.1.1;rv:22)",
            "build": "2016040101",
            "mobile": "HTC One A9",
            "model": "A9",
            "sdk": "22"
        },
    }

    def __init__(self, input_file):
        self.proxies = self.proxy_list()
        self.input_file = input_file
        self.common_header = {
            "os": "android 4.1.2",
            "User-Agent": "Musical.ly/2016020601 (Android; LAVA LAVA 4.1.2;rv:16)",
            "build": "2016020601",
            "mobile": "LAVA Iris 501",
            "version": "4.7.5",
            "X-Requested-With": "XMLHttpRequest",
            "language": "en_US",
            "Connection": "close",
            "network": "WiFi",
            "Host": "www.musical.ly",
            "Accept-Encoding": "gzip",
            "MIME-Version": "1.0"
        }
        self.signing_server = "http://45.55.203.163:8888/sign"
        self.signature_data = {
            "app": {
                "-r": "Gvt1",
                "os": "android 4.1.2",
                "version": "4.7.5"
            },
            "ostype": "and",
            "imei": "51a4454f",
            "mac": "4C:3C:16:82:EE:F3",
            "model": "SM-G730V",
            "sdk": "19",
        }
        self.session = requests.Session()
        # self.session.mount('https://', HTTPAdapter(max_retries=50))

    def proxy_list(self):
        content = requests.get("http://free-proxy-list.net").text
        doc = lxml.html.document_fromstring(content)
        lines = doc.cssselect('table.fpltable tr')
        temp_proxies = []
        for line in lines:
            tds = line.cssselect('td')
            if not tds:
                continue
            anonymity = tds[4].text
            if anonymity != 'transparent' and len(tds) > 7:
                temp_proxies.append({
                    'ip_address': tds[0].text,
                    'port': tds[1].text,
                    'country_code': tds[2].text,
                })
        print len(temp_proxies)

        return temp_proxies

    def alter_handle(self, handle):
        alter_option = random.choice([1, 2, 3])
        if alter_option == 1:
            handle += random.choice([str(n) for n in range(10)])
        elif alter_option == 2:
            _, __ = handle[-1], handle[-2]
            handle = handle[:-3] + _ + __
        else:
            handle = handle[:-1]

        return handle

    def generate_user(self):
        mail_servers = ["@newmail.com", "@gmail.com", "@hotmail.com", "@yahoo.com", "@outlook.com"]
        with open(self.input_file, "rb") as csvfile:
            reader = csv.reader(csvfile)
            reader.next()   # Skip the header row
            for row in reader:
                scraped_data = dict()
                scraped_data["country"] = row[0].decode('string-escape').decode("utf-8")
                scraped_data["nick_name"] = row[2].decode('string-escape').decode("utf-8")
                scraped_data["photo"] = "./photos"+row[3]+".jpg"

                handle = row[3].decode('string-escape').decode("utf-8")
                scraped_data["handle"] = self.alter_handle(handle)
                scraped_data["bio"] = row[4].decode('string-escape').decode("utf-8")
                scraped_data["email"] = scraped_data["handle"]+random.choice(mail_servers)
                scraped_data["password"] = scraped_data["handle"][::-1]+random.choice(["1", "2", "3", "4", "5"])
                yield scraped_data
  
    def get_likes(self, account, like_counts):
        return
  
    def get_follows(self, account, follow_counts):
        return
  
    def get_a_phone(self, phone):
        #random value for imei and mac no
        imei = ''.join(random.choice('0123456789abcdef') for i in range(8))
        val = ''.join(random.choice('0123456789ABCDEF') for i in range(12))
        mac = ':'.join(val[i:i+2] for i in xrange(0, 12, 2))
        self.signature_data["imei"] = imei
        self.signature_data["mac"] = mac

        if phone in self.phone_profiles:
            self.common_header["os"] = self.phone_details[phone]["os"]
            self.common_header["User-Agent"] = self.phone_details[phone]["User-Agent"]
            self.common_header["build"] = self.phone_details[phone]["build"]
            self.common_header["mobile"] = self.phone_details[phone]["mobile"]
          
            self.signature_data["app"]["os"] = self.phone_details[phone]["os"]
            self.signature_data["model"] = self.phone_details[phone]["model"]
            self.signature_data["sdk"] = self.phone_details[phone]["sdk"]

        return

    def get_proxy(self, country):
        if not self.proxies:
            self.proxies = self.proxy_list()

        temp_proxies = list(self.proxies)
        retries = 0

        for proxy in temp_proxies:
            if proxy['country_code'] == country:
                address = "%s:%s" % (proxy['ip_address'], proxy['port'])
                self.proxies.remove(proxy)
                try:
                    _proxy = {"http": "http://"+address, "https": "https://"+address}
                    response = self.session.get("http://ipecho.net/plain", proxies=_proxy)
                    if address.split(':')[0] == response.text:
                        return _proxy

                    raise Exception()
                except:
                    print 'get error, when checking proxy, try to get next proxy'
                    retries += 1
                    if retries == 5:
                        self.proxy_list()

                    if retries == 10:
                        break

        return False

    def unset_proxy(self):
        self.session.proxies = None

    # Function to get signature
    def get_signature(self):
        payload = {"data": json.dumps(self.signature_data)}
        response = self.session.get(self.signing_server, data=payload)
        try:
            return str(json.loads(response.text)["signature"])
        except ValueError:
            return "signature not received"

    # function to generate get request Id
    def get_unique_id(self):
        request_id = hashlib.md5(str(random.random())).hexdigest()
        request_id = request_id[:8]+"-"+request_id[8:12]+"-"+request_id[12:16]+"-"+request_id[16:20]+"-"+request_id[20:]
        return request_id

    # function for time stamp
    def get_time_stamp(self):
        a = time.time()*1000
        return "%.0f" % a
  
    def prepare_header(self, url, method):
        request_id = self.get_unique_id()
        timestamp = self.get_time_stamp()
        self.session.headers.clear()
        self.session.headers = dict(self.common_header)
        self.session.headers["X-Request-ID"] = request_id
        self.signature_data["app"]["X-Request-ID"] = request_id
        self.signature_data["serviceTime"] = timestamp
        self.signature_data["app"]["method"] = method
        self.signature_data["app"]["url"] = url
        request_signature = self.get_signature()
        self.session.headers["X-Request-Sign2"] = request_signature
        return
  
    def prepare_registration_data(self, handle, email, password):
        user = '''{"handle":"%s","email":"%s","password":"%s"}''' % (handle, email, password)
        post_url = "http://www.musical.ly/rest/v2/users/register"
        boundary = "27c8b11a-9b7e-4849-a665-7f1a04edf2b7"
        data = (
        """
--%(boundary)s
Content-Disposition: form-data; name="user"
Content-Type: application/json; charset=utf-8
Content-Length: %(content_length)s
\r\n%(user)s
--%(boundary)s--
        """ % {
            "boundary": boundary,
            "content_length": len(user),
            "user": user
        }).replace("\n", "\r\n")    # HTTP uses DOS-style line endings.

        # update current headers
        self.session.headers["Content-Type"] = "multipart/mixed; boundary=\"%s\"" % boundary
        return data

    def prepare_profile_data(self, user_id, instagram_id, handle, nick_name):
        data = (
        """
--2b8a2224-07c6-4463-bb4b-364576e556ad
Content-Disposition: form-data; name="user"
Content-Type: application/json; charset=utf-8
Content-Length: 276

{"userSettingDTO":{"policyVersion":1,"duet":false,"secret":false,"hideLocation":false,"privateChat":true,"userId":%(user_id)},"instagramID":%(instagram_id),"userDesc":"Editing Test name","gender":"n","handle":%(handle),"nickName":%(nick_name),"userId":%(user_id)}
--2b8a2224-07c6-4463-bb4b-364576e556ad--
        """ % {
            "user_id": user_id,
            "instagram_id": instagram_id,
            "handle": handle,
            "nick_name": nick_name
        })
        return data

    def register_accounts(self, count):
        output_fp = open('success.csv', 'w')
        output_writer = csv.writer(output_fp, delimiter=',')

        all_users = self.generate_user()
        for i in xrange(count):
            user_data = all_users.next()
            self.get_a_phone(random.choice(self.phone_profiles))
            country = user_data["country"]
            proxy = self.get_proxy(country)
            if not proxy:
                proxy = self.get_proxy("US")

            if not proxy:
                continue

            method = "POST"
            url = "https://www.musical.ly/rest/v2/users/register"
            self.prepare_header(url, method)
            handle = user_data["handle"]
            email = user_data["email"]
            password = user_data["password"]
            data = self.prepare_registration_data(handle, email, password)

            try:
                response = self.session.post(url, data=data, proxies=proxy, headers=self.session.headers)

                # profile edit
                # put photo

                if response.status_code == 200:
                    response_status = response.json().get('success', False)
                    if response_status:
                        output_writer.writerow([handle, password, email])
                        args = {
                            "username": "@"+handle,
                            "password": password,
                            "remember_me": "on"
                        }
                        login_url = "http://www.musical.ly/v2/login.do"
                        self.prepare_header(login_url, "POST")
                        response = self.session.post(login_url, params=args, headers=self.session.headers, proxies=proxy)

                        if response.status_code == 200:
                            pass

                print response.content
                print response.status_code

            except Exception, e:
                print e
                pass

            self.session.cookies.clear()
            self.unset_proxy()

        output_fp.close()


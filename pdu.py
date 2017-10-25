from requests import Request, Session
import xml.etree.ElementTree as ET
import urllib3
urllib3.disable_warnings()  # the PDU has a self signed cert so this is needed


class AuthenticationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PDU:
    ip = "https://192.168.0.1"
    endpoint = "/appliance/avtrans"
    username = ""
    password = ""
    s = Session()
    sid = 'none'

    def __init__(self, username, password, ip=ip):
        self.username = username
        self.password = password
        self.ip = ip
        self.SSL_Verify = False

        # Body for the login request
        login_body = '<avtrans><sid></sid><action>login</action><agents><src>wmi</src><dest>controller</dest></agents>' \
                     '<paths><path>units.topology</path></paths><payload><section structure="login"><parameter ' \
                     'id="username" structure="RWtext"><value>{}</value></parameter><parameter id="password" ' \
                     'structure="password"><value>{}</value></parameter></section></payload>' \
                     '</avtrans>'.format(self.username, password)

        # Response to the login request
        resp = self.s.post(self.ip + self.endpoint, data=login_body, verify=self.SSL_Verify)

        # If login was successful
        if (resp.status_code != 200 or b"Login failed" in resp.content):
            print("Login failed - http code: ", resp.status_code)
            raise AuthenticationError("Unable to login. Please check your credentials")

        # Parse the sid from the xml response and save it
        parsed_xml = ET.fromstring(resp.content)
        self.sid = parsed_xml[1].text

    def switch_outlet(self, outlet_num, state):
        on_body = '<avtrans><sid>{}</sid><action>targPowerOn</action><agents><src>wmi</src><dest>controller</dest>' \
                  '</agents><paths><path>units.topology</path></paths><payload><section structure="table" ' \
                  'id="topologyTable"><array id="pdu.JabelonePDU.{}"></array></section></payload>' \
                  '</avtrans>'.format(self.sid, outlet_num)

        off_body = '<avtrans><sid>{}</sid><action>targPowerOff</action><agents><src>wmi</src><dest>controller</dest>' \
                   '</agents><paths><path>units.topology</path></paths><payload><section structure="table" ' \
                   'id="topologyTable"><array id="pdu.JabelonePDU.{}"></array></section></payload>' \
                   '</avtrans>'.format(self.sid, outlet_num)

        if state:
            resp = self.s.post(self.ip + self.endpoint, data=on_body, verify=self.SSL_Verify)
            if (b'Request in Progress' in resp.content):
                print(resp.content)
                print("Switched on outlet ", outlet_num)
                return True

            else:
                return False

        else:
            resp = self.s.post(self.ip + self.endpoint, data=off_body, verify=self.SSL_Verify)
            if (b'Request in Progress' in resp.content):
                print("Switched off outlet ", outlet_num)
                return True

            else:
                return False

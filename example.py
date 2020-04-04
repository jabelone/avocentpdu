# Control an avocent PDU from python

import pdu

# Create an instance of the class and login to the PDU.
# The instance will make a https request to get a session id.
# The instance will then save that into a variable so any
# further requests will not have to login again.
#
# SYNTAX: pdu.PDU("USERNAME", "PASSWORD", "PDU_ID", "https://IP")
with pdu.PDU("admin", "1234", "JabelonePDU", "https://192.168.0.7") as pdu:
    pdu.switch_outlet(3, 0) # switch the third outlet off
    pdu.switch_outlet(5, 1) # switch the fifth outlet on

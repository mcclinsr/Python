#!/usr/bin/env python
from __future__ import unicode_literals, print_function
"""
Create a dictionary representing a network device. The dictionary should have key-value pairs
representing the 'ip_addr', 'vendor', 'username', and 'password' fields.

Print out the 'ip_addr' key from the dictionary.
If the 'vendor' field is 'cisco', then set the 'platform' to 'ios'. If the 'vendor' field is
'juniper', then set the 'platform' to 'junos'.
Create a second dictionary named bgp_fields. The bgp_fields should have a key for 'bgp_as',
'peer_as', and 'peer_ip'.
Using the .update() method add the bgp_fields key-value pairs to the network device dictionary.
Using a for-loop iterate over the dictionary and print out all of the dictionary keys.
Using a single for-loop iterate over the dictionary and print out all of the dictionary keys and
values.
"""

device = {"ip_addr":"10.0.0.1", "vendor":"cisco","username":"cisco", "password":"cisco"}
	
if device["vendor"].lower() == "cisco":
	device['platform'] = 'ios'
print ("the ip address is:", device["ip_addr"])

bgp_fields = {'bgp_as':"",'peer_as':"", 'peer_ip':""}

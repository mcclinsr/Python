from __future__ import print_function

with open('dhcpd_leases 03272018.txt') as f:
	t = f.readlines()
	count = 0
	ips = []

	for i in t:
		if "lease 10.37." in i:
			count += 1
			ips.append(i)
	output = []
	duplicates = 0
	seen = set()
	for value in ips:
		if value not in seen:
			output.append(value)
			seen.add(value)
		else:
			duplicates += 1
print (("-"*60"\n")*3)
#print ("-"*60)
#print ("-"*60)
print ("Total IP count is ",count)
print ("Total unique IP count is ",len(output))
print ("Total Duplicate count is ", duplicates)
print ((""-"*60'\n)*3))
#print ("-"*60)
#print ("-"*60)

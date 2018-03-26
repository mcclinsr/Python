
ip_addr2 = '172.168.1.1'

def print_ip(ip_addr, username='default-user', password='default-pass'):
	print ('my ip address is: {}'.format(ip_addr))
	try:
		print ('my ip address is: {}'.format(ip_addr2))
	except(NameError):
		pass
	print (username)
	print (password)
	return
	
#my_list = ['10.1.1.1','admin','admin123']

#print_ip(*my_list)


print_ip('10.1.1.1')
print_ip('192.168.1.1', 'admin', 'pass123')

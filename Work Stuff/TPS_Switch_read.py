import re
import os
import shutil

path = 'C:/Users/smcclintic/Documents/Scripts/renamed_configs/'
path2 = 'C:/Users/smcclintic/Documents/Scripts/assessed'

def print_vlans(i):
		all_vlans = os.path.join(path2,'all_vlans.txt')
		fopen2 = open(all_vlans)
		readin_time2 = fopen2.read()
		ass_file.write('Vlan info:\n\t')
		vlan_write = open(all_vlans, 'a')
		if i not in fopen2:
			vlan_write.write('%s\n\t' % i)
		else:
			pass

for filename in os.listdir(path):
	file = os.path.join(path,filename)
	filename.strip('.txt')
	new_file = os.path.join(path2,filename+"_assess.txt")
	fopen = open(file)
	readin_time = fopen.read()
	mgmt = re.search('set ip address (.*)', readin_time).group(1)
	vlans = re.findall('set vlan name (.*)', readin_time)
	ass_file = open(new_file, 'w')
	ass_file.write("Management info:\n\t"+mgmt+'\n')
	for i in vlans:
		ass_file.write('%s\n\t' % i)
		print_vlans(i)
		#print (i)

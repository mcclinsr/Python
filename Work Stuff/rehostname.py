import re
import os
import shutil

path = 'C:/Users/smcclintic/Documents/Scripts/configs'
path2 = 'C:/Users/smcclintic/Documents/Scripts/renamed_configs/'
for filename in os.listdir(path):
	file = path+"/"+filename
	f = open(file)
	t = f.read()
	hostname = re.search('set system name (.*)', t).group(1)
	hostname = hostname.replace('\"', "")
	hostname = hostname+".txt"
	newfile = os.path.join(path2, filename)
	print (hostname)
	shutil.copy(file,path2)
	os.rename(newfile, os.path.join(path2,hostname))
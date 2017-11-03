#!/usr/bin/env python3
import os
import os.path
import sys
import time
import stat
from datetime import date , datetime

#conversao de bytes
def sizeConvert(num, suffix='B'):
	for unit in ['','K','M','G','T','P','E','Z']:
		if abs(num) < 1023.9:
			return "%4.1f%s%s" % (num, unit, suffix)
		num /= 1023.9
	return "%4.1f%s%s" % (num, 'Yi', suffix)


# tamanho total do diretorio
def sizeDirec(pathF):
	size = float(0)
	for name, subfolders, filenames in os.walk(pathF):
		for file in filenames:
			t = (name+"/"+file)
			if os.access(t, os.R_OK):
				statinfo = os.stat(t)
				size +=  os.path.getsize(t)
	return size

try:
	mypath = (os.getcwd()+'/' + sys.argv[1])
except:
	print("eh preciso parametro com endereco da pasta")
	sys.exit(1)
if(not (os.path.isdir(mypath))):
	print("Precisa ser diretorio")
	sys.exit(1)


allPaths = []
for name, subfolders ,filenames in os.walk(mypath):
	for subfolder in subfolders :
		d = os.path.join(name ,subfolder+"/")
		if os.access(d, os.R_OK):
			statinfo = os.stat(d)
			size = sizeDirec(d)
			size = sizeConvert(size)
			modificado = datetime.fromtimestamp(statinfo.st_mtime).strftime("%Y-%m-%d")
			allPaths.append((modificado,size ,d))
		else:
			print("sem permissao em " + d)
	for file in filenames:
		t = (name+"/"+file)
		if os.access(t, os.R_OK):
			statinfo = os.stat(t)
			size = (sizeConvert(float(statinfo.st_size)))
			modificado = datetime.fromtimestamp(statinfo.st_mtime).strftime("%Y-%m-%d")
			allPaths.append((modificado,size ,t))
		else:
			print("sem permissao em :" + t)
#ordena pelo mais velhos
allPaths.sort(key=lambda x: time.mktime(time.strptime(x[0],"%Y-%m-%d")),reverse=False)

for oldest in allPaths:
	print('%s %8s %s' % (oldest[0], oldest[1], oldest[2])) 

##ordenar imagens
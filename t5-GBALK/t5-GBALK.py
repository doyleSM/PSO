import json, requests, sys, shutil, os, re, fileinput

directory = (os.getcwd()+"/img/")

def getCurrentComicNumber():
	url = "http://xkcd.com/info.0.json"   
	response = requests.get(url)
	try:	
		response.raise_for_status()
		load = (json.loads(response.text))
		numCurrent = (load['num'])
		return numCurrent
	except:
		print("Erro ao conectar")
		sys.exit(1)
		return None

def downloadComics():

	currentComicNumber = getCurrentComicNumber()
	url = (("http://xkcd.com/", "/info.0.json"))
	last4ComicsNames = []
	for i in range(0,4):
		response = requests.get(url[0]+(str(currentComicNumber-i))+url[1], stream=True)
		#print(url[0]+(str(currentComicNumber-i))+url[1])
		try:	
			response.raise_for_status()
			load = (json.loads(response.text))
			urlImage = (load['img'])
			imageName = (load['title'])+'.png'
			last4ComicsNames.append(str(currentComicNumber-i))
			response = requests.get(urlImage, stream=True)

			with open(directory+(str(currentComicNumber-i)), 'wb') as out_file:
				shutil.copyfileobj(response.raw, out_file)
			del response
		except:
			print("except")
			pass
	print(last4ComicsNames)
	return last4ComicsNames


def removeOldComics(last4ComicsNames):
	for filename in os.listdir(directory):
		if (filename not in last4ComicsNames):
			os.unlink(directory+filename)



#def updateHtml(lastComicsNames):
#	count = 0
#	srcs = []
#	file = 'index.html'
#	p = re.compile(r'src=[^\s]+')
#	with open(file,'r') as file:
#		for line in file:
#			m=p.search(line)
#			if(m):
#				url = "src=\"img/"+lastComicsNames[count]+"\""
				#print(url)
#				m2 = p.sub(url, line)
#				#srcs.append(m.group())
#				count =+1
#				print(m2)
			#else:
#				print(line.replace(line, line), end='')
def updateHtml(lastComicsNames):
	count = 0
	p = re.compile(r'src=[^\s]+')
	o = open("output","a") #open for append
	for line in open('index.html','r'):
		m=p.search(line)
		if(m):
			url = "src=\"img/"+lastComicsNames[count]+"\""
			#print(url)
			m2 = p.sub(url, line)
			#print(m2)
			line = line.replace(line, m2)
			count += 1
		o.write(line)
	o.seek(0,0)
	o.close()
	os.unlink(os.getcwd()+"/index.html")
	os.rename('output', 'index.html')


	


last4ComicsNames = downloadComics()
last4ComicsNames.sort(key=lambda i: i[1], reverse = True)
removeOldComics(last4ComicsNames)
updateHtml(last4ComicsNames)

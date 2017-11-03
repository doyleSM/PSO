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
	last4Comics = []
	for i in range(0,4):
		response = requests.get(url[0]+(str(currentComicNumber-i))+url[1], stream=True)
		#print(url[0]+(str(currentComicNumber-i))+url[1])
		try:	
			response.raise_for_status()
			load = (json.loads(response.text))
			urlImage = (load['img'])
			comicTitle = (load['title'])
			comicDate = ((load['day'])+"-"+(load['month'])+"-"+(load['year']))
			print(comicDate)
			last4Comics.append(((str(currentComicNumber-i)), comicTitle, comicDate))
			response = requests.get(urlImage, stream=True)

			with open(directory+(str(currentComicNumber-i)), 'wb') as out_file:
				shutil.copyfileobj(response.raw, out_file)
			del response
		except:
			print("except")
			pass
	return last4Comics


def removeOldComics(last4Comics):
	lastComicsNum =[]
	for i in range(4):
		lastComicsNum.append(last4Comics[i][0])
	for filename in os.listdir(directory):
		if (filename not in lastComicsNum):
			os.unlink(directory+filename)
			


def updateHtml(lastComics):
	lastComicsNum =[]
	comicsTitles = []
	comicsDates = []
	for i in range(4):
		lastComicsNum.append(last4Comics[i][0])
		comicsTitles.append(last4Comics[i][1])
		comicsDates.append(last4Comics[i][2])
	print(comicsDates)
	count = 0
	countTitle = 0
	countDate = 0
	p1 = re.compile(r'src=[^\s]+')
	p2 = re.compile(r"<h2>(.*?)<\/h2>")
	p3 = re.compile(r"<h4>(.*?)<\/h4>")
	o = open("output","a") #open for append
	for line in open('index.html','r'):
		q = p3.search(line)
		if(q):
			url = "<h4> Data da publicacao: "+comicsDates[countDate]+"</h4>"
			q2 = p3.sub(url, line)
			line = line.replace(line, q2)
			countDate +=1
		n=p2.search(line)
		if(n):
			url = "<h2>"+comicsTitles[countTitle]+"</h2>"
			n2 = p2.sub(url, line)
			line = line.replace(line, n2)
			countTitle += 1
			print(countTitle)
		m=p1.search(line)
		if(m):
			url = "src=\"img/"+lastComicsNum[count]+"\""
			m2 = p1.sub(url, line)
			line = line.replace(line, m2)
			count += 1
			print(count)
		o.write(line)
	o.seek(0,0)
	o.close()
	os.unlink(os.getcwd()+"/index.html")
	os.rename('output', 'index.html')


last4Comics = downloadComics()
last4Comics.sort(key=lambda i: i[0], reverse = True)
removeOldComics(last4Comics)
updateHtml(last4Comics)

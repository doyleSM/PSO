import json, requests, sys, shutil, os, re
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
		try:	
			response.raise_for_status()
			load = (json.loads(response.text))
			print("Baixando imagem " +str(i+1))
			urlImage = (load['img'])
			comicTitle = (load['title'])
			comicDate = ((load['day'])+"-"+(load['month'])+"-"+(load['year']))
			last4Comics.append(((str(currentComicNumber-i)), comicTitle, comicDate))
			response = requests.get(urlImage, stream=True)
			print("Gravando imagem no diretorio")
			with open(directory+(str(currentComicNumber-i)), 'wb') as out_file:
				shutil.copyfileobj(response.raw, out_file)
			del response
			print("Ok")
		except:
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

	count = 0
	countTitle = 0
	countDate = 0
	countRef = 0
	p1 = re.compile(r'src=[^\s]+')
	p2 = re.compile(r"<h2>(.*?)<\/h2>")
	p3 = re.compile(r"<h4>(.*?)<\/h4>")
	p4 = re.compile(r'href=[^\s]+')
	if(os.path.exists("index.html")):   # como vou abrir em append, para poder escrever linha a linha
		try:
			os.unlink(os.getcwd()+"/index.html")  #preciso deletar o arquivo caso ja exista
		except:
			print("Nao consegui remover o arquivo index.html")
			print("Encerrando")
			sys.exit(1)
	try:
		o = open("index.html","a") #open for append
	except:
		print("sem permissao de escrita em index.html")
		sys.exit(1)

	for line in open('template.html','r'):
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
		z = p4.search(line)
		if(z):
			url = "href=\"img/"+lastComicsNum[countRef]+"\">"
			m3 = p4.sub(url, line)
			line = line.replace(line, m3)
			countRef +=1
		m=p1.search(line)
		if(m):
			url = "src=\"img/"+lastComicsNum[count]+"\""
			m2 = p1.sub(url, line)
			line = line.replace(line, m2)
			count += 1

		o.write(line)
	o.seek(0,0)
	o.close()
	

last4Comics = downloadComics()
last4Comics.sort(key=lambda i: i[0], reverse = True)
removeOldComics(last4Comics)
updateHtml(last4Comics)

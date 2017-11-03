#!/usr/bin/env python3
# vim: fileencoding=utf-8
import socket
import argparse, re, sys, json, requests
from collections import Counter

#split é numero de characteres a ser ignorado 
#por exemplo SRC=192.168 ignorará SRC=
def findAndList(split, regex):
	file = sys.argv[1]
	lstMatches = []
	p = regex
	with open(file,'r') as file:
		for line in file:
			m=p.search(line)
			if(m):
				lstMatches.append(m.group()[split:])
		return lstMatches

def myCount(myList):
	myList = Counter(myList)
	myList = list(myList.items())
	myList.sort(key=lambda i: i[1], reverse = True)
	return myList[:10]

def location(myList):
	url = "http://ip-api.com/json/"
	lista = []
	for ip in myList:
		response = requests.get(url+ip[0])
		cidade = "not found"
		pais = "not found"
		try:	
			response.raise_for_status()
			load = (json.loads(response.text))
			l = load
			cidade = (l['city'])
			pais = (l['country'])
		except:
			pass
		lista.append((ip[0], ip[1], cidade, pais))	
	return lista 

def source():
	p = re.compile(r'SRC=[^\s]+')
	listSrc = findAndList(4, p)
	listSrc = myCount(listSrc)
	print("Buscando a localizacao dos ips fonte, isso pode demorar um pouco.")
	listSrc = location(listSrc)
	print("IP FONTE")
	print('%8s  %13s %25s %26s\n' % ("IP","TOTAL", "CIDADE", "PAIS"))
	for x in listSrc:
		print('%15s  %5s %28s %28s' % (x[0], x[1], x[2], x[3]))
	print("Obs: pode ser que tenha ficado muito espacado na cidade, mas em alguns casos o nome da cidade era muito grande\n")

def destiny():
	p = re.compile(r'DST=[^\s]+')
	listDst = findAndList(4,p)
	listDst = myCount(listDst)
	print("Buscando a localizacao dos ips destino, isso pode demorar um pouco.")
	listDst = location(listDst)
	print("IP DESTINO")
	print('%8s  %13s %25s %20s\n' % ("IP","TOTAL", "CIDADE", "PAIS"))
	for x in listDst:
		print('%15s  %5s %28s %20s' % (x[0], x[1], x[2], x[3]))
	print("obs: pode ser que tenha ficado muito espacado na cidade, mas em alguns casos o nome da cidade era muito grande\n")

def protocol():
	p = re.compile(r'PROTO=[^\s]+')
	listProto = findAndList(6,p)
	listProto = myCount(listProto)
	print("\nPROTOCOLS")
	print('%6s %7s\n' % ("NOME",  "TOTAL"))
	for x in listProto:
		print('%6s %8s' % (x[0], x[1]))


def port():
	p = re.compile(r'SPT=[^\s]+')
	listPort = findAndList(4,p)
	listPort = myCount(listPort)
	print("\nPORTAS")
	print('%7s %6s %10s\n' % ("Porta",  "Total", "Nome"))
	for x in listPort:
		try:
			print('%6s %6s %12s' % (x[0], x[1], str(socket.getservbyport(int(x[0])))))
		except:
			print('%6s %6s %16s' % (x[0], x[1], "nao registrada"))
def lenFile():
	with open(sys.argv[1],'r') as file:
		lines = (sum(1 for line in file))
	print('numero total de pacotes: %s \n' % lines)


lenFile()
source()
destiny()
protocol()
port()
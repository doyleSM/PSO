#!/bin/bash

input=$1

#total de pacotes
nPackets(){
	npackets=`wc -l $input | awk '{ print $1 }'` 
	echo "1. Número total de pacotes: $npackets"
}

#top 10 ips src e quantidade de cada um
ipsSrc(){
	cat $input | sed 's/SRC=/\n/g' | awk '{ print $1}' | grep [0-9] | sort | uniq -c | sort -k1 -n -r > .a
	echo "2. Top 10 IPs fonte"
	echo "Pacotes	IP"
	sed -n 1,10p .a
}

#top 10 ips dst e quantidade de cada um
ipsDst(){
	cat $input | sed 's/DST=/\n/g' | awk '{ print $1}' | grep [0-9] | sort | uniq -c | sort -k1 -n -r > .b
	echo "3. Top 10 IPs destino"
	echo "Pacotes	IP"
	sed -n 1,10p .b
}

#quantidade de pacotes por protocolo (TCP, UDP, ICMP)
nProto(){
	echo "4. Quantidade de pacotes por protocolo" 
	cat $input | awk '/PROTO=/' | sed 's/^.*PROTO=//g' | awk '{print $1}' | sort -n | uniq -c | awk '{print $1, $2}'
}

#top 10 portas usadas: nome, número e quantidades
nPorts(){

	echo "5. Top 10 portas origem"
	echo "Nº  Prot  Nome  Quant."
	cat $input | awk '/PROTO=/' | sed 's/^.*PROTO=//g' | awk '{print $2,$1}' |\
	awk '/SPT=/' | sed 's/^.*SPT=//g' | tr 'A-Z' 'a-z' |\
	sort -n | uniq -c | sort -n -r | head -10 | awk '{print $2, $3, $1}' > .a

	cat /etc/services | egrep -v '^#|^$' | awk '{ print $1, $2}' | sed 's/\// /g' | awk 'NF>=3' |\
	awk '{print $2, $3, $1}' > .b
	awk 'FNR==NR{a[$1,$2]=$3; next} ($1,$2) in a{print $0, a[$1,$2]} ' .a .b > ptname
	cat .a >> ptname
	cat ptname | sort -u -k1,1 -k2,2 | awk '{ print $NF,$0 }' | sort -k1,1 -n -r | cut -f2- -d' '

}

nPackets
ipsSrc
ipsDst
nProto
nPorts

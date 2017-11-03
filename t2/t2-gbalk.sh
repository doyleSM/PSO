
entrada=$1


total(){
	echo "-----TOTAL DE PACOTES------"
	cat $entrada |\
	wc -l $entrada
}
total


buscaSRC(){
    echo "------------IP FONTE-----------"
    echo "---total - Fonte--------- "
	cat $entrada |\
	sed 's/ /\n/g ' |\
	egrep 'SRC=' |\
	sed 's/=/: /g ; s/^[^:]\+: //g' |\
	sort -n | uniq -c | \
	sort -rn | head
}

buscaSRC

buscaDST(){
    echo "-----------IP DESTINO-----------"
    echo "  total - Destino"
	cat $entrada |\
	sed 's/ /\n/g ' |\
	egrep 'DST=' |\
	sed 's/=/: /g ; s/^[^:]\+: //g' |\
	sort -n | uniq -c |\
	sort -rn | head 
}

buscaDST

buscaTCP(){
    echo "-----------PRTOCOLOS-----------"
    echo "  total - protocolo" 
	cat $entrada |\
	sed 's/ /\n/g ' |\
	egrep 'PROTO=' |\
	sed 's/=/: /g ; s/^[^:]\+: //g' |\
	sort -n | uniq -c |\
	sort -rn | head
}

buscaTCP

buscaPorta(){
	echo "-----TOTAL PORTAS---------"
	cat $entrada |\
	sed 's/ /\n/g ' |\
	egrep '^\SPT=' |\
	sed 's/=/: /g ; s/^[^:]\+: //g'|\
	sort -n | uniq -c |\
	sort -rn | head
}

buscaPorta

nomePorta(){
	cat $entrada |\
	sed 's/ /\n/g ' |\
	egrep '^\SPT=' |\
	sed 's/=/: /g ; s/^[^:]\+: //g' |\
	sort -n | uniq -c|\
	sort -rn | head |\
	sed 's/.*[ ]//g' > portas.txt
	cat /etc/services |\
	sed 's/\// /g' > services.txt
	echo " NOME SERVIÇO - PORTA"
	echo "para funcionamento do prox comando preciso ter permissão para criar e apagar arquivo"
	awk -F" " 'FNR==NR {hash[$1]; next} $2 in hash' portas.txt services.txt |\
	sort -u -t" " -k 1,1 

	rm portas.txt
	rm services.txt

}
nomePorta

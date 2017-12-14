#usr/binenv python3
import telepot
import jwt 
import datetime
from api import token
bot = telepot.Bot("437774793:AAHVsD-6GHIrypiwUindcal9xULswRuDTa0") 

def responde(msg):
	
	id = (msg['from']['id'])

	if(msg['text'] == 'token'):
		newToken = token()
		bot.sendMessage(id, newToken)

	else:
		bot.sendMessage(id, "se voce precisa de um token, digite 'token', caso contrario nao posso ajuda-lo")


bot.message_loop(responde)

print("rodando....")
while(True):
	pass

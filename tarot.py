#For drawing random card + shuffle deck
import random

#For sending request to local llm
import requests
import json

majnum = 22
minnum = 56
totalnum = 78

#Generate full deck and return it
def getFullDeck():
	#Original order = Justice #8, Strength #11
	#Hermetic Order of the Golden Dawn/RWS = Strength #8, Justice #11
	#These vars use original order
	deck = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", 
			"The Chariot", "Justice", "The Hermit", "Wheel of Fortune", "Strength", "The Hanged Man", "Death", "Temperance", 
			"The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
	for i in range(1, 15):
		numstr = str(i)
		if i < 10:
			numstr = "0"+numstr
		deck.append("wands"+numstr)
		deck.append("cups"+numstr)
		deck.append("swords"+numstr)
		deck.append("pents"+numstr)
	return deck

def getMajorArcana():
	#Original order = Justice #8, Strength #11
	#Hermetic Order of the Golden Dawn/RWS = Strength #8, Justice #11
	#These vars use original order
	deck = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", 
			"The Chariot", "Justice", "The Hermit", "Wheel of Fortune", "Strength", "The Hanged Man", "Death", "Temperance", 
			"The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
	return deck

#Converts card filename formatted string to full name of card.
def getCardName(card):
	majorarcana = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", 
			"The Chariot", "Justice", "The Hermit", "Wheel of Fortune", "Strength", "The Hanged Man", "Death", "Temperance", 
			"The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"]
	suits = {"wands": "Wands", "swords": "Swords", "cups": "Cups", "pents": "Pentacles"}
	nonnum = {"1": "Ace", "11": "Page", "12": "Knight", "13": "Queen", "14": "King"}
	if card in majorarcana:
		return card 
	else:
		cardnum = card[-2:]
		cardsuit = card[:-2]
		cardsuit = suits[cardsuit]
		cardnumstring = str(int(cardnum))
		if cardnumstring in nonnum:
			cardnumstring = nonnum[cardnumstring]
		return cardnumstring+" of "+cardsuit

#Draws a card from a deck and returns it
#Deck is modified in place
def pickCard(deck):
	card = deck.pop(random.randint(0,len(deck)-1))
	return card

#Draws spread, returns tuple with (spreadlocation, fullcardname, cardfilename)
#Currently only past/present/future spread
def drawSpread(deck, spreadlayout):
	spread = []
	for spot in spreadlayout:
		card = pickCard(deck)
		cardname = getCardName(card)
		spread.append((spot, cardname, card))
	# pastcard = pickCard(deck)
	# pastname = getCardName(pastcard)
	# presentcard = pickCard(deck)
	# presentname = getCardName(presentcard)
	# futurecard = pickCard(deck)
	# futurename = getCardName(futurecard)
	# spread = [("Past", pastname, pastcard), ("Present", presentname, presentcard), ("Future", futurename, futurecard)]
	return spread


#oobaprompt is the oobabooga api request. Just enter prompt for the parameter and we get the response back
def oobaprompt(question):

	stopping_strings = ["\n### Instruction", "\n### Response:"]
	prompt = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n### Instruction:\n"
	prompt += question+"\n### Response:"

	#Send the request
	data = {"prompt": prompt, "stopping_strings": stopping_strings}
	response = requests.post('http://127.0.0.1:5000/api/v1/generate', data=json.dumps(data))
	if response.status_code == 200:
		#Get the output from the response
		jsondata = json.loads(response.content.decode('utf-8'))
		output = str(jsondata['results'][0]['text']).strip()
		return output
	else:
		return "Error"

def getTarotReading(spread):
	preprompt = "I'm doing a tarot card reading, please provide an analysis. One sentence per card.\n"
	cardprompt = ""
	for card in spread:
		cardprompt += card[0]+": "+card[1]+"\n"
	postprompt = "Explain what this reading means, and the overall picture."
	prompt = preprompt+cardprompt+postprompt
	reading = oobaprompt(prompt)
	return reading

# deck = getFullDeck()
# random.shuffle(deck)
# spreadlayout = {"Past": (0,0,0), "Present": (1,0,0), "Future": (2,0,0)}
# ppfspread = drawSpread(deck, spreadlayout)

# for card in ppfspread:
# 	print(card[0]+":", card[1])

# reading = getTarotReading(ppfspread)
# print("Reading:", reading)
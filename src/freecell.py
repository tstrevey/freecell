import copy
from random import randint

class Card(object):	
	suits = {0:'h',1:'s',2:'d',3:'c'}
	ranks = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K'}
	
	def __init__(self, suit, rank):
		self.suit = suit;
		self.rank = rank;
	
	def __repr__(self):
		return self.__str__()
		
	def __str__(self):
		return Card.ranks[self.rank] + Card.suits[self.suit]
	
	def __eq__(self, other): 
		return self.suit == other.suit and self.rank == other.rank
	
	def __lt__(self, other):
		return self.suit * 13 + self.rank < other.suit * 13 + other.rank
	
	def __gt__(self, other):
		return self.suit * 13 + self.rank < other.suit * 13 + other.rank
		
	def getSuit(self):
		return self.suit
	
	def getRank(self):
		return self.rank
		
class Deck(object):	
	def __init__(self):
		self.cardList = []
		for s in range(len(Card.suits)):
			for i in range(len(Card.ranks)):
				self.cardList.append(Card(s,i+1))
	
	def __repr__(self):
		return str(self.cardList)
		
	def __str__(self):
		return str(self.cardList)
	
	def size(self):
		return len(self.cardList)
		
	def shuffle(self):
		for i in range(10):
			newDeck = []
			while(len(self.cardList) > 0):
				r = randint(0,len(self.cardList)-1)
				newDeck.append(self.cardList[r])
				del self.cardList[r]
			self.cardList = newDeck
			
	def draw(self, n = 1):
		tmp = []
		for i in range(n):
			tmp.append(self.cardList[0])
			del self.cardList[0]
		return tmp
	
class BoardState:
	def __init__(self, gamestate = None, bsc = None):
		if bsc is not None:
			self.board = copy.deepcopy(bsc[0])
			self.swap = copy.deepcopy(bsc[1])
			self.clear = copy.deepcopy(bsc[2])
		elif gamestate is not None:
			self.board = gamestate.board
			self.swap = gamestate.swap
			self.clear = gamestate.clear
		else:
			self.newGame()
			
	def __repr__(self):
		return self.__str__()
		
	def __str__(self):
		pSwap = ""
		pClear = ""
		pRows = ""
		for k in range(max([len(x) for x in self.board])):
			for l in range(8):
				if len(self.board[l]) > k:
					pRows = "{}[{}]".format(pRows, self.board[l][k])
					if not self.board[l][k].getRank() == 10:
						pRows = "{} ".format(pRows)
				else:
					pRows = "{}[  ] ".format(pRows)
			pRows = "{}\n".format(pRows)
		for i in range(4):
			if len(self.swap) > i:
				pSwap = "{}[{}]".format(pSwap, self.swap[i])
			else:
				pSwap = "{}[  ]".format(pSwap)
		for j in range(4):
			if self.clear[j] is not None:
				pClear = "{}[{}]".format(pClear, self.clear[j])
			else:
				pClear = "{}[  ]".format(pClear)
		return "\n" + pSwap + " " * (39 - len(pClear + pSwap)) + pClear + "\n" + pRows
	
	def __eq__(self, other):
		return self.__hash__() == other.__hash__()
		'''
		if len(self.swap) == len(other.swap):
			for s in range(len(self.swap)):
				if not self.swap[s] == other.swap[s]:
					return False
		else:
			return False
		for x in range(len(self.board)):
			if len(self.board[x]) == len(other.board[x]):
				for y in range(len(self.board[x])):
					if not self.board[x][y] == other.board[x][y]:
						return False
			else:
				return False
		return True
		'''
	
	def __hash__(self):
		s = self.swap[:]
		return hash((str(self.board), str(s.sort())))
	'''
	Sets the boardState
	'''
	def setBoardState(self, board, swap, clear):
		self.board = copy.deepcopy(board)
		self.swap = copy.deepcopy(swap)
		self.clear = copy.deepcopy(clear)
	'''
	Returns a copy of itself
	'''
	def copy(self):
		return BoardState(bsc = [self.board, self.swap, self.clear])
	'''
	Clears the board and deals out a new game
	'''
	def newGame(self):
		self.board = [[],[],[],[],[],[],[],[]]
		self.swap = []
		self.clear = [None for x in range(4)]
		d = Deck()
		d.shuffle()
		for i in range(d.size()):
			dr = d.draw()
			for c in dr:
				self.board[i%8].append(c)
	'''
	Returns True if the board has been cleared
	'''
	def isWinner(self):
		for c in self.clear:
			if c is None or c.getRank() != 13:
				return False
		return True
	'''
	Returns True if the first card can be stacked onto the second card
	'''
	def isStackable(self, cardToMove, card):
		return (cardToMove.getSuit()%2 - card.getSuit()%2 != 0) and \
			cardToMove.getRank() + 1 == card.getRank()
	'''
	Returns True if the card can be played to the clear space
	'''
	def isValidClear(self, card):
		suit = card.getSuit()
		if self.clear[suit] is None and card.getRank() == 1:
			return True
		elif self.clear[suit] is not None:
			return card.getRank() == self.clear[card.getSuit()].getRank() + 1
		return False
	'''
	Returns the stack height, starting at the bootom of the given collumn
	'''
	def findStackHeight(self, collumn):
		height = 1
		for i in range(len(self.board[collumn])-1,0,-1):
			if self.isStackable(self.board[collumn][i], self.board[collumn][i-1]):
				height += 1
			else:
				break
		return height
	'''
	Returns the maximum move space
	'''
	def findMaxMoves(self, toEmpty = False):
		emptySwap = 4 - len(self.swap)
		emptyCols = 0
		maxMoves = 1
		for c in self.board:
			if len(c) == 0:
				emptyCols += 1
		if toEmpty:
			maxMoves = (emptySwap + 1) + (emptyCols - 1) * (emptySwap + 1)
		else:
			maxMoves = (emptySwap + 1) + emptyCols * (emptySwap + 1)
		if maxMoves > 13:
			return 13
		else:
			return maxMoves
	'''
	Moves a stack of cards between collumns
	'''
	def _moveStack(self, fromSpot, toSpot, numToMove = None):
		if numToMove is None:
			maxMoves = self.findMaxMoves(toEmpty = True)
			stackHeight = self.findStackHeight(fromSpot)
			numToMove = min(maxMoves, stackHeight)
		clearAt = len(self.board[fromSpot]) - numToMove
		for i in range(numToMove):
			self.board[toSpot].append(self.board[fromSpot].pop(clearAt))
	'''
	Returns True and makes the given move if it is valid
	'''
	def _moveCards(self, fromSpot, toSpot):
		if fromSpot == 0:
			if len(self.swap) == 0:
				return False
			elif toSpot in range(1,9):
				toSpot -= 1
				if len(self.board[toSpot]) == 0:
					self.board[toSpot].append(self.swap.pop(0))
					return True
				for c in self.swap:
					if self.isStackable(c, self.board[toSpot][-1]):
						self.board[toSpot].append(c)
						self.swap.remove(c)
						return True
				return False
			elif toSpot == 9:
				for c in self.swap:
					if self.isValidClear(c):
						self.clear[c.getSuit()] = c
						self.swap.remove(c)
						return True
				return False
			elif toSpot == 0:
				self.swap.append(self.swap.pop(0))
				return True
			else:
				return False
		elif fromSpot in range(1,9):
			fromSpot -= 1
			if len(self.board[fromSpot]) == 0:
				return False
			elif toSpot in range(1,9):
				toSpot -= 1
				if len(self.board[toSpot]) == 0:
					self._moveStack(fromSpot, toSpot)
					return True
				maxMoves = self.findMaxMoves()
				for i in range(1,self.findStackHeight(fromSpot)+1):
					if i > maxMoves:
						break
					if self.isStackable(self.board[fromSpot][-i], self.board[toSpot][-1]):
						self._moveStack(fromSpot, toSpot, i)
						return True
				return False
			elif toSpot == 0:
				if len(self.swap) < 4:
					self.swap.append(self.board[fromSpot].pop())
					return True
				return False
			elif toSpot == 9:
				if self.isValidClear(self.board[fromSpot][-1]):
					c = self.board[fromSpot].pop()
					self.clear[c.getSuit()] = c
		return False
	
	def moveCards(self, fromSpot, toSpot, withAutoClear = False):
		success = self._moveCards(fromSpot, toSpot)
		if withAutoClear:
			while self._autoClear():
				continue
		return success
	'''
	Automatically clears non-useful cards to the clear space
	'''
	def _autoClear(self):
		didAClear = False
		lowestCleared = 13
		for c in self.clear:
			if c is None:
				lowestCleared = 0
				break
			elif c.getRank() < lowestCleared:
				lowestCleared = c.getRank()
		clearUnder = lowestCleared + 2
		for s in self.swap:
			if self.isValidClear(s) and s.getRank() <= clearUnder:
				didAClear = True
				self.swap.remove(s)
				self.clear[s.getSuit()] = s
		for b in self.board:
			if len(b) > 0:
				if self.isValidClear(b[-1]) and b[-1].getRank() <= clearUnder:
					didAClear = True
					c = b.pop()
					self.clear[c.getSuit()] = c
		return didAClear

def playFreecell():
	import time
	print("Hello, welcome to Commandline Freecell")
	time.sleep(2)
	print("Building deck....")
	time.sleep(1)
	print("Shuffling...")
	time.sleep(1)
	print("Ok, ready? Let's play!")
	board = BoardState()
	user = ""
	while True:
		print("0" + " " * 23 + "9")
		print(board)
		print(" 1    2    3    4    5    6    7    8")
		print("Q to quit      N for New Game")
		first = raw_input("Enter the number to move a card from:")
		while len(first) < 1:
			first = raw_input("Enter the number to move a card from:")
		if first == "q" or first == "Q":
			break
		elif first == "n" or first == "N":
			board.newGame()
			continue
		elif int(first) == 0:
			print("Using leftmost card, 0 again will rotate the swap space")
		second = raw_input("Enter the number to move the card to:")
		while len(second) < 1:
			second = raw_input("Enter the number to move the card to:")
		board.moveCards(int(first),int(second), withAutoClear = True)
		if board.isWinner():
			print("You Win!!!")
			board.newGame()
	print("Thanks for playing!")


if __name__ == "__main__":
	playFreecell()

import random
# card=[attr1,attr2,attr3,attr4] atributes are integers 0,1,2

attributeNumber = 4
optionsPerAttribute = 3 #(number of cards per set)

def createDeck() -> list[list[int]]:
    deck = []
    for a in range(optionsPerAttribute):
        for b in range(optionsPerAttribute):
            for c in range(optionsPerAttribute):
                for d in range(optionsPerAttribute):
                    deck.append([a,b,c,d])
    return deck


def drawOneFromDeckToBoard(deck:list[list[int]], board:list[list[int]]) -> list[int]: #returns added card
    card=deck.pop(random.randint(0, len(deck)-1))
    board.append(card)
    return card

def setAbidesRules(set:list[list[int]]) -> bool: #checks if the card in the set actually fulfill the reqiurements of a set generally
    if len(set) != optionsPerAttribute:
        return False
    
    atributesList = []
    for it in range(attributeNumber):
        atributesList.append([])
    for card in set:
        for i in range(len(card)):
            if card[i] not in atributesList[i]:
                atributesList[i].append(card[i])
    

    for atr in atributesList:
        if len(atr) != 1 and len(atr) != optionsPerAttribute:
            return False
    return True

def setInBoard(set:list[list[int]], board:list[list[int]]) -> bool:
    for card in set:
        if card not in board:
            return False
    return True

def setIsValid(set:list[list[int]], board:list[list[int]]) -> bool: # checks if set is valid in current state of game
    return setInBoard(set, board) and setAbidesRules(set)

def removeSetFromBoard(set:list[list[int]], board:list[list[int]]) -> None:
    for card in set:
        board.pop(board.index(card))

def drawNFromDeckToBoard(deck:list[list[int]], board:list[list[int]], n:int) -> list[list[int]]: #returns added cards
    cards=[]
    for i in range(n):
        if len(deck) != 0:
            cards.append(drawOneFromDeckToBoard(deck, board))
    return cards

def createBoard(deck) -> list[list[int]]:
    board = []
    drawNFromDeckToBoard(deck, board, 12)
    return board

def noSetsInBoard(board):
    for a in range(len(board)):
        for b in range(len(board)):
            for c in range(len(board)):
                if setIsValid([board[a],board[b],board[c]], board) and a!=b and a!=c and b!=c:
                    return False
    return True
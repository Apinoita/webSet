import websockets
import asyncio
import gameLogic

#message types
"""
Server:
bo=board esim.   bo;[[1,1,1,1]:[1,1,1,1]:[1,1,1,1]:[1,1,1,1]]
rc=remove cards esim.   rc;[[1,1,1,1]:[1,1,1,1]:[1,1,1,1]:[1,1,1,1]]
ac=add cards esim.   ac;[[1,1,1,1]:[1,1,1,1]:[1,1,1,1]:[1,1,1,1]]
sc=score esim sc;{1:1,2:5}
cn=connect cn:playerId

ed=end


Client:
aa=add action
sa=submit action


"""

HOST_ADDRESS = "127.0.0.1"
PORT = 8080

deck = gameLogic.createDeck()
board = gameLogic.createBoard(deck)

connected = set()
WSToPlayerId={}
playerPoints = {}

def stringFromCardList(l:list[list[int]]) -> str:
    string="["
    for card in l:
        string+=str(card)+":"
    return string.removesuffix(":") + "]"        

def cardlistFromString(s:str):
    cards=[]
    try:
        s=s.split(":")
        print(s)
        for i in range(len(s)):
            cards.append([])
            s[i] = s[i].strip("[] ")
            s[i] = s[i].split(",")
            for ia in range(gameLogic.attributeNumber):
                cards[i].append(int(s[i][ia]))
    except IndexError:
        return []
    except ValueError:
        return []
    return cards


def getNewId():
    i=0
    while (i in WSToPlayerId .values()):
        i+=1
    return i

def addNewPlayer(websocket):
    WSToPlayerId[websocket] = getNewId()
    playerPoints[WSToPlayerId[websocket]] = 0

async def msgAll(msg):
    for conn in connected:
        await conn.send(msg)

async def handleMessage(message:str, websocket):
    if len(message)>2 and ";" in message:
        if message.startswith("sa"):
            message=message.removeprefix("sa;")
            cards = cardlistFromString(message)
            if gameLogic.setIsValid(cards, board):
                gameLogic.removeSetFromBoard(cards, board)
                if len(board)<12:
                    addedCards = gameLogic.drawNFromDeckToBoard(deck, board, gameLogic.optionsPerAttribute)
                else:
                    addedCards = []
                playerPoints[WSToPlayerId[websocket]] += 1
                while gameLogic.noSetsInBoard(board) and len(deck)!=0:
                    for i in range(gameLogic.optionsPerAttribute):
                        addedCards.append(gameLogic.drawOneFromDeckToBoard(deck, board))
                await msgAll(f"rc;{stringFromCardList(cards)}")
                await msgAll(f"ac;{stringFromCardList(addedCards)}")
                await msgAll(f"sc;{playerPoints}")

                if gameLogic.noSetsInBoard(board) and len(deck)==0:
                    await msgAll("en")

            

async def clientConnect(websocket):
    if websocket not in connected:
        connected.add(websocket)
        addNewPlayer(websocket)
        print("client connected")
    try:
        await websocket.send(f"cn;{WSToPlayerId[websocket]}")
        await websocket.send(f"bo;{stringFromCardList(board)}")
        await msgAll(f"sc;{playerPoints}")
        async for message in websocket:
            await handleMessage(message, websocket)
    except websockets.exceptions.ConnectionClosed:
        print("cilent disconnected (abnormally)")
    finally:
        connected.remove(websocket)
        playerPoints.pop(WSToPlayerId[websocket])
        WSToPlayerId.pop(websocket)



async def main():
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    startServer = await websockets.serve(clientConnect, HOST_ADDRESS, PORT)
    print(f"Listening on {HOST_ADDRESS}:{PORT}")
    await asyncio.Future()
asyncio.run(main())

import asyncio
import json
import websockets
import NAV
import ast

## receiving data as a client to the node server
# async def hello():
#     async with websockets.connect('ws://192.168.1.143:8002') as websocket:
#
#         name = input("What's your name? ")
#         await websocket.send(name)
#         print("> {}".format(name))
#
#         greeting = await websocket.recv()
#         print("< {}".format(greeting))
#
# asyncio.get_event_loop().run_until_complete(hello())


### pre-process - for the POC demo
with open('10_6_2017_15_55_55_22.json') as data_file:
    set1 = json.load(data_file)

count = 0
arrLen = 60
set1DictList = []

while count < arrLen:
    listEntry = {}
    listEntry["val"] = ast.literal_eval(set1[count]["val"])
    set1DictList.append(listEntry)
    count += 1
set1ProcessedJSON = NAV.SVR_process_monotypeAlt(set1DictList)
processed = json.loads(set1ProcessedJSON)
displacementProcessedJSON = NAV.calcLinearDisplacement(processed)

## sending data as a server to the react client
async def send(websocket, path):
    i = 0
    while True:
        if i < 60:
            status = 'now sending data point ' + str(i)
            await websocket.send(status)
            now = {}
            now["time"] = displacementProcessedJSON["time"][i]
            now["x-disp"] = displacementProcessedJSON["xDisplacement"][i]
            now["y-disp"] = displacementProcessedJSON["yDisplacement"][i]
            now["z-disp"] = displacementProcessedJSON["zDisplacement"][i]
            # now = datetime.datetime.utcnow().isoformat() + ' this is message # ' + str(i)
            toSend = json.dumps(now)
            ## websocket.send(str) can only take strings/jsons
            await websocket.send(toSend)
            i += 1
        else:
            toSend = 'end of the current batch, position ' + str(i) + ' not available'
            await websocket.send(toSend)
        ## await asyncio.sleep(time) sets the refresh rate
        await asyncio.sleep(0.5)

## websockets.serve(function name, your IP address, your port #)
## use this to send stuff to front-end
start_server = websockets.serve(send, '127.0.0.1', 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
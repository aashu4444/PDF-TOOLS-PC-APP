import json
import asyncio
import time

def long():
    time.sleep(4)

def acour(file):
    long()

    while True:
        text,s = (yield),(yield)

        # f.write(json.dumps({"name":name, "date":date}))
        print("You gave -", text, s)

        print("done")

ins = acour("myfiles.json")
next(ins)
ins.send("hii")
ins.send("hii", "g")
ins.send("hii", "g")

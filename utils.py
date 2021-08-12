import json

def toProcessText(text):
    splitted = text.split(" ")
    sentance = ""
    word = splitted[0]

    if word.endswith("e"):
        word = word[0:len(word)-1] + "ing"
    else:
        word += "ing"

    sentance += word + " "
    for i in " ".join(splitted[1:]):
        sentance += i


    return sentance


def toCompleteText(text):
    splitted = text.split(" ")
    sentance = ""
    word = splitted[0]

    if word.endswith("y"):
        word = word[0:len(word)-1] + "ied"
    elif word.endswith("e"):
        word += "d"
    else:
        word += "ed"

    for i in splitted[1:]:
        sentance += i + " "

    sentance += word

    return sentance

def writeSettings(data):
    with open("settings.json", "w") as f:
        f.write(data)

def readSettings():
    with open("settings.json", "r") as f:
        return json.loads(f.read())
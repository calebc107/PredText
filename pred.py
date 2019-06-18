import random
import ujson as json

from blist import *

import common

dictionary = []


class Word:
    body = ""
    posts = []

    def __init__(self, body, post):
        self.posts = [[post, 1]]
        self.body = body

    def __str__(self):
        return self.body

    def pickpost(self):
        total = 0
        if self.body != "":
            self.posts.sort(key=lambda x: x[1], reverse=True)
        for item in self.posts:
            total += item[1]
        rand = random.random()
        i = random.randint(0,len(self.posts)-1)
        return self.posts[i][0],self.posts[i][1]/total

    def addPost(self, str):
        i = bifindstring(self.posts, str, 0, len(self.posts) - 1)
        if i < len(self.posts) and self.posts[i][0] == str:
            self.posts[i][1] += 1
            return
        self.posts.insert(i, [str, 1])


def findword(wordbody):
    return bifindword(dictionary, wordbody, 0, len(dictionary) - 1)


def bifindword(collection, item, l, r):
    m = int((l + r) / 2)
    if l > r:
        return l
    elif collection[m].body == item:
        return m
    elif collection[m].body < item:
        return bifindword(collection, item, m + 1, r)
    else:
        return bifindword(collection, item, l, m - 1)


def bifindstring(collection, item, l, r):
    m = int((l + r) / 2)
    if l > r:
        return l
    elif collection[m][0] == item:
        return m
    elif collection[m][0] < item:
        return bifindstring(collection, item, m + 1, r)
    else:
        return bifindstring(collection, item, l, m - 1)


def sentancetowords(sentence2):
    if sentence2.lstrip().endswith("?"):
        return
    sentence = common.sanitize(sentence2)
    words = sentence.split(' ')
    for i in range(0, len(words)):
        if i < len(words) - 1 and words[i + 1] != "" and words[i] != "":
            body = words[i] + " " + words[i + 1]
        else:
            body = words[i]
        if body == "":
            continue
        post = ""
        if i == 0:
            dictionary[0].addPost(body)
        if i + 2 < len(words) and words[i + 2] != "":
            post = words[i + 2]
        index = findword(body)
        if index >= len(dictionary) or dictionary[index].body != body:
            newword = Word(body, post)
            newword.posts = blist()
            newword.addPost(post)
            dictionary.insert(index, newword)
        else:
            dictionary[index].addPost(post)


def LoadDB(count):
    global dictionary
    w = Word("", "")
    w.posts = blist()
    dictionary = blist()
    dictionary.insert(0, w)
    with open("comments.txt") as infile:
        loadedlines = 0
        for line in infile:
            if loadedlines > count:
                break
            try:
                comment = json.loads(line)
                sentancetowords(comment['data']['body'])
                loadedlines += 1
                print("\r" + 'loaded {} lines out of {} ({:.2f}%)'.format(loadedlines, count,
                                                                          (loadedlines / count * 100)),
                      end='')
            except Exception as e:
                continue


def LoadDictionary():
    global dictionary
    dictionary = []
    with open("pred.txt", "r") as f:
        for line in f:
            linedic = json.loads(line)
            word = Word(linedic['body'], "")
            word.posts = []
            for post in linedic['posts']:
                word.posts.append(post)
            dictionary.append(word)
        dictionary.sort(key=lambda x: x.body)


def prune():
    global dictionary
    originalSize = len(dictionary)
    print("Trimming unused posts")
    i=0
    while i < len(dictionary[0].posts):
        j = findword(dictionary[0].posts[i][0])
        if len(dictionary[j].posts)==1 and dictionary[j].posts[0][0]=="":
            dictionary[0].posts.pop(i)
            i-=1
        i+=1

    for word in dictionary:
        if word.body=="":
            continue
        total = 0
        for post in word.posts:
            total += post[1]
        i=0
        rt=0
        word.posts.sort(key=lambda x: x[1], reverse=True)
        while i< len(word.posts):
            if rt / total > .2:
                word.posts= word.posts[0:i]
                break
            rt+=word.posts[i][1]
            i+=1

    for _ in range(0,3):
        keep = [0 for __ in dictionary]
        print("Pass {}/{}".format(i,3))

        print("Marking used words")
        for word in dictionary:
            body2=""
            if " " in word.body:
                words=word.body.split(" ")
                body2=words[1]+" "
            for post in word.posts:
                
                i = findword(body2+post[0])
                try:
                    keep[i] = 1
                except:
                    print ("Error: "+body2+post[0]+" doesnt exist!")

        print("Creating new dictionary without unused words")
        newdic = []
        for i in range(0, len(keep)):
            if keep[i]:
                newdic.append(dictionary[i])
        dictionary = newdic

    print("{} -> {} words".format(originalSize, len(dictionary)))


def SaveDictionary():
    f = open("pred.txt", "w+")
    for word in dictionary:
        line = json.dumps(word.__dict__) + "\n"
        f.write(line)
    f.close()


def makesentance(max):
    sentence = ""
    blank = dictionary[findword("")]
    post = blank.pickpost()
    firstword = dictionary[findword(post[0])]
    lastword = firstword
    sentence = firstword.body
    wordcount = 1
    confidence = 0  # post[1]
    while wordcount <= max:
        pickedpost = lastword.pickpost()
        if pickedpost[0] == "":
            confidence += pickedpost[1]
            return sentence,0.5 # confidence / wordcount
        newword = pickedpost[0]
        sentence = sentence + " " + newword
        words = sentence.split(" ")
        lastword = dictionary[findword(words[-2] + " " + words[-1])]
        wordcount += 1
        confidence += pickedpost[1]
    return "", 0


def getSentence():
    return getSentence2(2, 7, 10)


def getSentence2(min, max, bestoutof):
    bestc = 0
    best = ""
    while True:
        if bestoutof <= 0 and best != "":
            return best
        sentence = makesentance(max / 2 + 1)
        if min <= len(sentence[0].split(" ")) <= max and not common.hasslur(sentence[0]) and not isfragment(
                sentence[0]) and not hasPhraseToAvoid(
            sentence[0]):
            bestoutof -= 1
            if 1 > sentence[1] > bestc:
                best = sentence[0]
                bestc = sentence[1]


articles = ["a", "the", "an"]


def isfragment(string):
    words = string.split(" ")
    for article in articles:
        if words[-1] is article:
            return True
    return False


phrases = ["questions or concerns"]


def hasPhraseToAvoid(string):
    for phrase in phrases:
        if phrase in string:
            return True
    return False

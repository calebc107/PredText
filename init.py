#!/usr/bin/python3
import json

import common
import pred

comments = common.DownloadThings("https://oauth.reddit.com/r/all/comments.json", 20000)
f = open("comments.txt", "w+")
for comment in comments:
    f.write(json.dumps(comment) + "\n")
f.close()
pred.LoadDB(20000)
pred.SaveDictionary()
pred.prune()

#!/usr/bin/python3
import pred

pred.LoadDictionary()
print("Press enter for a new sentance")
while True:
     input()
     print(pred.getSentence2(3, 8, 5))

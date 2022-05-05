from functools import reduce


myList = ['think', 'pad']
print(myList)
m = map(str.title, myList)
print(m)
lm=list(m)
print(lm)
r= reduce(lambda x,y: x+y, lm)
print(r)

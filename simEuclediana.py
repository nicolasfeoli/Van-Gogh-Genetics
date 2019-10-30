
from math import*

def euclidean_distance(x,y):

    return sqrt(sum(pow(a-b,2) for a, b in zip(x, y)))

#x = [1,2,3,4,5,6,7,8,9]
#y = [9,8,7,6,5,4,3,2,1]

x =[1,2,3,4,5,6,7,8,9]
y = [1,2,3,4,5,6,7,8,8.9]
print euclidean_distance(x,y) 
#function to sort zlist in descending order
def zListSort(x):
    if x[0]>x[1] and x[1]>x[2] and x[0]>x[2]:
        x=[x[0],x[1],x[2]]
    elif x[0]>x[2] and x[2]>x[1] and x[0]>x[1]:
        x=[x[0],x[2],x[1]]
    elif x[1]>x[0] and x[0]>x[2] and x[1]>x[2]:
        x=[x[1],x[0],x[2]]
    elif x[1]>x[2] and x[2]>x[0] and x[1]>x[0]:
        x=[x[1],x[2],x[0]]
    elif x[2]>x[0] and x[0]>x[1] and x[2]>x[1]:
        x=[x[2],x[0],x[1]]
    elif x[2]>x[1] and x[1]>x[0] and x[2]>x[0]:
        x=[x[2],x[1],x[0]]
    return x

#insert z-values in the array below
zlist=['c','b','a']
#sorts zlist in descending order
zlist = zListSort(zlist)

print(zlist)
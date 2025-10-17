value="""
# OBJ
# 
v  $2 $1 $1
v  $2 $1 $2
v  $2 $2 $1
v  $2 $2 $2
v  $1 $2 $1
v  $1 $1 $2
v  $1 $1 $1
v  $1 $2 $2
f 1 2 3
f 2 4 3
f 5 6 7
f 5 8 6
f 4 8 5
f 3 4 5
f 7 6 2
f 7 2 1
f 4 2 6
f 8 4 6
f 7 1 3
f 7 3 5

"""
print("\033c\033[43;30m\nW?->\n")
ww=input()
w=float(ww)
w1=w*1.00
w2=w*-1.00
w3=w*2.00
w1=str(w1)
w2=str(w2)
w3=str(w3)
value=value.replace("$1",w1)
value=value.replace("$2",w2)
value=value.replace("$3",w3)
ww="cube"+ww+".obj"
f1=open(ww,"w")
f1.write(value)
f1.close()

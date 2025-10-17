value="""
# OBJ
# 
v  $1 $2 $1
v  $3 $3 $2
v  $3 $3 $3
v  $2 $3 $1
f 1 2 3
f 2 1 3
f 3 1 2
f 1 2 4
f 2 1 4
f 4 1 2
f 1 3 4
f 3 1 4
f 4 1 3
f 2 3 4
f 3 2 4
f 4 2 3


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
ww="pyramide"+ww+".obj"
f1=open(ww,"w")
f1.write(value)
f1.close()

import os

try:
        b=open("arquivos/natual.dat", 'r') #try open 'nautal'
        b.close()
except IOError:
        b=open("arquivos/natual.dat", 'w+') #create a 'natual'
        b.write("1")
        b.close()

while True:
        try:
                a=open("arquivos/arq.gcode",'r') #try open file
                a.close()
                b=open("arquivos/natual.dat", 'r') #open 'natual'
                c = b.readline() #copy line
                b.close()
                n = "arquivos/" + c + ".gcode" #define name of file
                os.rename("arquivos/arq.gcode",n) #rename file
                num=c
                inteiro=int(num)
                e = inteiro + 1 #add 1 to natual
                b = open ("arquivos/natual.dat", 'w+')
                b.write(str(e))
                b.close()
        except IOError:
                d=0


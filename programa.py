#-*-coding:utf-8-*-
import shutil
import serial
import time
import os
import math
def mudarvalorlinha(inp,letra,vnovo): #change value of some parameter of g-code
        cond1=0
        cond2=0
        for l in inp:
                if cond1 == 1 and (l == ' ' or l == '\n'):
                        cond1 = 0
                if cond1 == 1 and cond2 == 0:
                        out = out + vnovo
                        cond2 = 1
                if cond1 == 0:
                        try:
                                out = out + l
                        except UnboundLocalError:
                                out = l
                if l == letra:
                        cond1 = 1
        return out
def procurarletra(linha,letra): #search letter in line and return a value after the word or -100 if dont find the letter
        cond1=0
        cond2=0
        for l in linha:
                if cond1 == 1 and (l == ' ' or l == '\n'):
                        cond2 = 1
                if cond1 == 1 and cond2 == 0:
                        try:
                                num = num + l
                        except UnboundLocalError:
                                num = l
                if l == letra:
                        cond1 = 1
        if cond1 == 1:
                return float(num)
        if cond1 == 0:
                return -100
def procurarletras(linha,letra1,letra2): #search two letters in one line
        if linha.find(letra1) >= 0 and linha.find(letra2) >= 0:
                return 1
        else:
                return 0
def conversor(inp,out): #function remove ; and spaces of g-code
        f = open (inp, 'r') #open file
        atemp = f.readlines() #copy lines
        f.close #close file
        f = open (out, 'w+')
        cond = 0
        for line in atemp:
                l = (line.strip()).split(';')[0]
                if len(l) > 3:
                        if cond == 1:
                                f.write('\n'+l) #copy the rest of liles without ;
                        else:
                                f.write(l)  #copy the first line without \n before and removing ;
                                cond = 1
        f.close()
def ler (diretorio): #function read files
        file = open (diretorio, 'r')
        b = file.readlines()
        file.close()
        i=1
        while (i>=0):
            c = b [len(b)-i]
            if (len(c)>=2):
                i=-1
            else:
                i = i + 1   
        return c
def lernum (diretorio): #function read files
        file = open (diretorio, 'r')
        b = file.readlines()
        file.close()
        i=1
        while (i>=0):
            c = b [len(b)-i]
            try:
                d = float(c)
                i=-1
            except ValueError:
                i = i + 1
        return c
def gravar(arquivo,diretorio): #function write in files
        file = open (diretorio, 'a+')
        file.write(arquivo+'\n')
        file.close()
def conversor2(inp,out): #remove printed part of g-code and change form of calibration
        a=open(inp,'r')
        atemp =  a.readlines()
        a.close()
        time.sleep(1)
        newfile=open(out,'w+')
        cond=0
        cond2=0
        cond3=0
        cond4=0
        xy=ler('tmp/xy.dat')
        z=float(lernum('tmp/z.dat'))
        e=float(lernum('tmp/E.dat'))
        newfile.write('G28 X0 Y0')
        for line in atemp:
                l=line.strip()
                if cond == 0:
                        if procurarletra(l,'G') != 28 and procurarletras(l,'G','Z') == 0 and procurarletra(l,'G') != 32 and procurarletra(l,'G') != 29 and ( procurarletra(l,'E') >= 0 or procurarletra(l,'E') == -100): #delete Z changes 
                                newfile.write('\n' + l)
                        if procurarletras(l,'X','Y') == 1 and procurarletras(l,'G','Z') == 0:
                                cond = 1
                if cond2 == 0:
                        if procurarletra(l,'Z') == z: #find Z
                                cond2 = 1
                if cond3 == 0:
                        if cond2 == 1 and (l+'\n') == xy: #find XY (after find Z)
                                cond3 = 1
                if cond3 == 1:
                        if procurarletra(l,'G') == 92 and procurarletra(l,'E') == 0:
                                cond4 = 1
                        if procurarletra(l,'Z') > 0 and procurarletra(l,'E') > 0 and cond4 == 0:
                                tmp = mudarvalorlinha(l,'E',str(round(procurarletra(l,'E')-float(lernum('tmp/E.dat')),6)))
                                newfile.write('\n' + mudarvalorlinha(tmp,'Z',str(round(procurarletra(l,'Z')-float(lernum('tmp/z.dat')),6)))) 
                        elif procurarletra(l,'E') > 0 and cond4 == 0:
                                newfile.write('\n' + mudarvalorlinha(l,'E',str(round(procurarletra(l,'E')-float(lernum('tmp/E.dat')),6))))
                        elif procurarletra(l,'Z') > 0:
                                newfile.write('\n' + mudarvalorlinha(l,'Z',str(round(procurarletra(l,'Z')-float(lernum('tmp/z.dat')),6))))
                        else:
                                newfile.write('\n' + l) #copy restant of lines
        a.close()
def direxiste(diretorio): #verify if directory exist 
        try:
                ler(diretorio)
                return 1
        except:
                return 0
def imprimir(line,impressora):
        l = line.strip() # copy line
        print ('Enviando: ' + l)# shows what is being sent
        l2 = l + "\n" # add enter
        impressora.write(l2.encode()) # send g-code to printer
        grbl_out = impressora.readline() # wait for printer out
        if procurarletra(l,'M') == 104: #discovers material and define your density (you can change this)
                temperatura = procurarletra(l,'S')
                if temperatura <= 220: #temp<220 PLA
                        gravar("1.24",'tmp/densidade.dat')
                        print ("Material: PLA")
                        gravar("PLA",'tmp/material.dat')
                else: #temp>220 ABS
                        gravar("1.03",'tmp/densidade.dat')
                        print ("Material: ABS")
                        gravar("ABS",'tmp/material.dat')
        if procurarletra(l,'M') == 82:
                 gravar('sim','tmp/Eabs.dat')
        if procurarletra(l,'Z') > 0: #save z
                gravar(str(procurarletra(l,'Z')),'tmp/z.dat')
        if procurarletras(l,'X','Y') == 1: #save X, Y, E e define used mass
                if procurarletra(l,'E') > 0:
                        comprimento = procurarletra(l,'E')/10
                        massa = comprimento * math.pi * ((0.175/2)**2) * float(lernum('tmp/densidade.dat'))
                        try:
                                Eabs=ler('tmp/Eabs.dat')
                                gravar(str(procurarletra(l,'E')),'tmp/E.dat')
                                massat = massa
                        except IOError:
                                massat = float(lernum('tmp/massa.dat')) + massa
                        print ("Massa Utilizada: " + str(massat))
                        gravar(str(massat),'tmp/massa.dat')
                gravar(l,'tmp/xy.dat')
        print ('Operação: ' + str(grbl_out.strip()) +'\nProgresso: '+ str(porcentagem) + '%')
        if procurarletras(str(grbl_out.strip()),'T:','B:') == 1 and procurarletras(l,'X','Y') == 1:
                while procurarletras(str(grbl_out.strip()),'T:','B:') == 1: #if the temperature is different from the should be, the program wait
                        l = 'G1 X76.054 Y91.386 F7800.000'
                        l2 = l + '\n'
                        print ('Enviando: ' + l)
                        time.sleep(0.1)
                        s.write(l2.encode()) # send gcode to printer
                        grbl_out = s.readline()
                        print ('Operação: ' + str(grbl_out.strip()) +'\nProgresso: '+ str(porcentagem) + '%')
while True:
        true=0
        while true==0: #try copy file from 'arquivos' to be printed
                try: #verify if some file being printed 
                        a=open('arq.gcode','r') 
                        a.close()
                        true=1
                except IOError: #try copy a file from 'arquivos' folder
                        try:
                                b=open('natual.dat', 'r')
                                b.close()
                        except IOError:
                                b=open('natual.dat', 'w+')
                                b.write("1")
                                b.close()
                        b=open('natual.dat', 'r')
                        c = b.readline()
                        b.close()
                        n = "arquivos/" + c + ".gcode"
                        try:
                                shutil.copy(n,"arq.gcode")
                                num=c
                                inteiro=int(num)
                                e = inteiro + 1
                                b = open ('natual.dat', 'w+')
                                b.write(str(e))
                                b.close()
                        except IOError:
                                d=0
        s = serial.Serial('COM16',115200) #open serial port
        print ("Iniciando...")
        serialcmd="\r\n\r\n" #turn printer on
        s.write(serialcmd.encode())
        time.sleep(5)   # wait printer
        s.flushInput()  # Flush startup text in serial input
        try:
                mas = open('tmp/massa.dat','r')
                mas.close()
        except IOError:
                os.mkdir('tmp')
                gravar('0','tmp/massa.dat')
        try: #resume print
                f = open('tmp/temporario.gcode','r')
                numeroLinhas=len(f.readlines())
                f.close()
                conversor2('tmp/temporario.gcode','tmp/temporario.gcode') #open file and convert it
                f = open('tmp/temporario.gcode','r')
                linhaAtual = int(lernum('tmp/linhaAtual.dat'))-1
                for line in f:
                        if direxiste('pausar.dat') == 1:
                                while direxiste('pausar.dat') == 1:
                                        time.sleep(0.2)
                                        if direxiste('cancelar.dat') == 1:
                                                break
                        if direxiste('cancelar.dat') == 1:
                                break
                        linhaAtual=linhaAtual+1 #add 1 in line contage
                        gravar (str(linhaAtual),'tmp/linhaAtual.dat')
                        porcentagem=round(float(linhaAtual)*100/numeroLinhas,3) #define %
                        gravar(str(porcentagem)+"%",'tmp/porcentagem.dat') #write %
                        imprimir(line,s)
                f.close()
        except IOError: #new print
                conversor('arq.gcode','tmp/temporario.gcode')
                f = open('tmp/temporario.gcode','r')
                numeroLinhas=len(f.readlines())
                f.close()
                f = open('tmp/temporario.gcode','r')
                linhaAtual = 0
                for line in f:
                        if direxiste('pausar.dat') == 1:
                                while direxiste('pausar.dat') == 1:
                                        time.sleep(0.2)
                                        if direxiste('cancelar.dat') == 1:
                                                break
                        if direxiste('cancelar.dat') == 1:
                                break
                        linhaAtual=linhaAtual+1 #add 1 in line contage
                        gravar (str(linhaAtual),'tmp/linhaAtual.dat')
                        porcentagem=round(float(linhaAtual)*100/numeroLinhas,3) #define %
                        gravar(str(porcentagem)+"%",'tmp/porcentagem.dat') #write %
                        imprimir(line,s)
                f.close()
        imprimir('M117 ENTER TO NEXT',s) #send a message
        shutil.rmtree('tmp') #remove /tmp
        os.remove('arq.gcode') #remove file
        try:
                os.remove('cancelar.dat')
        except:
                arqdelet=0
        try:
                os.remove('pausar.dat')
        except:
                arqdelet=0
        s.close()


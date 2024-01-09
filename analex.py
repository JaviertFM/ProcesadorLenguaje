#!/usr/bin/env python

import componentes
#import errores
import flujo
import string
import sys
import os
from sys import argv

class Analex:
#############################################################################
##  Conjunto de palabras reservadas para comprobar si un identificador es PR
#############################################################################
    PR = frozenset(["PROGRAMA", "VAR", "ENTERO", "REAL", "BOOLEANO", "INICIO", "FIN", "SI", "ENTONCES", "SINO", "MIENTRAS", "HACER", "LEE", "ESCRIBE", "Y", "O", "NO", "CIERTO","FALSO"])

 ############################################################################
 #
 #  Funcion: __init__
 #  Tarea:  Constructor de la clase
 #  Parametros:  flujo:  flujo de caracteres de entrada
 #  Devuelve: --
 #
 ############################################################################
    def __init__(self, flujo):
        self.flujo= flujo
        self.poserror= 0
        self.nlinea=1


 ############################################################################
 #
 #  Funcion: TrataNum
 #  Tarea:  Lee un numero del flujo
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #              ch: primera caractera tratar
 #  Devuelve: El valor numerico de la cadena leida
 #
 ############################################################################
    def TrataNum(self,flujo, ch):
        l=ch
        ch = flujo.siguiente()

        #Completar
        while(ch == "0" or ch == "1" or ch == "2" or ch == "3" or ch == "4" or ch == "5" or ch == "6" or ch == "7" or ch == "8" or ch == "9"):
            l += ch
            ch = flujo.siguiente()

        if (ch == "."):
            l += ch
            ch = flujo.siguiente()
            while (ch == "0" or ch == "1" or ch == "2" or ch == "3" or ch == "4" or ch == "5" or ch == "6" or ch == "7" or ch == "8" or ch == "9"):
                l += ch
                ch = flujo.siguiente()
            flujo.devuelve(ch)
            tipo = "<type 'float'>"
            return componentes.Numero(l, self.nlinea, tipo)
        else:
            flujo.devuelve(ch)
            tipo = "<type 'int'>"
            return componentes.Numero(l, self.nlinea, tipo)






 ############################################################################
 #
 #  Funcion: TrataIdent
 #  Tarea:  Lee identificadores
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #              ch: Primer caracter a tratar
 #  Devuelve: Devuelve una cadena de caracteres que representa un identificador
 #
 ############################################################################
    def TrataIdent(self,flujo, ch):
        l = ch
        ch = flujo.siguiente()
        while ((ord(ch) >= 65 and ord(ch) <= 90) or (ord(ch) >= 97 and ord(ch) <= 122) or (ord(ch)>=48 and ord(ch)<=57)):
                l += ch
                ch = flujo.siguiente()
        flujo.devuelve(ch)
        if (l in self.PR):
            return componentes.PR(l,self.nlinea)
        else:
            return componentes.Identif(l, self.nlinea)
  #Completar
#asadfsdaf234 = 34
  # return l

  ############################################################################
  #
  #  Funcion: TrataIdent
  #  Tarea:  Lee identificadores
  #  Prametros:  flujo:  flujo de caracteres de entrada
  #              ch: Primer caracter a tratar
  #  Devuelve: Devuelve una cadena de caracteres que representa un identificador
  #
  #  TrataComent
  ############################################################################

    def TrataComent(self, flujo):
        ch = flujo.siguiente()
        while ((ch != "\n") or (ch != "\r")):
            ch = flujo.siguiente()

  #Completar

 ############################################################################
 #
 #  Funcion: EliminaBlancos
 #  Tarea:  Descarta todos los caracteres blancos que hay en el flujo de entrada
 #  Prametros:  flujo:  flujo de caracteres de entrada
 #  Devuelve: --
 #
 ############################################################################
    def EliminaBlancos(self,flujo):
        l = flujo.cadena()
        return l.replace(" ","")
#Completar

 ############################################################################
 #
 #  Funcion: Analiza
 #  Tarea:  Identifica los diferentes componentes lexicos
 #  Prametros:  --
 #  Devuelve: Devuelve un componente lexico
 #
 ############################################################################

    def Analiza(self):
         l = ""
         ch = self.flujo.siguiente();
         if ch == " ":
         ##acciones si hemos encontrado un blancoi
         #Los blancos se ignoran
            return self.Analiza()
         elif ch == "\r":
         # acciones si hemos encontrado un salto de linea
         #Los saltos de linea se ignoran
            self.nlinea = self.nlinea + 1
            return self.Analiza()


         # ANALIZA SI ES UN NUMERO
         elif (ch == "0" or ch == "1" or ch == "2" or ch == "3" or ch == "4" or ch == "5" or ch == "6" or ch == "7" or ch == "8" or ch == "9"):
            numero = self.TrataNum(self.flujo,ch)
            return numero


         # ANALIZA SI ES UN COMENTARIO
         elif (ch == "%"):
             ch = self.flujo.siguiente()
             if (ch == "%"):
                self.TrataComent(self.flujo)
                print("linea de comentario")
             else:
                operador = componentes.OpMult(ch, self.nlinea)
                self.flujo.devuelve(ch)
                return operador



         # EMPIEZA LA SECCIÓN DE DIFERENCIAR OPERADORES RELACIONALES

         elif ( ch == "<"):
             op = ch
             ch = self.flujo.siguiente()
             if (ch == ">" or ch == "="):
                 op += ch
                 operador = componentes.OpRel(op,self.nlinea)
                 return operador
             else:
                 self.flujo.devuelve(ch)
                 operador = componentes.OpRel(op,self.nlinea)
                 return operador

         elif (ch == "="):
             oprel =  componentes.OpRel(ch,self.nlinea)

             return oprel
         elif (ch == ">"):
             op = ch
             ch = self.flujo.siguiente()
             if (ch == "="):
                 oprel = componentes.OpRel(op+ch,self.nlinea)

                 return oprel
             else:
                 self.flujo.devuelve(ch)
                 oprel = componentes.OpRel(op,self.nlinea)

                 return oprel

         # EMPIEZA LA SECCION DE DIFERENCIAR LOS SÍMBOLOS
         elif (ch == ";"):
             simbolo = componentes.Simbolo("PtoComa",self.nlinea)

             return simbolo

         elif (ch == "("):
             simbolo = componentes.Simbolo("ParentAp",self.nlinea)

             return simbolo

         elif (ch == ")"):
             simbolo = componentes.Simbolo("ParentCi",self.nlinea)
             return simbolo

         elif (ch == ","):
             simbolo = componentes.Simbolo("Coma",self.nlinea)

             return simbolo


         elif (ch == ":"):
             ch = self.flujo.siguiente()
             if(ch == "="):
                 simbolo = componentes.OpAsigna(":=",self.nlinea)
             else:
                self.flujo.devuelve(ch)
                simbolo = componentes.Simbolo("DosPtos",self.nlinea)

             return simbolo
         elif(ch=="."):
            simbolo = componentes.Simbolo("Pto",self.nlinea)
            return simbolo

        #SECCION PARA LOS IDENTIFICADORES Y LAS PALABRAS RESERVADAS

         elif (len(ch) != 0 and((ord(ch) >= 65 and ord(ch) <= 90) or (ord(ch) >= 97 and ord(ch) <= 122))):
             palabra = self.TrataIdent(self.flujo, ch)
             return palabra

        #SECCION PARA OPERADORES ARITMÉTICOS

         elif (ch == "+" or ch == "-"):
             simbolo = componentes.OpAdd(ch,self.nlinea)
             return simbolo

         elif (ch == "*" or ch == "/"):
             simbolo = componentes.OpMult(ch,self.nlinea)
             return simbolo

         # completar aqui para todas las categorias lexicas
         elif ch == "\n":
             ## acciones al encontrar un salto de linea
             self.nlinea = self.nlinea + 1
             return self.Analiza()
         elif ch:
             # se ha encontrado un caracter no permitido
             print ("ERROR LEXICO  Linea " + str(self.nlinea) + " ::  Caracter " + ch + " invalido ")
             return self.Analiza()
         else:
             # el final de fichero
             return componentes.EOF()

############################################################################
#
#  Funcion: __main__
#  Tarea:  Programa principal de prueba del analizador lexico
#  Prametros:  --
#  Devuelve: --
#
############################################################################

if __name__=="__main__":
    script, filename=argv
    txt=open(filename)
    print ("PROGRAMA FUENTE %r"  % filename)
    i=0
    fl = flujo.Flujo(txt)
    analex=Analex(fl)
    c = analex.Analiza()
    while c.cat != "EOF":
        print (c)
        c = analex.Analiza()
    i = i + 1


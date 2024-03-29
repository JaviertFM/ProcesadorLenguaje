#!/usr/bin/env python

import string
import sys
######################################################################################
##
##  Define varias clases que definen cada uno de los diferentes componentes lexicos
##
##
##
######################################################################################

# Clase generica que define un componente lexico 
class Componente:

    def __init__(self):
        self.cat= str(self.__class__.__name__)

    def __str__(self):
        s=[]
        for k,v in self.__dict__.items():
          if k!= "cat": s.append("%s: %s" % (k,v))
        if s:
          return "%s (%s)" % (self.cat,", ".join(s))
        else:
          return self.cat

#definicion de las clases que representan cada uno de los componentes lexicos

#Algunas tendran camps adicionales para almacenar informacion importante (valor de un numero, etc)

#clases para los simbolos de puntuacion y operadores

class OpAsigna (Componente):
    def __init__(self, v, nl):
        Componente.__init__(self)
        self.valor = v
        self.linea = nl


# Clase que define la categoria OpAdd
class OpAdd(Componente):
    #debe almacenarse de que operador se trata
    def __init__(self, v, nl):
        Componente.__init__(self)
        self.valor = v
        self.linea = nl
# Clase que define la categoria OpMult
class OpMult(Componente):
    #Debe alnmacenarse que operador es
    def __init__(self, v, nl):
        Componente.__init__(self)
        self.valor = v
        self.linea = nl

#clases para representar los numeros.
#Puede dividirse en 2 para representar los enteros y los reales de forma independiente
#Si se opta por una sola categoria debe alamcenarse el tipo de los datos ademas del valor
class Numero (Componente):
    def __init__(self,valor,nl,tipo):
        Componente.__init__(self)
        self.valor = valor
        self.linea = nl
        self.tipo = tipo
  
#clases para representar los identificadores y palabras reservadas
class Identif (Componente):
  def __init__(self,v,nl):
    Componente.__init__(self)
    self.valor= v
    self.linea=nl

#Clase que reprresenta las palabras reservadas.
#Sera una clase independiente de los identificadores para facilitar el analisis sintactico
class PR(Componente):
  def __init__(self, v,nl):
      Componente.__init__(self)
      self.valor = v
      self.linea = nl


# Clase que define la categoria OpRel
#Debe alnmacenarse que operador es concretamente

class OpRel (Componente):
    def __init__(self, v, nl):
        Componente.__init__(self)
        self.valor = v
        self.linea = nl
class Simbolo(Componente):
    def __init__(self,v,nl):
        Componente.__init__(self)
        self.valor = v
        self.linea = nl
class EOF(Componente):
    def __init__(self):
        Componente.__init__(self)
#!/usr/bin/env python

class AST:
	def __str__(self):
		return self.arbol()

class NodoAsignacion(AST):
	def __init__(self, izda, exp, linea):
		self.izda = izda
		self.exp = exp
		self.linea = linea
		self.compsem()
	def compsem(self):
		pass
	def arbol(self):
		return '( "Asignacion"\n  "linea: %s" \n%s\n%s\n)' % (self.linea, self.izda, self.exp)

class NodoSi(AST):
	def __init__(self, exp, si, sino, linea):
		self.exp = exp
		self.si = si
		self.sino = sino
		self.linea = linea
		self.compsem()

	def compsem(self):
		pass
	def arbol(self):
		return '( "Si" "linea: %s" %s\n %s\n %s\n )' % (self.linea, self.exp, self.si, self.sino)

class NodoMientras(AST):
	def __init__(self, exp, inst, linea):
		self.exp = exp
		self.inst = inst
		self.linea = linea
		self.compsem()

	def compsem(self):
		pass
	def arbol(self):
		return '( "Mientras" "linea: %s" %s\n %s\n )' % (self.linea, self.exp, self.inst)

class NodoLee(AST):
	def __init__(self,var,linea):
		self.var = var
		self.linea = linea
		self.compsem()

	def compsem(self):
		if type(self.var) != type(NodoEntero) and type(self.var) != type(NodoReal):
			return ("El NodoLee no puede tener valores que no sean Entero o Real")
	def arbol(self):
		return '( "Lee" "linea: %s" %s )' % (self.linea, self.var)

class NodoEscribe(AST):
	def __init__(self, exp, linea):
		self.exp = exp
		self.linea = linea
		self.compsem()

	def compsem(self):
		if type(self.exp) != type(NodoExpresion):
			return ("El NodoEscribe no puede tener valores que no sean NodoExpresion")
	def arbol(self):
		return '( "Escribe" "linea: %s" %s )' % (self.linea, self.exp)

class NodoCompuesta(AST):
	def __init__(self, lsen, linea):
		self.lsen = lsen
		self.linea = linea
		self.compsem()

	def compsem(self):
		pass
	def arbol(self):
		r= ""
		for sent in self.lsen:
			r+= sent.arbol()+"\n"
		return '( "Compuesta"\n %s)' % r

class NodoComparacion(AST):
	def __init__(self, izq, dcha, linea, op):
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = None
		self.compsem()

	def compsem(self):
		pass
	def arbol(self):
		return '( "Comparacion" "op: %s" "tipo: %s" "linea: %s" \n %s\n %s\n)' % (self.op, self.tipo, self.linea, self.izq, self.dcha)

class NodoAritmetico(AST):
	def __init__(self,signo, izq, dcha, linea, op):
		self.signo = signo #Hemos añadido el signo de la expresion
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = None
		self.compsem()

	#Nuevo constructor para cuando no llega el signo, que lo ponga a + por defecto
	def __init__(self, izq, dcha, linea, op):
		self.signo = "+" 
		self.izq = izq
		self.dcha = dcha
		self.linea = linea
		self.op = op
		self.tipo = None
		self.compsem()

	def compsem(self):
		pass
	def arbol(self):
		return '( "Aritmetica" "signo: %s" "op: %s" "tipo: %s" "linea: %s" \n %s\n %s\n)' % (self.signo, self.op, self.tipo, self.linea, self.izq, self.dcha)

class NodoEntero(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.compsem()

	def compsem(self):
		aux = self.valor+".0"
		self.valor = aux

	def arbol(self):
		return '( "Entero" "valor: %s" "linea: %s" )' % (self.valor, self.linea)


class NodoReal(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.compsem()
	
	def compsem(self):
		pass
	def arbol(self):
		return '( "Real" "valor: %s"  "linea: %s" )' % (self.valor, self.linea)

class NodoBooleano(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.compsem()
	
	def compsem(self):
		if self.valor == "FALSO":
			self.valor = 0
		else:
			self.valor = 1
	def arbol(self):
		return '( "BOOLEANO" "valor: %s" "linea: %s" )' % (self.valor, self.linea)

class NodoAccesoVariable(AST):
	def __init__(self, var, linea, tipo):
		self.var = var
		self.linea = linea
		self.tipo = tipo
		self.compsem()

	def compsem(self):
		pass
	def arbol(self):
		return '( "AccesoVariable" "v: %s" "linea: %s" )' % (self.var, self.linea)

class NodoAccesoVector(AST):
	def __init__(self, vect, exp, linea, tipo):
		self.vect = vect
		self.exp = exp
		self.linea = linea
		self.tipoVar = tipo
		self.compsem()

	def compsem(self):
		pass
	def arbol(self):
		return '( "AccesoVector" "tipo: %s" "linea: %s" %s\n %s\n)' % (self.tipo, self.linea, self.vect, self.exp)


#############################
#							#
#		NUEVOS NODOS		#
#							#
#############################

class NodoNegacion(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.compsem()

	def compsem(self):
		pass
	def arbol(self):
		return '( "NodoNegacion" "NO valor:%s "linea: %s" )' % (self.valor.arbol(), self.linea)


class NodoRelacion(AST):
	def __init__(self, dcha, izda, linea,op):
		self.dcha = dcha
		self.izda = izda
		self.linea = linea
		self.op = op
		self.compsem()

	def compsem(self):
		pass

	def arbol(self):
		#TODO Cambiar la forma de mostrar el árbol
		return '( "NodoExpresion" "exp1:%s" "exp2:%s" "op: %s" "linea: %s" )' % (self.dcha,self.izda,self.op ,self.linea)

class NodoInicio(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.compsem()

	def compsem(self):
		pass
	def arbol(self):
		return '( "INICIO" %s "FIN" "linea: %s" )' % (self.valor.arbol(), self.linea)

class NodoPrograma(AST):
	def __init__(self,id, dcha, linea):
		self.id = id
		self.dcha = dcha
		self.linea = linea
		self.compsem()

	def compsem(self):
		pass
	def arbol(self):
		return '( "PROGRAMA" %s ";" %s "linea: %s" )' % (self.id,self.dcha.arbol(), self.linea)


class NodoId(AST):
	def __init__(self, valor,tipo, linea):
		self.valor = valor
		self.tipo = tipo
		self.linea = linea
		self.compsem()
	

	def compsem(self):
		pass

	def arbol(self):
		return '( id: %s, tipo:%s "linea: %s" )' % (self.valor,self.tipo, self.linea)


class NodoExpresion(AST):
	def __init__(self, valor, linea):
		self.valor = valor
		self.linea = linea
		self.compsem()

	def compsem(self):
		pass

	def arbol(self):
		return '( Expresion: %s "linea: %s" )' % (self.valor.arbol(), self.linea)


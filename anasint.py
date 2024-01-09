#!/usr/bin/env python

#import arboles

import componentes
import flujo
import analex
import sys
from sys import argv
import AST
#import errores

class Sintactico:
#Constructor de la clase que implementa el Analizador Sintactico
#Solicita el primer compnente lexico 
    def __init__(self, lexico):
        self.lexico= lexico
        self.token=self.lexico.Analiza()

        #diccionario tabla de simbolos

        self.tSimbolos = {}

    # Funcion que muestra los mensajes de error
    def Error(self, nerr, tok):
        if nerr == 1:
            print ("Linea: " + str(self.token.linea) + "  ERROR Se espera PROGRAMA")
        elif nerr==2:
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera IDENTIFICADOR")
        elif nerr ==3:
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera un PtoComa")
        elif nerr ==4:   
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera VAR") 
        elif nerr ==5:   
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera LEE o ESCRIBE") 
        elif nerr ==6:   
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera OpAsigna") 
        elif nerr ==7:   
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera ParentAp") 
        elif nerr ==8:   
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera ParentCi") 
        elif nerr ==9:   
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera OpRel") 
        elif nerr ==10:   
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera CIERTO o FALSO") 
        elif nerr ==11:   
            print ("Linea: " + str(self.token.linea) + "  ERROR:Se espera OpAdd")
        elif nerr == 12:
            print("Linea: " + str(self.token.linea) + " ERROR: Se espera Identif")
        elif nerr == 13:
            print("Linea: " + str(self.token.linea) + " ERROR: Se espera DosPtos")
        elif nerr == 14:
            print("Linea: " + str(self.token.linea) + " ERROR: Se espera PtoComa")
        elif nerr == 15:
            print("Linea: " + str(self.token.linea) + " ERROR: Se espera una palabra reservada de tipo ENTERO,REAL o BOLEANO")
        elif nerr == 16:
            print("Linea: " + str(self.token.linea) + " ERROR: Se espera una palabra reservada de tipo FIN")
        elif nerr == 17:
            print(
                "Linea: " + str(self.token.linea) + " ERROR: Se espera una palabra reservada de tipo INICIO, LEE, SI, Escribe o Mientras, o un Identificador")
        elif nerr == 18:
            print(
                "Linea: " + str(self.token.linea) + " ERROR: Se espera un ENTONCES")
        elif nerr == 19:
            print(
                "Linea: " + str(self.token.linea) + " ERROR: Se espera un SINO")
        elif nerr == 20:
            print(
                "Linea: " + str(self.token.linea) + " ERROR: Se espera un HACER")



    #TODO 
    #ES POSIBLE QUE AL HACER RETURN ANTES DE HACERLO HAYA QUE HACER UN ANALIZA PARA PASAR DE TOKEN?

    def Programa(self):
        if self.token.cat != "PR" or self.token.valor != "PROGRAMA":
            self.Error (1,self.token)  #raise errores.ErrorSintactico("Se espera la palabra reservada PROGRAMA")  #error 1
            return (False,[])
        else:
            self.token = self.lexico.Analiza()
            if self.token.cat != "Identif":
                #TODO Comprobar que el id esta disponible
                self.Error(2,self.token)  # raise errores.ErrorSintactico("Se espera IDENTIFICADOR")  #error 2
                return (False,[])
            else:
                id = self.token.valor
                self.token = self.lexico.Analiza()
                if self.token.cat !="Simbolo" or self.token.valor != "PtoComa":
                    self.Error(3,self.token)
                    return (False,[])
                else:
                    self.token = self.lexico.Analiza()
                    valor1, nodovar = self.decl_var()
                    valor2, nodoInst = self.instrucciones()
                    valor = valor1 and valor2
                    lsen = nodovar + nodoInst
                    nodoComp = AST.NodoCompuesta(lsen, self.token.linea)
                    nodo = AST.NodoPrograma(id,nodoComp,self.token.linea)

                    print(str(nodo))
                    return (valor,nodo)
        


    def decl_var(self):
        if self.token.cat != "PR" or self.token.valor != "VAR":
            return (True,[]) #Devolemos True porque esta regla es anulable
        # TODO 
        else:
            self.token = self.lexico.Analiza()
            #Cuando Existen terminales en medio de no terminales lo que vamos a hacer es crear funciones auxiliares
            #que los analicen.
            valorList, ids = self.lista_id()
            valoraux, decv = self.auxDecl_var()
            lista = [] #Lista para guardar el conjunto de ids de un tipo
            for id in ids:
                if id in self.tSimbolos.keys():
                    raise Exception("ID repetido")
                else:
                    self.tSimbolos[id] = (id,decv[0])
                    lista.append(AST.NodoId(id,decv[0],self.token.linea))
            # if decv[0] == "ENTERO":
            #     for id in ids:
            #         if id in self.tSimbolos.keys():
            #             raise Exception("ID repetido")
            #         else:
            #             self.tSimbolos[id] = (id,"ENTERO")
            #             lista.append(AST.NodoEntero(id,self.token.linea))
            # elif decv[0] == "REAL":
            #     for id in ids:
            #         if id in self.tSimbolos.keys():
            #             raise Exception("ID repetido")
            #         else:
            #             self.tSimbolos[id] = (id,"REAL")
            #             lista.append(AST.NodoReal(id,self.token.linea))
            # else: #decv[0] == "BOOLEANO"
            #     for id in ids:
            #         if id in self.tSimbolos.keys():
            #             raise Exception("ID repetido")
            #         else:
            #             self.tSimbolos[id] = (id,"BOOLEANO")
            #             lista.append(AST.NodoBooleano(id,self.token.linea))

            nodo1decl = [AST.NodoCompuesta(lista,self.token.linea)]
            if decv !=[]:
                toConcatenate = [decv[1]]
            else:
                toConcatenate = []
            nodoVariasDecl = AST.NodoCompuesta(nodo1decl + toConcatenate,self.token.linea)
            valor = valorList and valoraux

            return (valor,[nodoVariasDecl])

    def auxDecl_var(self):
        if self.token.cat != "Simbolo" or self.token.valor != "DosPtos":
            self.Error(13,self.token)
            return(False,[])
        else:
            self.token = self.lexico.Analiza()
            valorTipo,nodoTipo = self.tipo_std()
            valorAux,nodoAux = self.aux2Decl_var()
            valor = valorTipo and valorAux
            return (valor,[nodoTipo[0],nodoAux])

    def aux2Decl_var(self):
        if self.token.cat != "Simbolo" or self.token.valor != "PtoComa":
            self.Error(14,self.token)
            return (False,[])
        else:
            self.token = self.lexico.Analiza()
            valor,nodo = self.decl_v()
            return (valor,nodo)
            

    def decl_v(self):
        
        if self.token.cat != "Identif": #El Identif pertenece a la función lista_id
            if self.token.cat == "PR" and self.token.valor != "INICIO": #Inicio pude aparecer
            #     Restriccion R2 Id = Palabra reservada
                 raise Exception("No se puede usar una palabra reservada como id")
            return (True,[])
        else:
            valorList, ids = self.lista_id()
            valoraux, decv = self.auxDecl_v()
            lista = [] #Lista para guardar el conjunto de ids de un tipo

            for id in ids:
                if id in self.tSimbolos.keys():
                    raise Exception("ID repetido")
                else:
                    self.tSimbolos[id] = (id,decv[0])
                    lista.append(AST.NodoId(id,decv[0],self.token.linea))

            # if decv[0] == "ENTERO":
            #     for id in ids:
            #         if id in self.tSimbolos.keys():
            #             raise Exception("ID repetido")
            #         else:
            #             self.tSimbolos[id] = (id,"ENTERO")
            #             lista.append(AST.NodoEntero(id,self.token.linea))
            # elif decv[0] == "REAL":
            #         if id in self.tSimbolos.keys():
            #             raise Exception("ID repetido")
            #         else:
            #             self.tSimbolos[id] = (id,"REAL")
            #             lista.append(AST.NodoReal(id,self.token.linea))
            # else: #decv[0] == "BOOLEANO"
            #     for id in ids:
            #         if id in self.tSimbolos.keys():
            #             raise Exception("ID repetido")
            #         else:
            #             self.tSimbolos[id] = (id,"BOOLEANO")
            #             lista.append(AST.NodoBooleano(id,self.token.linea))
            nodo1decl = [AST.NodoCompuesta(lista,self.token.linea)]
            nodoVariasDecl = AST.NodoCompuesta(nodo1decl + decv[1],self.token.linea)
            valor = valorList and valoraux
            return (valor,nodoVariasDecl)

    def auxDecl_v(self):
        if self.token.cat != "Simbolo" or self.token.valor != "DosPtos":
            self.Error(13,self.token)
            return(False,[])
        else:
            self.token = self.lexico.Analiza()
            valorTipo,nodoTipo = self.tipo_std()
            valorAux,nodoAux = self.aux2Decl_v()
            valor = valorTipo and valorAux
            return (valor,[nodoTipo,nodoAux]) #NodoTipo = ENTERO,REAL o BOOLEANO y nodoAUX son mas de delv

    def aux2Decl_v(self):
        if self.token.cat != "Simbolo" or self.token.valor != "PtoComa":
            self.Error(14,self.token)
            return(False,[])
        else:
            self.token = self.lexico.Analiza()
            valor,nodo = self.decl_v()
            return (valor,nodo)



    def lista_id(self):
        if self.token.cat !="Identif":
            self.Error(12,self.token)
            if self.token.cat == "PR":
                #Restriccion 2
                raise Exception("No se puede poner como id una palabra reservada")
            return (False,[])
        else:
            #TODO Creo que es aquí donde hay que comprobar que no se repitan ids
            id = [self.token.valor] #Nos guardamos el id que analizamos como lista para cooncatenar con lo que llegue de resto_listaID
            self.token = self.lexico.Analiza()
            valor, restoid = self.resto_listaid()
            ids = id + restoid
            return (valor,ids)

    def resto_listaid(self):
        if self.token.cat != "Simbolo" or self.token.valor != "Coma":
            return (True,[]) #resto_listaid es anulable
        else:
            self.token = self.lexico.Analiza()
            valor, ids = self.lista_id()
            return (valor,ids)

    def tipo_std(self):
        if self.token.cat != "PR" or (self.token.valor != "ENTERO" and self.token.valor != "REAL" and self.token.valor != "BOOLEANO"):
            self.Error(15,self.token)
            return (False,[])
        else:
            tipo = self.token.valor #ENTERO, REAL o BOOLEANO
            self.token = self.lexico.Analiza()
            return (True,[tipo]) # Solo devuelve terminales

    def instrucciones(self):
        if self.token.cat != "PR" or self.token.valor != "INICIO":
            self.Error(16,self.token)
            return (False,[])
        else:
            self.token = self.lexico.Analiza()
            valorList, nodoList = self.lista_inst()
            valoraux,nodoaux = self.auxInstrucciones()
            valor = valorList and valoraux
            nodoLista = AST.NodoCompuesta(nodoList,self.token.linea)
            nodo = AST.NodoInicio(nodoLista,self.token.linea)
            return (valor,[nodo])

    def auxInstrucciones(self):
        if self.token.cat != "PR" or self.token.valor != "FIN":
            self.Error(17,self.token)
            return (False,[])
        else:
            return (True,[])

    def lista_inst(self):
        if (self.token.cat != "PR" or self.token.valor != "INICIO") and (self.token.cat != "Identif") and (self.token.cat != "PR" or self.token.valor != "LEE") and (
            self.token.cat != "PR" or self.token.valor != "ESCRIBE") and (
            self.token.cat != "PR" or self.token.valor != "SI") and (self.token.cat != "PR" or self.token.valor != "MIENTRAS"):
            return (True,[]) #Es anulable
        else:
            valorInst,nodoInst = self.instruccion()
            valor1,nodoaux = self.auxLista_inst()
            valor = valorInst and valor1
            lista = nodoInst + nodoaux
            return (valor,lista)

    def auxLista_inst(self):
        if self.token.cat != "Simbolo" or self.token.valor != "PtoComa":
            self.Error(14,self.token)
            return (False,[])
        else:
            self.token = self.lexico.Analiza()
            valor,nodo = self.lista_inst()
            return (valor,nodo)

    def instruccion(self):
        if (self.token.cat != "PR" or self.token.valor != "INICIO") and (
                self.token.cat != "Identif") and (
                self.token.cat != "PR" or self.token.valor != "LEE") and (
                self.token.cat != "PR" or self.token.valor != "SI") and (
                self.token.cat != "PR" or self.token.valor != "MIENTRAS") and (
                self.token.cat != "PR" or self.token.valor != "ESCRIBE"
        ):
            self.Error(17,self.token)
            return (False,[])

        #NOTA: Los nodos de las funciones auxiliares siempre son vacíos, por eso no se usan
        elif self.token.cat == "PR":
                if self.token.valor == "INICIO":
                    self.token = self.lexico.Analiza()
                    valorList,nodoList = self.lista_inst()
                    valorAux,nodoAux = self.auxInstruccion()
                    valor = valorList and valorAux
                    nodo = AST.NodoInicio(nodoList[0],self.token.linea) 
                    return (valor,[nodo])

                elif self.token.valor == "LEE" or self.token.valor == "ESCRIBE":
                    #Ocurre lo mismo que con Identif, LEE y ESCRIBE pertenecen a inst_es() por lo que ya devuelve el nodo construido
                    valor, nodo = self.inst_es()
                    return (valor,nodo)

                elif self.token.valor == "SI":
                    self.token = self.lexico.Analiza()
                    valorexp,nodoexp = self.expresion()
                    valoraux1,nodoaux1 = self.aux2Instruccion()
                    valorIns1,nodoIns1 = self.instruccion()
                    valorAux2,nodoAux2 = self.aux3Instruccion()
                    valorIns2,nodoIns2 = self.instruccion()
                    valor = valorexp and valorIns1 and valoraux1 and valorAux2 and valorIns2
                    nodo = AST.NodoSi(nodoexp[0],nodoIns1[0],nodoIns2[0],self.token.linea)
                    return (valor,[nodo])

                elif self.token.valor == "MIENTRAS":
                    self.token = self.lexico.Analiza()
                    valorexp,nodoexp = self.expresion()
                    valoraux,nodoaux = self.aux4Instruccion()
                    valorIns,nodoIns = self.instruccion()
                    valor = valorexp and valoraux and valorIns
                    nodo = AST.NodoMientras(nodoexp[0],nodoIns[0],self.token.linea)
                    return (valor,[nodo])

        elif self.token.cat == "Identif":
            #Como el identificador pertenece a instruccion simple, no hace falta crear un Nodo, porque lo crea inst_simple.
            valor, nodo = self.inst_simple()
            return (valor,nodo)


    def auxInstruccion(self):
        if (self.token.cat != "PR" or self.token.valor != "FIN"):
            self.Error(16,self.token)
            return (False,[])
        else:
            self.token = self.lexico.Analiza()
            return (True,[])

    def aux2Instruccion(self):
        if (self.token.cat != "PR" or self.token.valor != "ENTONCES"):
            self.Error(18,self.token)
            return (False,[])
        else:
            self.token = self.lexico.Analiza()
            return (True,[])
    def aux3Instruccion(self):
        if (self.token.cat != "PR" or self.token.valor != "SINO"):
            self.Error(19,self.token)
            return (False,[])
        else:
            self.token = self.lexico.Analiza()
            return (True,[])
    def aux4Instruccion(self):
        if (self.token.cat != "PR" or self.token.valor != "HACER"):
            self.Error(20,self.token)
            return (False,[])
        else:
            self.token = self.lexico.Analiza()
            return (True,[])







    ###########################################################################################################################################
    #
    #
    # OJO, YO HE TRATADO EL SELF.TOKEN COMO SI CUANDO ENTRA A LA FUNCION, ESTÁ APUNTANDO AL ELEMENTO QUE LE TOCA ANALIZAR. ES DECIR
    # CADA VEZ QUE LEO ALGO (OpSum, Identif, ...) SE HACE SELF.ANALIZA, PARA AVANZAR EL PUNTERO Y PREPARARLO PARA LO SIGUIENTE, YA 
    # SEA OTRA FUNCIÓN (LE LLEGA YA EL PUNTERO PREPARADO) O EL RETURN (PORQUE PUEDE HABER CONCATENACIONES).
    #
    # SIEMPRE DESPUÉS DE IF SELF.TOKEN != (ES DECIR, ANALIZAR UN ELEMENTO), SE PASA AL SIGUIENTE ELEMENTO, TANTO DENTRO DEL IF (ASI SE
    # PUEDEN ENCADENAR ERRORES) COMO FUERA (SI VA BIEN). 
    #
    #
    # EXCEPCIÓN: CUANDO UNA FUNCIÓN ES ANULABLE, ES DECIR, PUEDE SER VACÍA, SI LEES ALGO Y NO ES LO QUE TE INTERESA, SUPONES QUE ES 
    # ANULABLE Y DEVUELVES TRUE, SIN AVANZAR EL PUNTERO, PORQUE SUPUESTAMENTE YA ESTÁ PREPARADO PARA LO QUE VENGA DESPUÉS.
    #
    #
    ###########################################################################################################################################




    def inst_simple(self):
        if self.token.cat == "Identif":
            id = self.token.valor
            self.token = self.lexico.Analiza()
            if self.token.cat == "OpAsigna":
                self.token = self.lexico.Analiza()
                valor, nodo1 = self.expresion()
                nodo = AST.NodoAsignacion(id, nodo1[0], self.token.linea)
                return (valor, [nodo])
            else: 
                self.token = self.lexico.Analiza()
                self.Error(5,self.token)
                return (False, [])
        else:
            self.token = self.lexico.Analiza()
            self.Error(2,self.token)
            return (False, [])


    def inst_es(self):
        if self.token.cat != "PR" or self.token.valor != "LEE":
            if self.token.cat != "PR" or self.token.valor != "ESCRIBE":
                self.token = self.lexico.Analiza()
                self.Error(6,self.token)
                return (False,[])
            else:
                self.token = self.lexico.Analiza()
                if self.token.cat != "Simbolo" or self.token.valor != "ParentAp" :
                    self.token = self.lexico.Analiza()
                    self.Error(7,self.token)
                    return (False,[])
                else:
                    self.token = self.lexico.Analiza()
                    valor, nodo1 = self.expr_simple()
                    if (valor):
                        if self.token.cat != "Simbolo" or self.token.valor != "ParentCi" :
                            self.token = self.lexico.Analiza()
                            self.Error(8,self.token) 
                            return (False,[])
                        else:
                            nodo = AST.NodoEscribe(nodo1[0],self.token.linea) 
                            self.token = self.lexico.Analiza()
                            return (True, [nodo])
                    else:
                        return (False,[])
        else:
            self.token = self.lexico.Analiza()
            if self.token.cat != "Simbolo" or self.token.valor != "ParentAp" :
                self.token = self.lexico.Analiza()
                self.Error(7,self.token)
                return (False,[])
            else:
                self.token = self.lexico.Analiza()
                if self.token.cat != "Identif":
                    self.token = self.lexico.Analiza()
                    self.Error(2,self.token)  # raise errores.ErrorSintactico("Se espera IDENTIFICADOR")  #error 2
                    return (False,[])
                else:
                    id = self.token.value
                    self.token = self.lexico.Analiza()
                    if self.token.cat != "Simbolo" or self.token.valor != "ParentCi" :
                        self.token = self.lexico.Analiza()
                        self.Error(8,self.token) 
                        return (False,[])
                    else:
                        nodo = AST.NodoLee(id, self.token.linea)
                        self.token = self.lexico.Analiza()
                        return (True,[nodo])
                    
                    
                    
    def expresion(self):
        valor1, nodo1 = self.expr_simple()
        valor2, nodo2 = self.expresion2()
        valor = valor1 and valor2
        if nodo2 == []:
            nodo = AST.NodoExpresion(nodo1[0], self.token.linea)
            return(valor, [nodo])
        
        nodoaux = AST.NodoRelacion(nodo1[0],nodo2[0],self.token.linea,nodo2[1])
        nodo = AST.NodoExpresion(nodoaux, self.token.linea)
        return (valor, [nodo])       
        
    def expresion2(self):
        if self.token.cat != "OpRel":
            #SE DEVUELVE COMO ANULABLE 
            return (True,[])
        else:
            op = self.token.valor #Guardamos el operador
            self.token = self.lexico.Analiza()
            valor, nodo1 = self.expr_simple()
            return (valor, [nodo1[0],op])
        
        #TODO NO SE SI SE PASA UN OPREL ###############################################################################################

    def expr_simple(self):
        valor0 = True
        signo = "+"
        if self.token.cat == "OpAdd":
            valor0,signo = self.signo()
        valor1, nodo1 = self.termino()
        valor2, nodo2 = self.resto_exsimple()
        valor = valor1 and valor2 and valor0
        if nodo2 == []:
            nodo1[0].signo = signo
            return(valor, nodo1)
        
        nodo = AST.NodoAritmetico(signo, nodo1[0], nodo2[0], self.token.linea, nodo2[1])
        
        return (valor, [nodo])


    def resto_exsimple(self):
        if self.token.cat != "OpAdd":
            if self.token.cat != "PR" or self.token.valor != "O":
                #SE DEVUELVE COMO ANULABLE
                return (True, [])
            else:
                op = self.token.valor
                self.token = self.lexico.Analiza()
                valor1, nodo1 = self.termino()
                valor2, nodo2 = self.resto_exsimple()
                valor = valor1 and valor2
                if nodo2 == []:
                    return(valor, [nodo1[0], op])
                nodo = AST.NodoAritmetico(nodo1[0],nodo2[0],self.token.linea,nodo2[1])
                

                return(valor[nodo,op])

        else:
            op = self.token.valor
            self.token = self.lexico.Analiza()
            valor1, nodo1 = self.termino()
            valor2, nodo2 = self.resto_exsimple()
            valor = valor1 and valor2
            if nodo2 == []:
                return(valor, [nodo1[0], op])
            
            nodo = AST.NodoAritmetico(nodo1[0],nodo2[0],self.token.linea,nodo2[1])
            

            return(valor[nodo,op])
        
        
        
    def termino(self):
        valor1, nodo1 = self.factor()
        valor2, nodo2 = self.resto_term()
        valor = valor1 and valor2
        if nodo2 == []:
            return(valor,nodo1) 
        nodo = AST.NodoAritmetico(nodo1[0], nodo2[0], self.token.linea, nodo2[1])
        return (valor, [nodo])


    def resto_term(self):
        if self.token.cat != "OpMult":
            if self.token.cat != "PR" or self.token.valor != "Y":
                #SE DEVUELVE COMO ANULABLE
                return (True,[])
            else:
                op = self.token.valor
                self.token = self.lexico.Analiza()

                valor1, nodo1 = self.factor()
                valor2, nodo2 = self.resto_term()
                valor = valor1 and valor2
                if nodo2 == []:
                    return(valor, [nodo1[0], op])
                
                nodo = AST.NodoAritmetico(nodo1[0],nodo2[0],self.token.linea,nodo2[1])
                
                return(valor[nodo,op])
            
        else:
            op = self.token.valor
            self.token = self.lexico.Analiza()
            valor1, nodo1 = self.factor()
            valor2, nodo2 = self.resto_term()
            valor = valor1 and valor2
            if nodo2 == []:
                return(valor, [nodo1[0], op])
            nodo = AST.NodoAritmetico(nodo1[0],nodo2[0],self.token.linea,nodo2[1])
            

            return(valor[nodo,op])
    


    def factor(self):
        if self.token.cat != "Numero":
            if self.token.cat != "Identif":
                if self.token.cat != "Simbolo" or self.token.valor != "ParentAp" :
                    if self.token.cat != "PR" or self.token.valor != "NO":
                        if self.token.cat != "PR" or self.token.valor != "CIERTO" or self.token.valor != "FALSO":
                            self.token = self.lexico.Analiza()
                            self.Error(10,self.token) 
                            return (False, [])
                        else:
                            if self.token.valor == "FALSO":
                                nodo = AST.NodoBooleano(0,self.token.linea)
                            else:
                                nodo = AST.NodoBooleano(1,self.token.linea)
                            self.token = self.lexico.Analiza()
                            return (True, [nodo])
                    else:
                        self.token = self.lexico.Analiza()
                        valor, nodo = self.factor()
                        nodo = AST.NodoNegacion(nodo[0],self.token.linea)
                        return(valor, [nodo])
                else:
                    
                    
                    self.token = self.lexico.Analiza()
                    valor, nodo1 = self.expresion()
                    if (valor):
                        if self.token.cat != "Simbolo" or self.token.valor != "ParentCi" :
                            self.token = self.lexico.Analiza()
                            self.Error(8,self.token) 
                            return (False,[])
                        else:
                            self.token = self.lexico.Analiza()
                            return (True,nodo1)
                    else:
                        return (False,[])
                    
                    
                    
                    
            else:
                id = self.token.valor
                nodo = AST.NodoId(id,None,self.token.linea) #None porque el tipo es indefinido
                self.token = self.lexico.Analiza()
                return (True, [nodo])
        else:
            if self.token.tipo == "<type 'float'>":
                nodo = AST.NodoReal(self.token.valor, self.token.linea)
            else:
                nodo = AST.NodoEntero(self.token.valor, self.token.linea)
                
            self.token = self.lexico.Analiza()
            return (True, [nodo])
        
        
    def signo(self):
        if self.token.cat != "OpAdd":
            self.token = self.lexico.Analiza()
            self.Error(8,self.token) 
            return (False, [])
        else:
            self.token = self.lexico.Analiza()
            valor = self.token.valor
            return (True, [valor])
    


    
    
    
    
    
########################################################
##
## PRograma principal que lanza el analizador sintactico
####################################################

if __name__=="__main__":
    script, filename=argv
    #filename = "programa.txt" # Línea donde pasamos el nombre a mano para poder usar el debugger
    txt=open(filename)
    print ("Este es tu fichero %r" % filename)
    i=0
    fl = flujo.Flujo(txt)
    anlex=analex.Analex(fl)
    S = Sintactico(anlex)
    if S.Programa()[0]: #Como devolvemos tuplas, comprobamos solo el booleano
      print ("Analisis sintactico SATISFACTORIO. Fichero :", filename, "CORRECTO")
    else:
       print ("Analisis sintactico CON ERRORES. Fichero :", filename, "ERRONEO")


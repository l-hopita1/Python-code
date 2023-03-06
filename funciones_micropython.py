"""Módulo con funciones a implementar en MicroPython (uPy)."""
import struct

class FormatTable:
    """Clase con el formato de tabla de serialización"""
    def __init__(self,tag,type,len):
        self.tag = tag
        self.type = type
        self.len = len

class BinaryParser:
    """"Clase para codificar/decodificar un objeto o estructura de datos en función de un formato definido:
    ObjetoDatos <- Formato -> Trama binaria
    #ObjetoDatos -> Es el objeto que contiene los campos de datos que deben ser codificado/decodificado. Campos:
        • uint -> entero sin signo, longitud variable (1 a 32bits)
        • int -> entero con signo, longitud variable (complemento a 2, 2 a 32bits)
        • float -> punto flotante de precisión simple (IEEE 754, 32bits)
        • ascii -> ASCII string terminada en #0 | 7bits x caracter
    #Trama binaria -> Es un buffer -> diccionario / tabla serializado/a (cadena / bytes) que contiene los datos codificados de manera tal de optimizar la cantidad de bytes utilizados.
    #Formato -> Es un array o vector de objetos, donde cada elemento corresponde a la definición de cada campo del objeto (ObjetoDatos) que se pretende codificar/decodificar.
    Formato de la Tabla / Vector de objetos { { tag: "?", type: "?", len: ? } } donde:
        • tag -> Nombre del campo en el objeto para de/serializar
        • type -> Tipo de dato del campo
        • len -> Longitud en bits del campo (si aplica al tipo)} """
        
    def encode(src, format):
        """Codifica un objeto utilizando el formato ingresado.
        Devuelve una trama binaria codificada. 
        @param {*} src -> Diccionario / tabla a frasear (serializar)
        @param {*} format -> Formato de serialización (ver notas adjuntas)
        @return {*} size -> tamaño en bits de la trama. buffer -> diccionario / tabla serializado/a
        versión: 1.0"""
        buffer = ""
        
        # Convierto cada diccionario en un objeto FormatTable
        ObjetoDatos = [FormatTable(**datos) for datos in format]
        
        # Genero el formato y el argumento para serializar la trama
        structFormat=""
        structArg=[]
        for iObjetoDatos in ObjetoDatos:
            if (iObjetoDatos.type=="uint"):
                structFormat+="I"
                structArg.append(src[iObjetoDatos.tag])
            elif (iObjetoDatos.type=="int"):
                structFormat+="i"
                structArg.append(src[iObjetoDatos.tag])
            elif (iObjetoDatos.type=="float"):
                structFormat+="f"
                structArg.append(src[iObjetoDatos.tag])
            else:
                structFormat+=str(len(src[iObjetoDatos.tag]))+"s"
                structArg.append(src[iObjetoDatos.tag].encode('utf-8'))
                
        # Calculo el tamaño de la trama.
        size=struct.calcsize(structFormat)
        
        # Transformo los datos en una trama binaria
        buffer = struct.pack(structFormat, *structArg)
        return size, buffer


    def decode(buffer, format):
        """Decodifica la trama binaria del buffer utilizando el formato ingresado.
        Devuelve la lista con los objetos decodificados. 
        @param {*} buffer -> Trama a deserializar (cadena / bytes)
        @param {*} format -> Formato de serialización (ver notas adjuntas)
        @return {*} diccionario / tabla "composición" (trama deserializada en campos tag = valor)
        version: 1.0"""
        
        # Convierto cada diccionario en un objeto FormatTable
        ObjetoDatos = [FormatTable(**datos) for datos in format]
        
        # Genero el formato para deserializar la trama
        structFormat=""
        for iObjetoDatos in ObjetoDatos:
            if (iObjetoDatos.type=="uint"):
                structFormat+="I"
            elif (iObjetoDatos.type=="int"):
                structFormat+="i"
            elif (iObjetoDatos.type=="float"):
                structFormat+="f"
            else: #Es un 'ascii'
                structFormat+=str(int(iObjetoDatos.len/8))+"s" #informo cuantos caracteres tiene.
                
        # Transformo la trama binaria en datos 
        unpacked = struct.unpack(structFormat,buffer)
        
        # Transformo los datos en una lista de objetos
        result = {}
        count=0
        for iObjetoDatos in ObjetoDatos:
            if (iObjetoDatos.type=='ascii'):
                result[iObjetoDatos.tag] = unpacked[count].decode('utf-8').rstrip('\x00')
            else:
                result[iObjetoDatos.tag] = unpacked[count]
            count+=1
        return result

# main.py -- put your code here!
import struct
         
# Creo un diccionario para serializar:
var0 = {
    'Value': 1,
    'DOppm': -300,
    'TurbNTU': 3.1415,
    'ID': 'BsAs321'
}
 
# Genero la lista para des/serializar
format1 = [
    {"tag": "Value", "type": "uint", "len": 1},
    {"tag": "DOppm", "type": "int", "len": 10},
    {"tag": "TurbNTU", "type": "float","len":0},
    {"tag": "ID", "type": "ascii", "len": 7*8}
]

# BinaryParser {}
# Nota: 
#   Sólo sirve para cuatro objetos en la lista.
#
# Creo una clase con el formato de la tabla de serialización:
class FormatTable:
    def __init__(self,tag,type,len):
        self.tag = tag
        self.type = type
        self.len = len
            
# Función encode:
# @param {*} src -> Diccionario / tabla a frasear (serializar)
# @param {*} format -> Formato de serialización (ver notas adjuntas)
# @return {*} size -> tamaño en bits de la trama. buffer -> diccionario / tabla serializado/a
# versión: 1.0
def BinaryParser_encode1(src, format):
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

# Función decode:
# @param {*} buffer -> Trama a deserializar (cadena / bytes)
# @param {*} format -> Formato de serialización (ver notas adjuntas)
# @return {*} diccionario / tabla "composición" (trama deserializada en campos tag = valor)
# versión: 1.0
def BinaryParser_decode1(buffer, format):
    
    
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
        else:
            structFormat+=str(int(iObjetoDatos.len/8))+"s"
            
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

# Función principal:
print(f"Mis datos iniciales son: var0\n    {var0}")
[ParserSize, BinaryData]= BinaryParser_encode1(var0, format1)
print(f"La trama binaria es: ({ParserSize} bytes)\n    {BinaryData}")
var1= BinaryParser_decode1(BinaryData,format1)
print(f"Mis datos finales son: var1\n    {var1}")
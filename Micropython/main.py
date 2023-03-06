# main.py -- put your code here!
from funciones_micropython import BinaryParser
         
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

# Función principal:
print(f"Mis datos iniciales son: var0\n    {var0}")
[ParserSize, BinaryData]= BinaryParser.encode(var0, format1)
print(f"La trama binaria es: ({ParserSize} bytes)\n    {BinaryData}")
var1= BinaryParser.decode(BinaryData,format1)
print(f"Mis datos finales son: var1\n    {var1}")
help(BinaryParser)
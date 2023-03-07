"""Función para comprobar el correcto funcionamiento de 'BinaryParser' y sus funciones 'encode' y 'decode'.
Se puede utilizar el comando ' python -m unittest' para realizar otra comprobación mediante unittest."""
from funciones_micropython import *

var0 = { # Creo un diccionario para serializar.
    'Value': 1,
    'DOppm': -300,
    'TurbNTU': 3.1415,
    'ID': 'BsAs321'
}

format1 = [ # Genero la lista para des/serializar
    {"tag": "Value", "type": "uint", "len": 1},
    {"tag": "DOppm", "type": "int", "len": 10},
    {"tag": "TurbNTU", "type": "float","len":4},
    {"tag": "ID", "type": "ascii", "len": 7*8}
]

print(f"Mis datos iniciales son: var0\n    {var0}") # Imprimo mis valores iniciales.

[ParserSize, BinaryData]= BinaryParser.encode(var0, format1) #Codifico mis datos
print(f"La trama binaria es: ({ParserSize} bytes)\n    {BinaryData}") # Imprimo mis datos codificados.

var1= BinaryParser.decode(BinaryData,format1) # Decodifico la trama binaria.
print(f"Mis datos finales son: var1\n    {var1}") # Imprimo mis datos decodificados.

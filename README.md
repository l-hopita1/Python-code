# Python-code

Dentro de la carpeta Micropython se encuentran funciones para aplicar en microcontroladores ESP32 ó ESP8266
La clase BinaryParser contiene dos funciones para generar un codificador y un decodificador a implementar con un diccionario ó un único objeto.
BinaryParser.encode:
  Codifica un objeto utilizando el formato ingresado. Devuelve una trama binaria codificada. 
  @param {*} src -> Diccionario / tabla a frasear (serializar)
  @param {*} format -> Formato de serialización (ver notas adjuntas)
  @return {*} size -> tamaño en bits de la trama. buffer -> diccionario / tabla serializado/a
BinaryParser.decode:
  Decodifica la trama binaria del buffer utilizando el formato ingresado. Devuelve la lista con los objetos decodificados. 
  @param {*} buffer -> Trama a deserializar (cadena / bytes)
  @param {*} format -> Formato de serialización (ver notas adjuntas)
  @return {*} diccionario / tabla "composición" (trama deserializada en campos tag = valor)
  
  
 >>>Ejemplo:
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
imprime:
Mis datos iniciales son: var0
    {'TurbNTU': 3.1415, 'ID': 'BsAs321', 'Value': 1, 'DOppm': -300}
    
[ParserSize, BinaryData]= BinaryParser.encode(var0, format1) #Codifico mis datos
print(f"La trama binaria es: ({ParserSize} bytes)\n    {BinaryData}") # Imprimo mis datos codificados.
imprime:
La trama binaria es: (19 bytes)
    b'\x01\x00\x00\x00\xd4\xfe\xff\xffV\x0eI@BsAs321'
    
var1= BinaryParser.decode(BinaryData,format1) # Decodifico la trama binaria.
print(f"Mis datos finales son: var1\n    {var1}") # Imprimo mis datos decodificados.
imprime:
Mis datos finales son: var1
    {'TurbNTU': 3.1415, 'ID': 'BsAs321', 'Value': 1, 'DOppm': -300}
    
    
Observaciones:
- Cuando una variable es de tipo float, no devuelve exactamente el mismo valor.
- No funciona si Var0 ó Format1 son de distinto largo

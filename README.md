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
  
  
Ejemplo en el programa main:

    var0 = { # Creo un diccionario para serializar.
        'Value': 1,
        'DOppm': -300,
        'TurbNTU': 3.1415,
        'ID': 'BsAs321'
    }

    format1 = [ # Genero la lista para des/serializar
        {"tag": "Value", "type": "uint", "len": 1},
        {"tag": "DOppm", "type": "int", "len": 10},
        {"tag": "TurbNTU", "type": "float","len":32},
        {"tag": "ID", "type": "ascii", "len": 7*7}
    ]
    print(f"Mis datos iniciales son: var0\n    {var0}") # Imprimo mis valores iniciales.

    [ParserSize, BinaryData]= BinaryParser.encode1(var0, format1) #Codifico mis datos
    print(f"La trama binaria es: ({ParserSize} bytes)\n    {BinaryData}") # Imprimo mis datos codificados.

    var1= BinaryParser.decode1(BinaryData,format1) # Decodifico la trama binaria.
    print(f"Mis datos finales son: var1\n    {var1}") # Imprimo mis datos decodificados.

Devuelve:

    Mis datos iniciales son: var0    {'Value': 1, 'DOppm': -300, 'TurbNTU': 3.1415, 'ID': 'BsAs321'}La trama binaria es: (102 bytes)
        110110101000100000001001001000011100101011001000010011100110100000101110011001100110011001000110001000
    Mis datos finales son: var1
        {'Value': 1, 'DOppm': -300, 'TurbNTU': 3.1414999961853027, 'ID': 'BsAs321'}
    
Observaciones:

    - Cuando una variable es de tipo float, no devuelve exactamente el mismo valor.
    - En caso que Var0 ó Format1 sean de distinto largo, devuelve la mayor cantidad de datos posibles advirtiendo un problema.
    - Emite un alerta en caso que se escriba mal algún tipo de formato: 'uint', 'int', 'float' ó 'ascii'. Y no ejecuta el serializado de ese objeto.
    - La trama binaria es de mayor tamaño que la suma de la columna 'len' ya que se completa la trama con zeros overhead completando el byte a transmitir.

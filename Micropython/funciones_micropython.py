"""Módulo con funciones a implementar en MicroPython (uPy)."""
import struct
import bitstring
        
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

    def encode1(src, format):
        """Codifica un objeto utilizando el formato ingresado.
        Devuelve una trama binaria codificada. 
        @param {*} src -> Diccionario / tabla a frasear (serializar)
        @param {*} format -> Formato de serialización (ver notas adjuntas)
        @return {*} size -> tamaño en bits de la trama. buffer -> diccionario / tabla serializado/a
        versión: 2.0"""
        try:
            # Verifico los datos de entrada:
            if len(src) > len(format):
                print(f"encode1: El largo del diccionario 'src' es mayor a la tabla de formato 'format': {len(src)} < {len(format)}")
                
            # Crea una lista vacía para almacenar la trama binaria
            bits = bitstring.BitArray()
            
            # Recorre la lista format para serializar cada campo en el diccionario src
            count=0
            for field in format:
                # Obtiene el valor del campo en el diccionario src
                value = src[field['tag']]
                
                # Serializa el valor según el tipo de campo y el tamaño especificado en format
                if field['type'] == 'uint':
                    bits.append(bitstring.pack('uint:%d' % field['len'], value))
                    if value.bit_length()>field['len']:
                        print(f"encode1: Se recortó el valor de {field['tag']} ya que  supera el límite establecido en format. {value}({value.bit_length()} bits) > {field['len']} bits")
                elif field['type'] == 'int':
                    bits.append(bitstring.pack('int:%d' % field['len'], value))
                    if value.bit_length()>field['len']:
                        print(f"encode1: Se recortó el valor de {field['tag']} ya que  supera el límite establecido en format. {value}({value.bit_length()} bits) > {field['len']} bits")
                elif field['type'] == 'float':
                    bits.append(bitstring.pack('floatbe:%d' % field['len'], value))
                elif field['type'] == 'ascii':
                    encoded = struct.pack('%ds' % (field['len']//7), value.encode('ascii'))
                    bits.append(bitstring.BitArray(bytes=encoded))
                    if len(value)*7>field['len']:
                        print(f"encode1: Se recortó el valor de {field['tag']} ya que  supera el límite establecido en format. {value}({len(value)*7} bits) > {field['len']} bits")
                else:
                    print(f"encode1: No se reconoce el tipo de objeto: {field['type']}")
                count+=1
                
        except KeyError:
            print(KeyError)
            print(f"Advertencia! Las filas del diccionario (src) deben igualar a las del formato (format): {len(src)}(src)~={len(format)}(format)\nSe utilizan menos filas de format.")
            ShortFormat=[row for i, row in enumerate(format) if i != count]
            [output0,output1]=BinaryParser.encode1(src, ShortFormat)
            return output0,output1
        else:
            # Agrego bits overhead para completar el paquete de bytes.
            trama=bits.bin + '0'*(bits.len%8)
            # Devuelve el tamaño y el valor de la trama binaria
            return len(trama), trama

    def decode1(buffer, format):
        """Decodifica la trama binaria del buffer utilizando el formato ingresado.
        Devuelve la lista con los objetos decodificados. 
        @param {*} buffer -> Trama a deserializar (cadena / bytes)
        @param {*} format -> Formato de serialización (ver notas adjuntas)
        @return {*} diccionario / tabla "composición" (trama deserializada en campos tag = valor)
        version: 2.0"""
        try:
            # Crea un diccionario vacío para almacenar los valores deserializados
            values = {}
            
            # Convierte la trama binaria a un objeto BitArray de bitstring
            bits = bitstring.BitArray(bin=buffer)
            
            # Recorre la lista format para deserializar cada campo de la trama binaria
            for field in format:
                if field['type'] == 'uint':
                    values[field['tag']] = bits.unpack('uint:{:d}'.format(field['len']))[0]
                elif field['type'] == 'int':
                    values[field['tag']] = bits.unpack('int:{:d}'.format(field['len']))[0]
                elif field['type'] == 'float':
                    values[field['tag']] = bits.unpack('floatbe:{:d}'.format(field['len']))[0]
                elif field['type'] == 'ascii':
                    length = field['len'] // 7
                    values[field['tag']] = bits.unpack('bytes:{}'.format(length))[0].decode('ascii', 'ignore')
                else:
                    print(f"decode1: No se reconoce el tipo de objeto: {field['type']}")
                bits=bits[field['len']:]
        except bitstring.ReadError:
            print(bitstring.ReadError)
            print("Advertencia! La trama binaria debería ser mayor según el formato ingresado.")
            return None
        else:
            return values
        

"""Módulo para ejecutar el unittest de BinaryParser"""
import unittest
from funciones_micropython import *

class TestBinaryParser(unittest.TestCase):
    def test_code(self):
        [ParserSize, BinaryData]= BinaryParser.encode(var0, format1) #Codifico mis datos
        self.assertAlmostEqual(BinaryParser.decode(BinaryData,format1), var0, places=2)

var0 = { # Creo un objeto para serializar.
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
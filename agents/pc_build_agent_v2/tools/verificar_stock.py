"""
Herramienta de Verificación de Stock
Funciones para consultar disponibilidad de productos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from typing import Dict, Any
from consultas_productos import obtener_detalle_producto


def verificar_stock(noparte: str, clave_marca: str) -> Dict[str, Any]:
    """
    Verifica disponibilidad de stock de un producto
    
    Args:
        noparte: Número de parte del producto
        clave_marca: Clave de la marca
        
    Returns:
        Diccionario con stock por sucursal y total
    """
    producto = obtener_detalle_producto(noparte, clave_marca)
    
    if not producto or not producto.get('Stock'):
        return {
            'disponible': False,
            'total': 0,
            'por_sucursal': {},
            'producto': None
        }
    
    stock_por_sucursal = producto['Stock']
    total_stock = sum(stock_por_sucursal.values())
    
    return {
        'disponible': total_stock > 0,
        'total': total_stock,
        'por_sucursal': stock_por_sucursal,
        'producto': {
            'noparte': producto['Noparte'],
            'descripcion': producto['Descripcion'],
            'marca': producto['Marca']
        }
    }


def tiene_stock_minimo(noparte: str, clave_marca: str, minimo: int = 1) -> bool:
    """
    Verifica si un producto tiene al menos la cantidad mínima en stock
    
    Args:
        noparte: Número de parte del producto
        clave_marca: Clave de la marca
        minimo: Cantidad mínima requerida
        
    Returns:
        True si hay stock suficiente, False si no
    """
    stock_info = verificar_stock(noparte, clave_marca)
    return stock_info['total'] >= minimo

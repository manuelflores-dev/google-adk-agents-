"""
Herramienta de Consultas de Productos
Funciones para buscar y filtrar productos en la base de datos
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from typing import List, Dict, Any, Optional
from conexion_bd import conectar_bd


from decimal import Decimal

def _convert_decimals(obj: Any) -> Any:
    """Convierte recursivamente objetos Decimal a float para serialización JSON"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: _convert_decimals(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_convert_decimals(i) for i in obj]
    return obj


def _format_stock(stock_json: Any) -> str:
    """Convierte el JSON de stock a un string legible para el agente"""
    if not stock_json or not isinstance(stock_json, dict):
        return "Consultar disponibilidad"
    
    # Filtrar sucursales con stock 0 y formatear
    items = [f"{k}: {v}" for k, v in stock_json.items() if v > 0]
    return ", ".join(items) if items else "Sin stock disponible"


def consultar_productos_por_categoria(
    subfamilia: str,
    nivel_precio: int = 1,
    precio_min: float = 0,
    precio_max: float = 100000,
    limite: int = 20
) -> List[Dict[str, Any]]:
    """
    Busca productos por categoría (Subfamilia) con filtros de precio.
    """
    try:
        connection = conectar_bd()
        cursor = connection.cursor(dictionary=True)
        
        # Validar nivel de precio (1-10)
        nivel_precio = max(1, min(10, nivel_precio))
        columna_precio = f"Precio{nivel_precio}"
        
        query = f"""
            SELECT Noparte, Codigo, Descripcion, Marca, Subfamilia, Stock, {columna_precio} as Precio, Atributos_json
            FROM producto_ensamble 
            WHERE Subfamilia LIKE %s 
            AND {columna_precio} BETWEEN %s AND %s
            LIMIT %s
        """
        
        cursor.execute(query, (f"%{subfamilia}%", precio_min, precio_max, limite))
        productos = cursor.fetchall()
        
        resultado = []
        for p in productos:
            try:
                stock_raw = json.loads(p['Stock']) if p['Stock'] else {}
            except:
                stock_raw = {}
                
            resultado.append({
                "noparte": p['Noparte'],
                "descripcion": p['Descripcion'],
                "marca": p['Marca'],
                "precio": p['Precio'],
                "stock_formateado": _format_stock(stock_raw), # Stock listo para usar
                "specs": p['Atributos_json']
            })
            
        return _convert_decimals(resultado)
        
    except Exception as e:
        print(f"Error en consultar_productos_por_categoria: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def buscar_productos(
    termino_busqueda: str,
    nivel_precio: int = 1,
    limite: int = 5
) -> List[Dict[str, Any]]:
    """
    Busca productos por término en descripción o marca.
    """
    try:
        connection = conectar_bd()
        cursor = connection.cursor(dictionary=True)
        
        nivel_precio = max(1, min(10, nivel_precio))
        columna_precio = f"Precio{nivel_precio}"
        
        query = f"""
            SELECT Noparte, Descripcion, Marca, Subfamilia, Stock, {columna_precio} as Precio
            FROM producto_ensamble 
            WHERE (Descripcion LIKE %s OR Marca LIKE %s OR Noparte LIKE %s)
            LIMIT %s
        """
        
        term = f"%{termino_busqueda}%"
        cursor.execute(query, (term, term, term, limite))
        productos = cursor.fetchall()
        
        resultado = []
        for p in productos:
            try:
                stock_raw = json.loads(p['Stock']) if p['Stock'] else {}
            except:
                stock_raw = {}
                
            resultado.append({
                "noparte": p['Noparte'],
                "descripcion": p['Descripcion'],
                "marca": p['Marca'],
                "categoria": p['Subfamilia'],
                "precio": p['Precio'],
                "stock_formateado": _format_stock(stock_raw) # Stock listo para usar
            })
            
        return _convert_decimals(resultado)
        
    except Exception as e:
        print(f"Error en buscar_productos: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def obtener_detalle_producto(
    noparte: str,
    nivel_precio: int = 1
) -> Dict[str, Any]:
    """
    Obtiene detalles completos de un producto específico.
    """
    try:
        connection = conectar_bd()
        cursor = connection.cursor(dictionary=True)
        
        nivel_precio = max(1, min(10, nivel_precio))
        columna_precio = f"Precio{nivel_precio}"
        
        query = f"""
            SELECT *
            FROM producto_ensamble 
            WHERE Noparte = %s
        """
        
        cursor.execute(query, (noparte,))
        producto = cursor.fetchone()
        
        if producto:
            try:
                stock_raw = json.loads(producto['Stock']) if producto['Stock'] else {}
                specs = json.loads(producto['Atributos_json']) if producto['Atributos_json'] else {}
            except:
                stock_raw = {}
                specs = {}

            resultado = {
                "noparte": producto['Noparte'],
                "descripcion": producto['Descripcion'],
                "marca": producto['Marca'],
                "categoria": producto['Subfamilia'],
                "precio": producto[columna_precio],
                "stock_formateado": _format_stock(stock_raw), # Stock listo para usar
                "especificaciones": specs
            }
            return _convert_decimals(resultado)
            
        return {}
        
    except Exception as e:
        print(f"Error en obtener_detalle_producto: {e}")
        return {}
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

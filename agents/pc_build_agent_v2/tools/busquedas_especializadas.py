"""
Herramientas de búsqueda especializadas por componente
Optimizadas para reducir tokens y búsquedas precisas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from typing import List, Dict, Any, Optional
from decimal import Decimal
from conexion_bd import conectar_bd
from subfamilia_map import obtener_subfamilias


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
    """Convierte el JSON de stock a un string legible"""
    if not stock_json or not isinstance(stock_json, dict):
        return "Consultar disponibilidad"
    
    items = [f"{k}: {v}" for k, v in stock_json.items() if v > 0]
    return ", ".join(items) if items else "Sin stock disponible"


def buscar_procesadores(
    socket: Optional[str] = None,
    cores_min: Optional[int] = None,
    marca: Optional[str] = None,
    precio_max: float = 100000,
    nivel_precio: int = 1,
    limite: int = 10
) -> List[Dict]:
    """
    Busca procesadores (CPUs) con filtros precisos.
    
    Args:
        socket: Socket del CPU (ej: "AM5", "LGA1700", "AM4")
        cores_min: Número mínimo de cores
        marca: Marca específica (ej: "AMD", "INTEL")
        precio_max: Precio máximo en pesos
        nivel_precio: Nivel de precio a consultar (1-10)
        limite: Máximo de resultados (default 10 para optimizar tokens)
    
    Returns:
        Lista de procesadores con especificaciones
    """
    try:
        connection = conectar_bd()
        cursor = connection.cursor(dictionary=True)
        
        nivel_precio = max(1, min(10, nivel_precio))
        columna_precio = f"Precio{nivel_precio}"
        
        # Obtener subfamilias para CPU
        subfamilias = obtener_subfamilias("PROCESADOR")
        placeholders = ', '.join(['%s'] * len(subfamilias))
        
        conditions = [f"Subfamilia IN ({placeholders})"]
        params = list(subfamilias)
        
        # Filtro por socket (búsqueda en JSON)
        if socket:
            conditions.append("(Atributos_json LIKE %s OR Descripcion LIKE %s)")
            socket_pattern = f"%{socket.upper()}%"
            params.extend([socket_pattern, socket_pattern])
        
        # Filtro por marca
        if marca:
            conditions.append("Marca LIKE %s")
            params.append(f"%{marca.upper()}%")
        
        # Filtro por precio
        conditions.append(f"{columna_precio} <= %s")
        params.append(precio_max)
        
        # Solo con stock
        conditions.append("Stock IS NOT NULL")
        
        query = f"""
            SELECT Noparte, Codigo, Descripcion, Marca, Subfamilia, Stock, 
                   {columna_precio} as Precio, Atributos_json
            FROM producto_ensamble 
            WHERE {' AND '.join(conditions)}
            ORDER BY {columna_precio} ASC
            LIMIT %s
        """
        params.append(limite)
        
        cursor.execute(query, params)
        productos = cursor.fetchall()
        
        resultado = []
        for p in productos:
            try:
                stock_raw = json.loads(p['Stock']) if p['Stock'] else {}
                specs = json.loads(p['Atributos_json']) if p['Atributos_json'] else {}
            except:
                stock_raw = {}
                specs = {}
            
            # Solo agregar si tiene stock real
            if not stock_raw or sum(stock_raw.values()) == 0:
                continue
                
            resultado.append({
                "noparte": p['Noparte'],
                "descripcion": p['Descripcion'],
                "marca": p['Marca'],
                "precio": p['Precio'],
                "stock_formateado": _format_stock(stock_raw),
                "specs": specs,
                "socket": specs.get("socket", "N/A"),
                "cores": specs.get("cores", "N/A"),
                "threads": specs.get("threads", "N/A")
            })
            
        return _convert_decimals(resultado)
        
    except Exception as e:
        print(f"Error en buscar_procesadores: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def buscar_motherboards(
    socket: Optional[str] = None,
    chipset: Optional[str] = None,
    tipo_ram: Optional[str] = None,
    precio_max: float = 100000,
    nivel_precio: int = 1,
    limite: int = 10
) -> List[Dict]:
    """
    Busca tarjetas madre (motherboards) con filtros precisos.
    
    Args:
        socket: Socket compatible (ej: "AM5", "LGA1700")
        chipset: Chipset específico (ej: "B550", "Z790")
        tipo_ram: Tipo de RAM soportada (ej: "DDR4", "DDR5")
        precio_max: Precio máximo
        nivel_precio: Nivel de precio (1-10)
        limite: Máximo de resultados
    """
    try:
        connection = conectar_bd()
        cursor = connection.cursor(dictionary=True)
        
        nivel_precio = max(1, min(10, nivel_precio))
        columna_precio = f"Precio{nivel_precio}"
        
        subfamilias = obtener_subfamilias("MOTHERBOARD")
        placeholders = ', '.join(['%s'] * len(subfamilias))
        
        conditions = [f"Subfamilia IN ({placeholders})"]
        params = list(subfamilias)
        
        if socket:
            conditions.append("(Atributos_json LIKE %s OR Descripcion LIKE %s)")
            socket_pattern = f"%{socket.upper()}%"
            params.extend([socket_pattern, socket_pattern])
        
        if chipset:
            conditions.append("(Atributos_json LIKE %s OR Descripcion LIKE %s)")
            chipset_pattern = f"%{chipset.upper()}%"
            params.extend([chipset_pattern, chipset_pattern])
        
        if tipo_ram:
            conditions.append("(Atributos_json LIKE %s OR Descripcion LIKE %s)")
            ram_pattern = f"%{tipo_ram.upper()}%"
            params.extend([ram_pattern, ram_pattern])
        
        conditions.append(f"{columna_precio} <= %s")
        params.append(precio_max)
        
        conditions.append("Stock IS NOT NULL")
        
        query = f"""
            SELECT Noparte, Codigo, Descripcion, Marca, Stock, 
                   {columna_precio} as Precio, Atributos_json
            FROM producto_ensamble 
            WHERE {' AND '.join(conditions)}
            ORDER BY {columna_precio} ASC
            LIMIT %s
        """
        params.append(limite)
        
        cursor.execute(query, params)
        productos = cursor.fetchall()
        
        resultado = []
        for p in productos:
            try:
                stock_raw = json.loads(p['Stock']) if p['Stock'] else {}
                specs = json.loads(p['Atributos_json']) if p['Atributos_json'] else {}
            except:
                stock_raw = {}
                specs = {}
            
            if not stock_raw or sum(stock_raw.values()) == 0:
                continue
                
            resultado.append({
                "noparte": p['Noparte'],
                "descripcion": p['Descripcion'],
                "marca": p['Marca'],
                "precio": p['Precio'],
                "stock_formateado": _format_stock(stock_raw),
                "specs": specs,
                "socket": specs.get("socket", "N/A"),
                "chipset": specs.get("chipset", "N/A"),
                "tipo_memoria": specs.get("tipo de memoria", specs.get("memory type", "N/A"))
            })
            
        return _convert_decimals(resultado)
        
    except Exception as e:
        print(f"Error en buscar_motherboards: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def buscar_ram(
    tipo: Optional[str] = None,
    velocidad_mhz: Optional[int] = None,
    capacidad_gb: Optional[int] = None,
    precio_max: float = 100000,
    nivel_precio: int = 1,
    limite: int = 10
) -> List[Dict]:
    """
    Busca memorias RAM con filtros precisos.
    
    Args:
        tipo: Tipo de RAM (ej: "DDR4", "DDR5")
        velocidad_mhz: Velocidad mínima en MHz (ej: 3200, 6000)
        capacidad_gb: Capacidad en GB (ej: 8, 16, 32)
        precio_max: Precio máximo
        nivel_precio: Nivel de precio (1-10)
        limite: Máximo de resultados
    """
    try:
        connection = conectar_bd()
        cursor = connection.cursor(dictionary=True)
        
        nivel_precio = max(1, min(10, nivel_precio))
        columna_precio = f"Precio{nivel_precio}"
        
        subfamilias = obtener_subfamilias("RAM")
        placeholders = ', '.join(['%s'] * len(subfamilias))
        
        conditions = [f"Subfamilia IN ({placeholders})"]
        params = list(subfamilias)
        
        if tipo:
            conditions.append("(Atributos_json LIKE %s OR Descripcion LIKE %s)")
            tipo_pattern = f"%{tipo.upper()}%"
            params.extend([tipo_pattern, tipo_pattern])
        
        if capacidad_gb:
            conditions.append("(Descripcion LIKE %s OR Descripcion LIKE %s)")
            params.extend([f"%{capacidad_gb}GB%", f"%{capacidad_gb} GB%"])
        
        conditions.append(f"{columna_precio} <= %s")
        params.append(precio_max)
        
        conditions.append("Stock IS NOT NULL")
        
        query = f"""
            SELECT Noparte, Codigo, Descripcion, Marca, Stock, 
                   {columna_precio} as Precio, Atributos_json
            FROM producto_ensamble 
            WHERE {' AND '.join(conditions)}
            ORDER BY {columna_precio} ASC
            LIMIT %s
        """
        params.append(limite)
        
        cursor.execute(query, params)
        productos = cursor.fetchall()
        
        resultado = []
        for p in productos:
            try:
                stock_raw = json.loads(p['Stock']) if p['Stock'] else {}
                specs = json.loads(p['Atributos_json']) if p['Atributos_json'] else {}
            except:
                stock_raw = {}
                specs = {}
            
            if not stock_raw or sum(stock_raw.values()) == 0:
                continue
                
            resultado.append({
                "noparte": p['Noparte'],
                "descripcion": p['Descripcion'],
                "marca": p['Marca'],
                "precio": p['Precio'],
                "stock_formateado": _format_stock(stock_raw),
                "specs": specs
            })
            
        return _convert_decimals(resultado)
        
    except Exception as e:
        print(f"Error en buscar_ram: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def buscar_gpu(
    vram_gb_min: Optional[int] = None,
    marca: Optional[str] = None,
    precio_max: float = 100000,
    nivel_precio: int = 1,
    limite: int = 10
) -> List[Dict]:
    """
    Busca tarjetas gráficas (GPUs) con filtros precisos.
    
    Args:
        vram_gb_min: VRAM mínima en GB (ej: 4, 6, 8)
        marca: Marca de GPU (ej: "NVIDIA", "AMD", "GEFORCE", "RADEON")
        precio_max: Precio máximo
        nivel_precio: Nivel de precio (1-10)
        limite: Máximo de resultados
    """
    try:
        connection = conectar_bd()
        cursor = connection.cursor(dictionary=True)
        
        nivel_precio = max(1, min(10, nivel_precio))
        columna_precio = f"Precio{nivel_precio}"
        
        subfamilias = obtener_subfamilias("GPU")
        placeholders = ', '.join(['%s'] * len(subfamilias))
        
        conditions = [f"Subfamilia IN ({placeholders})"]
        params = list(subfamilias)
        
        if marca:
            conditions.append("(Marca LIKE %s OR Descripcion LIKE %s)")
            marca_pattern = f"%{marca.upper()}%"
            params.extend([marca_pattern, marca_pattern])
        
        if vram_gb_min:
            conditions.append("(Descripcion LIKE %s OR Descripcion LIKE %s)")
            params.extend([f"%{vram_gb_min}GB%", f"%{vram_gb_min} GB%"])
        
        conditions.append(f"{columna_precio} <= %s")
        params.append(precio_max)
        
        conditions.append("Stock IS NOT NULL")
        
        query = f"""
            SELECT Noparte, Codigo, Descripcion, Marca, Stock, 
                   {columna_precio} as Precio, Atributos_json
            FROM producto_ensamble 
            WHERE {' AND '.join(conditions)}
            ORDER BY {columna_precio} ASC
            LIMIT %s
        """
        params.append(limite)
        
        cursor.execute(query, params)
        productos = cursor.fetchall()
        
        resultado = []
        for p in productos:
            try:
                stock_raw = json.loads(p['Stock']) if p['Stock'] else {}
                specs = json.loads(p['Atributos_json']) if p['Atributos_json'] else {}
            except:
                stock_raw = {}
                specs = {}
            
            if not stock_raw or sum(stock_raw.values()) == 0:
                continue
                
            resultado.append({
                "noparte": p['Noparte'],
                "descripcion": p['Descripcion'],
                "marca": p['Marca'],
                "precio": p['Precio'],
                "stock_formateado": _format_stock(stock_raw),
                "specs": specs
            })
            
        return _convert_decimals(resultado)
        
    except Exception as e:
        print(f"Error en buscar_gpu: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def buscar_almacenamiento(
    tipo: Optional[str] = None,
    capacidad_gb_min: Optional[int] = None,
    interfaz: Optional[str] = None,
    precio_max: float = 100000,
    nivel_precio: int = 1,
    limite: int = 10
) -> List[Dict]:
    """
    Busca unidades de almacenamiento (SSD/HDD) con filtros precisos.
    
    Args:
        tipo: Tipo de almacenamiento (ej: "SSD", "HDD", "NVME", "SATA")
        capacidad_gb_min: Capacidad mínima en GB
        interfaz: Interfaz (ej: "NVME", "SATA", "M.2")
        precio_max: Precio máximo
        nivel_precio: Nivel de precio (1-10)
        limite: Máximo de resultados
    """
    try:
        connection = conectar_bd()
        cursor = connection.cursor(dictionary=True)
        
        nivel_precio = max(1, min(10, nivel_precio))
        columna_precio = f"Precio{nivel_precio}"
        
        # Incluir tanto SSD como HDD
        subfamilias_ssd = obtener_subfamilias("SSD")
        subfamilias_hdd = obtener_subfamilias("HDD_INTERNO")
        subfamilias = subfamilias_ssd + subfamilias_hdd
        
        placeholders = ', '.join(['%s'] * len(subfamilias))
        
        conditions = [f"Subfamilia IN ({placeholders})"]
        params = list(subfamilias)
        
        if tipo:
            conditions.append("(Descripcion LIKE %s OR Atributos_json LIKE %s)")
            tipo_pattern = f"%{tipo.upper()}%"
            params.extend([tipo_pattern, tipo_pattern])
        
        if interfaz:
            conditions.append("(Descripcion LIKE %s OR Atributos_json LIKE %s)")
            interfaz_pattern = f"%{interfaz.upper()}%"
            params.extend([interfaz_pattern, interfaz_pattern])
        
        conditions.append(f"{columna_precio} <= %s")
        params.append(precio_max)
        
        conditions.append("Stock IS NOT NULL")
        
        query = f"""
            SELECT Noparte, Codigo, Descripcion, Marca, Stock, 
                   {columna_precio} as Precio, Atributos_json
            FROM producto_ensamble 
            WHERE {' AND '.join(conditions)}
            ORDER BY {columna_precio} ASC
            LIMIT %s
        """
        params.append(limite)
        
        cursor.execute(query, params)
        productos = cursor.fetchall()
        
        resultado = []
        for p in productos:
            try:
                stock_raw = json.loads(p['Stock']) if p['Stock'] else {}
                specs = json.loads(p['Atributos_json']) if p['Atributos_json'] else {}
            except:
                stock_raw = {}
                specs = {}
            
            if not stock_raw or sum(stock_raw.values()) == 0:
                continue
                
            resultado.append({
                "noparte": p['Noparte'],
                "descripcion": p['Descripcion'],
                "marca": p['Marca'],
                "precio": p['Precio'],
                "stock_formateado": _format_stock(stock_raw),
                "specs": specs
            })
            
        return _convert_decimals(resultado)
        
    except Exception as e:
        print(f"Error en buscar_almacenamiento: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def buscar_fuentes_poder(
    watts_min: Optional[int] = None,
    certificacion: Optional[str] = None,
    precio_max: float = 100000,
    nivel_precio: int = 1,
    limite: int = 10
) -> List[Dict]:
    """
    Busca fuentes de poder (PSU) con filtros precisos.
    
    Args:
        watts_min: Watts mínimos (ej: 500, 650, 750)
        certificacion: Certificación (ej: "80 PLUS", "BRONZE", "GOLD", "PLATINUM")
        precio_max: Precio máximo
        nivel_precio: Nivel de precio (1-10)
        limite: Máximo de resultados
    """
    try:
        connection = conectar_bd()
        cursor = connection.cursor(dictionary=True)
        
        nivel_precio = max(1, min(10, nivel_precio))
        columna_precio = f"Precio{nivel_precio}"
        
        subfamilias = obtener_subfamilias("FUENTE_PODER")
        placeholders = ', '.join(['%s'] * len(subfamilias))
        
        conditions = [f"Subfamilia IN ({placeholders})"]
        params = list(subfamilias)
        
        if watts_min:
            conditions.append("Descripcion LIKE %s")
            params.append(f"%{watts_min}W%")
        
        if certificacion:
            conditions.append("(Descripcion LIKE %s OR Atributos_json LIKE %s)")
            cert_pattern = f"%{certificacion.upper()}%"
            params.extend([cert_pattern, cert_pattern])
        
        conditions.append(f"{columna_precio} <= %s")
        params.append(precio_max)
        
        conditions.append("Stock IS NOT NULL")
        
        query = f"""
            SELECT Noparte, Codigo, Descripcion, Marca, Stock, 
                   {columna_precio} as Precio, Atributos_json
            FROM producto_ensamble 
            WHERE {' AND '.join(conditions)}
            ORDER BY {columna_precio} ASC
            LIMIT %s
        """
        params.append(limite)
        
        cursor.execute(query, params)
        productos = cursor.fetchall()
        
        resultado = []
        for p in productos:
            try:
                stock_raw = json.loads(p['Stock']) if p['Stock'] else {}
                specs = json.loads(p['Atributos_json']) if p['Atributos_json'] else {}
            except:
                stock_raw = {}
                specs = {}
            
            if not stock_raw or sum(stock_raw.values()) == 0:
                continue
                
            resultado.append({
                "noparte": p['Noparte'],
                "descripcion": p['Descripcion'],
                "marca": p['Marca'],
                "precio": p['Precio'],
                "stock_formateado": _format_stock(stock_raw),
                "specs": specs
            })
            
        return _convert_decimals(resultado)
        
    except Exception as e:
        print(f"Error en buscar_fuentes_poder: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def buscar_gabinetes(
    factor_forma: Optional[str] = None,
    precio_max: float = 100000,
    nivel_precio: int = 1,
    limite: int = 10
) -> List[Dict]:
    """
    Busca gabinetes (cases) con filtros precisos.
    
    Args:
        factor_forma: Factor de forma (ej: "ATX", "MICRO ATX", "MINI ITX")
        precio_max: Precio máximo
        nivel_precio: Nivel de precio (1-10)
        limite: Máximo de resultados
    """
    try:
        connection = conectar_bd()
        cursor = connection.cursor(dictionary=True)
        
        nivel_precio = max(1, min(10, nivel_precio))
        columna_precio = f"Precio{nivel_precio}"
        
        subfamilias = obtener_subfamilias("GABINETE")
        placeholders = ', '.join(['%s'] * len(subfamilias))
        
        conditions = [f"Subfamilia IN ({placeholders})"]
        params = list(subfamilias)
        
        if factor_forma:
            conditions.append("(Descripcion LIKE %s OR Atributos_json LIKE %s)")
            forma_pattern = f"%{factor_forma.upper()}%"
            params.extend([forma_pattern, forma_pattern])
        
        conditions.append(f"{columna_precio} <= %s")
        params.append(precio_max)
        
        conditions.append("Stock IS NOT NULL")
        
        query = f"""
            SELECT Noparte, Codigo, Descripcion, Marca, Stock, 
                   {columna_precio} as Precio, Atributos_json
            FROM producto_ensamble 
            WHERE {' AND '.join(conditions)}
            ORDER BY {columna_precio} ASC
            LIMIT %s
        """
        params.append(limite)
        
        cursor.execute(query, params)
        productos = cursor.fetchall()
        
        resultado = []
        for p in productos:
            try:
                stock_raw = json.loads(p['Stock']) if p['Stock'] else {}
                specs = json.loads(p['Atributos_json']) if p['Atributos_json'] else {}
            except:
                stock_raw = {}
                specs = {}
            
            if not stock_raw or sum(stock_raw.values()) == 0:
                continue
                
            resultado.append({
                "noparte": p['Noparte'],
                "descripcion": p['Descripcion'],
                "marca": p['Marca'],
                "precio": p['Precio'],
                "stock_formateado": _format_stock(stock_raw),
                "specs": specs
            })
            
        return _convert_decimals(resultado)
        
    except Exception as e:
        print(f"Error en buscar_gabinetes: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

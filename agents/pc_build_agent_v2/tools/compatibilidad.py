"""
Herramienta de Compatibilidad de Componentes
Funciones para validar compatibilidad entre componentes de PC
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import Dict, Any, Optional, List
from consultas_productos import consultar_productos_por_categoria


def buscar_componentes_compatibles(
    tipo_componente: str,
    atributo_compatibilidad: str,
    valor_compatibilidad: str,
    nivel_precio: int = 1,
    limite: int = 20
) -> List[Dict[str, Any]]:
    """
    Obtiene componentes compatibles basados en atributos específicos
    
    Args:
        tipo_componente: Tipo de componente (subfamilia)
        atributo_compatibilidad: Nombre del atributo de compatibilidad
        valor_compatibilidad: Valor esperado del atributo
        nivel_precio: Nivel de precio a usar
        limite: Número máximo de resultados
        
    Returns:
        Lista de productos compatibles
    """
    # Obtener todos los productos de la categoría
    productos = consultar_productos_por_categoria(tipo_componente, nivel_precio, limite=limite)
    
    # Filtrar por compatibilidad en los atributos JSON
    compatibles = []
    for producto in productos:
        attrs = producto.get('Atributos_json', {})
        if isinstance(attrs, dict):
            # Buscar el atributo (case-insensitive)
            for key, value in attrs.items():
                if key.lower() == atributo_compatibilidad.lower():
                    if valor_compatibilidad.lower() in str(value).lower():
                        compatibles.append(producto)
                        break
    
    return compatibles[:limite]


def validar_compatibilidad_cpu_motherboard(cpu: Dict[str, Any], motherboard: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida si un CPU es compatible con una motherboard
    
    Args:
        cpu: Diccionario con información del CPU (debe incluir Atributos_json)
        motherboard: Diccionario con información de la motherboard
        
    Returns:
        Diccionario con resultado de validación
    """
    cpu_attrs = cpu.get('Atributos_json', {})
    mb_attrs = motherboard.get('Atributos_json', {})
    
    # Buscar socket en ambos componentes
    cpu_socket = None
    mb_socket = None
    
    for key, value in cpu_attrs.items():
        if 'socket' in key.lower():
            cpu_socket = str(value).strip()
            break
    
    for key, value in mb_attrs.items():
        if 'socket' in key.lower():
            mb_socket = str(value).strip()
            break
    
    if not cpu_socket or not mb_socket:
        return {
            'compatible': None,
            'razon': 'No se pudo determinar el socket de uno o ambos componentes',
            'cpu_socket': cpu_socket,
            'mb_socket': mb_socket
        }
    
    compatible = cpu_socket.lower() == mb_socket.lower()
    
    return {
        'compatible': compatible,
        'razon': 'Sockets coinciden' if compatible else f'Socket incompatible: CPU={cpu_socket}, MB={mb_socket}',
        'cpu_socket': cpu_socket,
        'mb_socket': mb_socket
    }


def validar_ram_motherboard(ram: Dict[str, Any], motherboard: Dict[str, Any]) -> Dict[str, Any]:
    """
    Valida si una memoria RAM es compatible con una motherboard
    
    Args:
        ram: Diccionario con información de la RAM
        motherboard: Diccionario con información de la motherboard
        
    Returns:
        Diccionario con resultado de validación
    """
    ram_attrs = ram.get('Atributos_json', {})
    mb_attrs = motherboard.get('Atributos_json', {})
    
    # Buscar tipo de memoria
    ram_tipo = None
    mb_tipo = None
    
    for key, value in ram_attrs.items():
        if 'tipo' in key.lower() or 'type' in key.lower():
            ram_tipo = str(value).upper()
            break
    
    for key, value in mb_attrs.items():
        if 'tipo de memoria' in key.lower() or 'memory type' in key.lower():
            mb_tipo = str(value).upper()
            break
    
    if not ram_tipo or not mb_tipo:
        return {
            'compatible': None,
            'razon': 'No se pudo determinar el tipo de memoria',
            'ram_tipo': ram_tipo,
            'mb_tipo': mb_tipo
        }
    
    # Verificar si hay coincidencia (DDR4, DDR5, etc.)
    compatible = any(tipo in mb_tipo for tipo in ['DDR4', 'DDR5'] if tipo in ram_tipo)
    
    return {
        'compatible': compatible,
        'razon': 'Tipos de memoria coinciden' if compatible else f'RAM incompatible: RAM={ram_tipo}, MB soporta {mb_tipo}',
        'ram_tipo': ram_tipo,
        'mb_tipo': mb_tipo
    }


def obtener_categorias_pc() -> Dict[str, List[str]]:
    """
    Retorna las categorías principales para ensamble de PC
    """
    return {
        'cpu': ['PROCESADORES', 'CPU', 'PROCESSOR'],
        'gpu': ['TARJETAS DE VIDEO', 'VIDEO', 'GRAPHICS', 'GPU'],
        'motherboard': ['TARJETAS MADRE', 'MOTHERBOARD', 'PLACA MADRE'],
        'ram': ['MEMORIAS RAM', 'MEMORIA', 'RAM', 'MEMORY'],
        'storage_ssd': ['SSD', 'ESTADO SOLIDO', 'SOLID STATE'],
        'storage_hdd': ['DISCOS DUROS', 'HDD', 'HARD DRIVE'],
        'psu': ['FUENTES DE PODER', 'POWER SUPPLY', 'PSU'],
        'case': ['GABINETES', 'CASE', 'CHASIS'],
        'cooling': ['ENFRIAMIENTO', 'COOLER', 'COOLING', 'VENTILADOR']
    }


def calcular_watts_requeridos(
    cpu_tdp: int,
    gpu_tdp: int,
    num_drives: int = 2,
    margen_seguridad: float = 1.2
) -> int:
    """
    Calcula watts mínimos requeridos para la fuente de poder.
    
    Args:
        cpu_tdp: TDP del procesador en watts
        gpu_tdp: TDP de la GPU en watts
        num_drives: Número de unidades de almacenamiento (default 2)
        margen_seguridad: Multiplicador de seguridad (default 1.2 = 20% extra)
    
    Returns:
        Watts mínimos recomendados para PSU
        
    Example:
        >>> calcular_watts_requeridos(cpu_tdp=65, gpu_tdp=220)
        414  # (65 + 220 + 20 + 50) * 1.2
    """
    # Componentes base
    drives_watts = num_drives * 10  # ~10W por drive
    otros_watts = 50  # Motherboard, RAM, ventiladores
    
    base_watts = cpu_tdp + gpu_tdp + drives_watts + otros_watts
    return int(base_watts * margen_seguridad)


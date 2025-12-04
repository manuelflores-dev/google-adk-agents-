"""
Módulo de Herramientas para PC Build Agent
Exporta todas las herramientas disponibles
"""

from .conexion_bd import conectar_bd
from .consultas_productos import (
    consultar_productos_por_categoria,
    buscar_productos,
    obtener_detalle_producto
)
from .verificar_stock import (
    verificar_stock,
    tiene_stock_minimo
)
from .compatibilidad import (
    buscar_componentes_compatibles,
    validar_compatibilidad_cpu_motherboard,
    validar_ram_motherboard,
    obtener_categorias_pc
)

__all__ = [
    # Conexión
    'conectar_bd',
    
    # Consultas
    'consultar_productos_por_categoria',
    'buscar_productos',
    'obtener_detalle_producto',
    
    # Stock
    'verificar_stock',
    'tiene_stock_minimo',
    
    # Compatibilidad
    'buscar_componentes_compatibles',
    'validar_compatibilidad_cpu_motherboard',
    'validar_ram_motherboard',
    'obtener_categorias_pc'
]

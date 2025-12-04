"""
Mapeo de categorías de productos a subfamilias en la base de datos.
Estos valores deben coincidir EXACTAMENTE con los valores de la columna 'Subfamilia' en producto_ensamble.
"""

SUBFAMILIAS_PC = {
    # ============== PROCESADORES ==============
    "PROCESADOR": [
        # Intel
        "PROCESADORES INTEL SOCKET 1851",
        "PROCESADORES INTEL SOCKET 1700 14ª GEN", 
        "PROCESADORES INTEL SOCKET 1700 13° GEN",
        "PROCESADORES INTEL SOCKET 1700 12° GEN",
        "PROCESADORES INTEL SOCKET 1200",
        # AMD
        "PROCESADORES AMD SOCKET AM5",
        "PROCESADORES AMD SOCKET AM4",
    ],
    
    # ============== TARJETAS MADRE ==============
    "MOTHERBOARD": [
        # Intel
        "T. MADRE SOCKET 1851 (INTEL)",
        "T. MADRE SOCKET 1700 (INTEL",  # Nota: Aparece sin el paréntesis de cierre en la BD
        "T.MADRE SOCKET 1200 (INTEL)",
        # AMD
        "T. MADRE SOCKET AM5 (AMD)",
        "T. MADRE SOCKET AM4 (AMD)",
    ],
    
    # ============== MEMORIA RAM ==============
    "RAM": [
        # DDR5 DIMM (para Desktop)
        "MEMORIAS RAM DIMM DDR5",
        # DDR4 DIMM (para Desktop)
        "MEMORIAS RAM DIMM DDR4",
        # DDR5 SODIMM (para Laptop, solo si necesario)
        "MEMORIAS RAM SODIMM PARA LAPTOP DDR5",
        # DDR4 SODIMM (para Laptop, solo si necesario)
        "MEMORIAS RAM SODIMM PARA LAPTOP DDR4",
        # DDR3 SODIMM (legacy, probablemente no usar)
        "MEMORIAS RAM SODIMM PARA LAPTOP DDR3",
    ],
    
    # ============== TARJETAS GRÁFICAS ==============
    "GPU": [
        "TARJETAS DE VIDEO PCI-EXP",
        "TARJETA DE VIDEO  PCI",  # Nota: tiene doble espacio en la BD
    ],
    
    # ============== ALMACENAMIENTO ==============
    "SSD": [
        "SSD UNIDADES DE ESTADO SOLIDO",
        "SSD EXTERNOS",
    ],
    
    "HDD_INTERNO": [
        "DISCOS DUROS SATA 3.5 PULGADAS",
    ],
    
    "HDD_EXTERNO": [
        "DISCOS DUROS EXTERNOS",
    ],
    
    # ============== COMPONENTES DE SOPORTE ==============
    "FUENTE_PODER": [
        "FUENTES DE PODER",
    ],
    
    "GABINETE": [
        "GABINETES COMPUTADORA",
    ],
    
    "COOLER": [
        "DISIPADORES Y VENTILADORES PARA PROCESADOR",
    ],
    
    "VENTILADOR": [
        "VENTILADORES PARA GABINETE",
    ],
    
    "ENCLOSURE": [
        "ENCLOSURE PARA DISCOS DUROS",
    ],
    
    # ============== ACCESORIOS ==============
    "PASTA_TERMICA": [
        "PASTA TERMICA PARA PROCESADORES",
    ],
    
    "ILUMINACION": [
        "ILUMINACIÓN PARA GABINETES",
    ],
    
    "SOPORTE_GPU": [
        "SOPORTES TARJETA DE VIDEO",
    ],
    
    "BASE_GABINETE": [
        "BASES PARA GABINETES",
    ],
    
    # ============== LIMPIEZA ==============
    "LIMPIEZA": [
        "TOALLAS ANTIESTATICAS",
        "KIT DE LIMPIEZA",
        "LIMPIADOR ANTIESTATICO PARA PANTALLAS",
        "LIMPIADOR TARJETAS ELECTRONICAS",
        "ESPUMA LIMPIADORA",
        "AIRE COMPRIMIDO",
        "ALCOHOL ISOPROPILICO",
    ],
    
    # ============== ALMACENAMIENTO PORTÁTIL ==============
    "USB": [
        "MEMORIAS USB",
    ],
    
    "SD": [
        "MEMORIAS SD (SECURE DIGITAL)",
        "MEMORIAS MICRO SD",
    ],
}

# Mapeo inverso: código -> categoría
CODIGO_A_CATEGORIA = {}
for categoria, codigos in SUBFAMILIAS_PC.items():
    for codigo in codigos:
        CODIGO_A_CATEGORIA[codigo] = categoria


def obtener_subfamilias(categoria: str) -> list:
    """
    Retorna las subfamilias válidas para una categoría.
    
    Args:
        categoria: Nombre de categoría (ej: "PROCESADOR", "GPU", "RAM")
        
    Returns:
        Lista de códigos de subfamilia para filtrar en consultas SQL
        
    Example:
        >>> obtener_subfamilias("PROCESADOR")
        ['CPU', 'PROCESADORES', 'PR']
    """
    return SUBFAMILIAS_PC.get(categoria.upper(), [])


def identificar_categoria(subfamilia_codigo: str) -> str:
    """
    Identifica la categoría a partir de un código de subfamilia.
    
    Args:
        subfamilia_codigo: Código de subfamilia (ej: "DIS", "FP")
        
    Returns:
        Nombre de categoría o "DESCONOCIDO"
        
    Example:
        >>> identificar_categoria("DIS")
        'COOLER'
    """
    return CODIGO_A_CATEGORIA.get(subfamilia_codigo.upper(), "DESCONOCIDO")


def listar_categorias_principales() -> list:
    """Retorna lista de categorías principales para ensamblaje PC"""
    return [
        "PROCESADOR",
        "MOTHERBOARD",
        "RAM",
        "GPU",
        "SSD",
        "HDD_INTERNO",
        "FUENTE_PODER",
        "GABINETE",
        "COOLER"
    ]


def es_componente_principal(subfamilia_codigo: str) -> bool:
    """
    Verifica si un código de subfamilia pertenece a componentes principales de PC.
    
    Args:
        subfamilia_codigo: Código de subfamilia
        
    Returns:
        True si es componente principal, False si no
    """
    categoria = identificar_categoria(subfamilia_codigo)
    return categoria in listar_categorias_principales()

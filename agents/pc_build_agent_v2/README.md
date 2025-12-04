# PC Build Expert AI - v2

Agente especializado en diseño, ensamble, compatibilidad técnica y cotización profesional de equipos de cómputo para **Zegucom**.

## 🚀 Inicio Rápido

```bash
# Desde el directorio del agente
cd agents/pc_build_agent_v2

# Ejecutar con ADK
adk dev-ui
```

## 📁 Estructura

```
pc_build_agent_v2/
├── agent.py          # Agente principal con instrucciones completas
├── .env              # Variables de entorno (DB config)
├── __init__.py
└── tools/
    ├── busquedas_especializadas.py  # Búsqueda de componentes
    ├── compatibilidad.py             # Validación de compatibilidades
    ├── conexion_bd.py                # Conexión a MariaDB
    ├── verificar_stock.py            # Verificación de stock
    ├── subfamilia_map.py             # Mapeo de categorías
    └── consultas_productos.py        # Consultas genéricas
```

## ⚙️ Configuración

Edita `.env` con tus credenciales:

```env
GOOGLE_API_KEY=tu_api_key
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_NAME=tu_base_de_datos
```

## 🎯 Funcionalidades

- **Recolección de requisitos**: Pregunta uso, presupuesto, preferencias
- **Búsqueda optimizada**: 7 categorías de componentes
- **Validación de compatibilidad**: CPU-MB, RAM-MB, cálculo de watts
- **3 configuraciones**: Economía, Balance, Premium
- **Stock en tiempo real**: Consulta vista `producto_ensamble`

## 📝 Vista de BD Requerida

El agente usa la vista `producto_ensamble` con:
- Noparte, Codigo, Descripcion, Marca
- Precio1..Precio10
- Stock (JSON por sucursal)
- Atributos_json (especificaciones)

# 🤖 Google ADK Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Google ADK](https://img.shields.io/badge/Google-ADK-4285F4?logo=google)](https://developers.google.com/)
[![Status](https://img.shields.io/badge/Status-Active-success)]()

> Una colección de agentes inteligentes desarrollados con Google Agent Development Kit (ADK) para automatizar tareas, procesar información y proporcionar soluciones basadas en IA.

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Agentes Disponibles](#-agentes-disponibles)
- [Uso](#-uso)
- [Desarrollo](#-desarrollo)
- [Ejemplos](#-ejemplos)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

## 🎯 Descripción

Este repositorio contiene una colección de agentes inteligentes construidos utilizando el **Google Agent Development Kit (ADK)**. El ADK permite crear agentes conversacionales y autónomos que pueden realizar tareas complejas, integrarse con APIs externas, y proporcionar experiencias interactivas impulsadas por modelos de lenguaje de última generación.

Los agentes en este repositorio están diseñados para ser modulares, escalables y fáciles de extender, siguiendo las mejores prácticas de desarrollo con Google ADK.

## ✨ Características

- 🚀 **Agentes Modulares**: Cada agente está diseñado como un módulo independiente y reutilizable
- 🔧 **Configuración Flexible**: Sistema de configuración basado en variables de entorno
- 📊 **Logging Avanzado**: Sistema completo de logs para debugging y monitoreo
- 🔄 **Integración con APIs**: Conexión fácil con servicios externos y APIs de terceros
- 💬 **Conversaciones Contextuales**: Manejo inteligente del contexto en conversaciones
- 🎨 **Personalización**: Fácil personalización de comportamiento y respuestas
- 🧪 **Testing**: Suite de pruebas para garantizar calidad y confiabilidad
- 📚 **Documentación Completa**: Documentación detallada para cada agente

## 📦 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Google Cloud Platform
- API Key de Google ADK
- Git

## 🚀 Instalación

1. **Clona el repositorio:**

```bash
git clone https://github.com/tuusuario/google-adk-agents.git
cd google-adk-agents
```

2. **Crea un entorno virtual:**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias:**

```bash
pip install -r requirements.txt
```

4. **Instala Google ADK:**

```bash
pip install google-adk
```

## ⚙️ Configuración

1. **Crea un archivo `.env` en la raíz del proyecto:**

```env
# Google ADK Configuration
GOOGLE_API_KEY=tu_api_key_aqui
GOOGLE_PROJECT_ID=tu_project_id
GOOGLE_ADK_MODEL=gemini-pro

# Agent Configuration
AGENT_NAME=mi-agente
AGENT_DESCRIPTION=Descripción de mi agente
MAX_TOKENS=2048
TEMPERATURE=0.7

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/agent.log
```

2. **Configura las credenciales de Google Cloud:**

```bash
gcloud auth application-default login
gcloud config set project TU_PROJECT_ID
```

## 📁 Estructura del Proyecto

```
google-adk-agents/
├── agents/                 # Directorio de agentes
│   ├── __init__.py
│   ├── base_agent.py      # Clase base para agentes
│   ├── chat_agent.py      # Agente de chat conversacional
│   ├── task_agent.py      # Agente de tareas específicas
│   └── custom_agent.py    # Tu agente personalizado
├── config/                 # Configuraciones
│   ├── __init__.py
│   └── settings.py
├── utils/                  # Utilidades
│   ├── __init__.py
│   ├── logger.py
│   └── helpers.py
├── tests/                  # Pruebas unitarias
│   ├── __init__.py
│   └── test_agents.py
├── examples/               # Ejemplos de uso
│   ├── basic_chat.py
│   └── advanced_agent.py
├── logs/                   # Archivos de log
├── .env.example           # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

## 🤖 Agentes Disponibles

### 1. Chat Agent
Agente conversacional básico para interacciones de chat.

**Características:**
- Conversación natural y contextual
- Memoria de conversación
- Respuestas personalizadas

### 2. Task Agent
Agente especializado en ejecutar tareas específicas.

**Características:**
- Ejecución de comandos
- Integración con APIs
- Procesamiento de datos

### 3. Custom Agent
Plantilla para crear tus propios agentes personalizados.

**Características:**
- Base extensible
- Fácil personalización
- Hooks para funcionalidades adicionales

## 💻 Uso

### Uso Básico

```python
from agents.chat_agent import ChatAgent

# Inicializar el agente
agent = ChatAgent(
    name="MiAsistente",
    model="gemini-pro"
)

# Enviar un mensaje
response = agent.chat("Hola, ¿cómo estás?")
print(response)

# Conversación con contexto
response = agent.chat("¿Puedes ayudarme con una tarea?")
print(response)
```

### Uso Avanzado

```python
from agents.task_agent import TaskAgent
from config.settings import load_config

# Cargar configuración
config = load_config()

# Crear agente con configuración personalizada
agent = TaskAgent(
    name="TaskExecutor",
    model=config.model,
    temperature=config.temperature,
    max_tokens=config.max_tokens
)

# Ejecutar tarea
result = agent.execute_task({
    "action": "process_data",
    "data": "datos_a_procesar",
    "options": {"format": "json"}
})

print(result)
```

### Ejecutar desde CLI

```bash
# Ejecutar agente de chat
python -m agents.chat_agent

# Ejecutar agente de tareas
python -m agents.task_agent --task "tu_tarea"

# Modo interactivo
python run_agent.py --interactive
```

## 🛠️ Desarrollo

### Crear un Nuevo Agente

1. **Crea un nuevo archivo en `agents/`:**

```python
from agents.base_agent import BaseAgent

class MiNuevoAgente(BaseAgent):
    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)
        self.setup()
    
    def setup(self):
        """Configuración inicial del agente"""
        pass
    
    def process(self, input_data):
        """Lógica principal del agente"""
        response = self.generate_response(input_data)
        return response
    
    def custom_function(self):
        """Funcionalidad personalizada"""
        pass
```

2. **Registra tu agente en `agents/__init__.py`:**

```python
from .mi_nuevo_agente import MiNuevoAgente

__all__ = ['BaseAgent', 'ChatAgent', 'TaskAgent', 'MiNuevoAgente']
```

### Testing

```bash
# Ejecutar todas las pruebas
pytest tests/

# Ejecutar pruebas específicas
pytest tests/test_agents.py -v

# Ejecutar con cobertura
pytest --cov=agents tests/
```

## 📖 Ejemplos

### Ejemplo 1: Asistente de Código

```python
from agents.chat_agent import ChatAgent

code_assistant = ChatAgent(
    name="CodeAssistant",
    system_prompt="Eres un experto en programación que ayuda a resolver problemas de código."
)

response = code_assistant.chat(
    "¿Cómo puedo optimizar este bucle en Python?"
)
print(response)
```

### Ejemplo 2: Procesador de Documentos

```python
from agents.task_agent import TaskAgent

doc_processor = TaskAgent(name="DocProcessor")

result = doc_processor.execute_task({
    "action": "summarize",
    "document": "ruta/al/documento.txt",
    "length": "short"
})

print(result.summary)
```

### Ejemplo 3: Agente Multi-Idioma

```python
from agents.chat_agent import ChatAgent

multilang_agent = ChatAgent(
    name="MultiLangAgent",
    model="gemini-pro"
)

# Español
response_es = multilang_agent.chat("Hola, ¿cómo estás?")

# Inglés
response_en = multilang_agent.chat("Hello, how are you?")
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres contribuir a este proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Sigue el estilo de código PEP 8
- Añade tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Asegúrate de que todas las pruebas pasen

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- Google por el Agent Development Kit
- La comunidad de desarrolladores de IA
- Todos los contribuidores del proyecto

## 📞 Contacto

- **Issues**: [GitHub Issues](https://github.com/tuusuario/google-adk-agents/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/tuusuario/google-adk-agents/discussions)

---

⭐ Si este proyecto te ha sido útil, considera darle una estrella en GitHub!

**Hecho con ❤️ usando Google ADK**
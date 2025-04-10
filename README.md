# AzureBeach

Sistema automatizado de evaluación y mitigación de eventos críticos en Azure utilizando LLMs, Azure AI y Logic Apps.

## 🚀 Objetivo

Monitorizar eventos como la creación de recursos en Azure y actuar de forma automática ante comportamientos sospechosos o críticos, como:

- Borrar grupos de recursos no autorizados
- Detener o eliminar VMs
- Deshabilitar usuarios

## ⚙️ Tecnologías empleadas

- **Azure Logic Apps** + **Event Grid**
- **Azure AI Projects** (Evaluador y Ejecutor)
- **Azure SDK for Python**
- **Contenedor DevContainer + Conda**

---

## 🌐 Estructura del proyecto

### `.devcontainer/`

- `devcontainer.json`: Configuración del entorno VSCode
- `Dockerfile`: Python 3.13 + Miniconda + entorno `azurebeach`
- `requirements.txt`: Dependencias del entorno

### `setup/`

- `*.bicep`: Scripts para configurar Azure AI Hub y Projects
- `deploy.sh`: Script para desplegar los recursos necesarios

### `workshop/`

#### Archivos principales

- `main.py`: Entrada del sistema. Lógica completa de evaluación y mitigación
- `.env`: Variables como `MODEL_DEPLOYMENT_NAME`, `PROJECT_CONNECTION_STRING`

#### `agents/`

- `evaluator_agent.py`: Crea o recupera el agente evaluador
- `executor_agent.py`: Crea o recupera el agente ejecutor

#### `prompts/`

- `evaluator.txt`: Prompt para el evaluador (solo devuelve JSON)
- `executor.txt`: Prompt para el ejecutor

#### `tools/`

- `evaluate_tool.py`: Devuelve juicio sobre una alerta
- `mitigate_tool.py`: Redirige la alerta a la acción adecuada
- `delete_resource_group.py`: Borra RG con Azure SDK
- `vm_actions.py`:
  - `delete_virtual_machine` → si OS es Windows
  - `stop_virtual_machine` → si OS es Linux
- `disable_user.py`: Deshabilita usuario con Microsoft Graph

#### `utilities/`

- `utilities.py`: Funciones de logging, carga de instrucciones, subida de archivos, etc.
- `terminal_colors.py`: Estilos de texto para consola
- `utils.py`: Auxiliar

#### Otros

- `stream_event_handler.py`: Manejador de eventos en streaming desde Azure AI

---

## ✅ Flujo general

1. Logic App recibe evento (p. ej. creación de RG)
2. Envía el evento al agente evaluador (Azure AI)
3. Evaluador decide si es crítico (JSON estructurado)
4. Si es crítico → ejecutor realiza la acción real (borrar RG, detener VM, etc.)
5. Resultado mostrado en consola

---

## 🌐 Lógica de mitigación

```python
if operation == "resourceGroups/write":
    delete_resource_group()
elif operation == "virtualMachines/delete" or OS == "Windows":
    delete_virtual_machine()
elif OS == "Linux":
    stop_virtual_machine()
elif operation == "graph.microsoft.com/users":
    disable_user()
```

---

## 🎧 Recomendaciones

- Usa `az login` dentro del contenedor si usas `DefaultAzureCredential`
- Ejecuta `main.py` para iniciar el sistema manualmente o automatízalo con un `supervisor` o `cron`

---

## ⚡ Pendiente

- Conexión directa desde Logic App al contenedor (WebSocket / webhook)
- Persistencia de estado / logs
- Mejoras UX para consola o dashboard web

---

## 📦 Licencia

MIT

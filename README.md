# AzureBeach

Sistema automatizado de evaluación y mitigación de eventos críticos en Azure utilizando LLMs, Azure AI y Logic Apps.

## 🚀 Objetivo

Monitorizar eventos críticos en Azure y actuar automáticamente ante comportamientos sospechosos o no autorizados, como:

- Borrar grupos de recursos no autorizados
- Detener o eliminar máquinas virtuales
- Deshabilitar usuarios en Azure AD

## ⚙️ Tecnologías empleadas

- **Azure Logic Apps** + **Event Grid**: Para recibir y procesar eventos en tiempo real.
- **Azure AI Projects**: Implementación de agentes evaluadores y ejecutores.
- **Azure SDK for Python**: Para interactuar con los recursos de Azure.
- **Contenedor DevContainer**: Entorno de desarrollo basado en Docker y Conda.

---

## 🌐 Estructura del proyecto

### `.devcontainer/`

- `devcontainer.json`: Configuración del entorno de desarrollo en VSCode.
- `Dockerfile`: Imagen base con Python 3.13, Miniconda y dependencias del proyecto.
- `requirements.txt`: Lista de dependencias necesarias.

### `setup/`

- `*.bicep`: Scripts para configurar recursos en Azure (AI Hub, Projects, etc.).
- `deploy.sh`: Script para desplegar los recursos necesarios en Azure.

### `workshop/`

#### Archivos principales

- `main.py`: Entrada principal del sistema. Contiene la lógica de evaluación y mitigación.
- `.env`: Variables de entorno como `MODEL_DEPLOYMENT_NAME` y `PROJECT_CONNECTION_STRING`.

#### `agents/`

- `evaluator_agent.py`: Lógica para crear o recuperar el agente evaluador.
- `executor_agent.py`: Lógica para crear o recuperar el agente ejecutor.

#### `prompts/`

- `evaluator.txt`: Prompt para el evaluador (devuelve JSON estructurado).
- `executor.txt`: Prompt para el ejecutor (realiza acciones de mitigación).

#### `tools/`

- `evaluate_tool.py`: Evalúa alertas y devuelve un juicio.
- `mitigate_tool.py`: Redirige alertas a las acciones de mitigación correspondientes.
- `delete_resource_group.py`: Borra grupos de recursos utilizando el Azure SDK.
- `vm_actions.py`:
  - `delete_virtual_machine`: Elimina máquinas virtuales (Windows).
  - `stop_virtual_machine`: Detiene máquinas virtuales (Linux).
- `disable_user.py`: Deshabilita usuarios en Azure AD utilizando Microsoft Graph.

#### `utilities/`

- `utilities.py`: Funciones auxiliares como logging, carga de instrucciones y manejo de archivos.
- `terminal_colors.py`: Estilos de texto para la consola.
- `utils.py`: Funciones auxiliares adicionales.

#### Otros

- `stream_event_handler.py`: Manejador de eventos en streaming desde Azure AI.

---

## ✅ Flujo general

1. **Recepción del evento**: Logic App recibe un evento (por ejemplo, creación de un grupo de recursos).
2. **Evaluación**: El evento se envía al agente evaluador (Azure AI), que decide si es crítico.
3. **Mitigación**: Si el evento es crítico, el agente ejecutor realiza la acción correspondiente (borrar RG, detener VM, etc.).
4. **Resultado**: El resultado de la acción se muestra en la consola.

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

- **Autenticación**: Usa `az login` dentro del contenedor si utilizas `DefaultAzureCredential`.
- **Ejecución manual**: Ejecuta `main.py` para iniciar el sistema manualmente.
- **Automatización**: Configura un `supervisor` o `cron` para ejecutar el sistema automáticamente.

---

## ⚡ Pendiente

- **Integración directa**: Conexión desde Logic App al contenedor mediante WebSocket o webhook.
- **Persistencia**: Implementar almacenamiento de estado y logs.
- **Mejoras UX**: Crear un dashboard web o mejorar la experiencia en consola.

---

## 📦 Licencia

MIT

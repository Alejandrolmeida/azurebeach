import asyncio
import os
import json
from dotenv import load_dotenv

from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import AsyncFunctionTool

from agents.evaluator_agent import get_or_create_evaluator_agent
from agents.executor_agent import get_or_create_executor_agent
from tools.evaluate_tool import evaluate_alert
from tools.mitigate_tool import mitigate_alert
from stream_event_handler import StreamEventHandler

load_dotenv()

MODEL_DEPLOYMENT_NAME = os.getenv("MODEL_DEPLOYMENT_NAME")
PROJECT_CONNECTION_STRING = os.getenv("PROJECT_CONNECTION_STRING")
PROMPT_EVALUATOR = "prompts/evaluator.txt"
PROMPT_EXECUTOR = "prompts/executor.txt"


async def main():
    print("🧠 Inicializando entorno...")

    credential = DefaultAzureCredential()
    project_client = AIProjectClient.from_connection_string(
        conn_str=PROJECT_CONNECTION_STRING,
        credential=credential
    )

    print("🔍 Buscando o creando agentes...")
    evaluator = await get_or_create_evaluator_agent(project_client, MODEL_DEPLOYMENT_NAME, PROMPT_EVALUATOR)
    executor = await get_or_create_executor_agent(project_client, MODEL_DEPLOYMENT_NAME, PROMPT_EXECUTOR)

    print("🧵 Creando hilos de conversación...")
    eval_thread = await project_client.agents.create_thread()
    exec_thread = await project_client.agents.create_thread()

    print(f"✅ Agentes creados: Evaluador ({evaluator.id}), Ejecutor ({executor.id})")

    eval_handler = StreamEventHandler(
        functions=AsyncFunctionTool({evaluate_alert}),
        project_client=project_client
    )

    exec_handler = StreamEventHandler(
        functions=AsyncFunctionTool({mitigate_alert}),
        project_client=project_client
    )

    while True:
        user_input = input("\n🚨 Introduce una alerta (en JSON o texto simple), o escribe 'exit': ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue

        # Paso 1: Crear mensaje en el hilo del evaluador
        await project_client.agents.create_message(
            thread_id=eval_thread.id,
            role="user",
            content=user_input
        )

        print("\n🔍 Evaluador analizando...")

        run = await project_client.agents.create_run(
            thread_id=eval_thread.id,
            agent_id=evaluator.id
        )

        while run.status != "completed":
            run = await project_client.agents.get_run(thread_id=eval_thread.id, run_id=run.id)

            if run.status == "requires_action":
                tool_outputs = []

                for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                    args = json.loads(tool_call.function.arguments)
                    print("🧪 Ejecutando función:", tool_call.function.name)
                    result = await evaluate_alert(**args)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": result,
                    })

                await project_client.agents.submit_tool_outputs_to_run(
                    thread_id=eval_thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )

            elif run.status == "failed":
                print("❌ La ejecución del evaluador falló:", run.last_error)
                break

        # Obtener respuesta del evaluador
        messages = await project_client.agents.list_messages(thread_id=eval_thread.id)
        eval_response = messages.data[0].content[0].text.value if messages.data else ""

        # Intenta decodificar la respuesta como JSON
        try:
            eval_json = json.loads(eval_response)
            eval_response = json.dumps(eval_json)  # Normalizamos JSON en una sola línea
        except Exception:
            print("⚠️ La respuesta del evaluador no es un JSON válido. No se puede mitigar.")
            continue


        print("\n✅ Evaluación completada.\n📨 Resultado:\n", eval_response)

        if not eval_response.strip():
            print("⚠️ No se obtuvo respuesta del evaluador.")
            continue

        print("\n📤 Enviando al ejecutor:\n", eval_response)
        
        # Paso 2: Enviar al ejecutor
        await project_client.agents.create_message(
            thread_id=exec_thread.id,
            role="user",
            content=eval_response
        )

        print("\n🛠 Ejecutando acción de mitigación...")

        stream_exec = await project_client.agents.create_stream(
            thread_id=exec_thread.id,
            agent_id=executor.id,
            event_handler=exec_handler,
            instructions=executor.instructions
        )

        async with stream_exec as stream:
            async for event in stream:
                if hasattr(event, "delta") and event.delta and event.delta.content:
                    print(event.delta.content, end="", flush=True)

        print("\n✅ Mitigación completada.")

    """ print("\n🧹 Limpiando recursos...")
    await project_client.agents.delete_agent(evaluator.id)
    await project_client.agents.delete_agent(executor.id)
    await project_client.agents.delete_thread(eval_thread.id)
    await project_client.agents.delete_thread(exec_thread.id)

    print("🏁 Todo limpio. Fin del programa.") """


if __name__ == "__main__":
    asyncio.run(main())

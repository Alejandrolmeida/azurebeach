from azure.ai.projects.models import Agent, AsyncToolSet, AsyncFunctionTool
from tools.mitigate_tool import mitigate_alert
from utilities.utils import load_prompt


async def get_or_create_executor_agent(project_client, model_name: str, prompt_path: str) -> Agent:
    AGENT_NAME = "Executor Agent"

    raw_list = await project_client.agents.list_agents()
    agent_dicts = raw_list.get("data", [])

    for agent_meta in agent_dicts:
        if agent_meta["name"] == AGENT_NAME:
            print(f"♻️ Reutilizando agente existente: {AGENT_NAME}")
            return await project_client.agents.get_agent(agent_meta["id"])

    print(f"✨ Creando nuevo agente: {AGENT_NAME}")

    instructions = load_prompt(prompt_path)

    toolset = AsyncToolSet()
    toolset.add(AsyncFunctionTool({mitigate_alert}))

    agent = await project_client.agents.create_agent(
        model=model_name,
        name=AGENT_NAME,
        instructions=instructions,
        toolset=toolset,
        temperature=0.1,
        headers={"x-ms-enable-preview": "true"},
    )

    return agent

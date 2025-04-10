from azure.identity.aio import DefaultAzureCredential
from msgraph.core import GraphClient

async def disable_user(user_principal_name: str) -> str:
    credential = DefaultAzureCredential()
    async with credential:
        client = GraphClient(credential=credential)
        response = await client.patch(
            f"/users/{user_principal_name}",
            json={"accountEnabled": False}
        )
        if response.status_code == 204:
            return f"✅ Usuario '{user_principal_name}' deshabilitado correctamente."
        return f"⚠️ Fallo al deshabilitar el usuario '{user_principal_name}'. Código: {response.status_code}"

import asyncio
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient

def _delete_rg(resource_group_name: str, subscription_id: str) -> str:
    try:
        credential = DefaultAzureCredential()
        client = ResourceManagementClient(credential, subscription_id)
        delete_async_operation = client.resource_groups.begin_delete(resource_group_name)
        delete_async_operation.result()
        return f"✅ Grupo de recursos '{resource_group_name}' eliminado correctamente."
    except Exception as e:
        return f"❌ Error al eliminar el grupo de recursos '{resource_group_name}': {str(e)}"

async def delete_resource_group(resource_group_name: str, subscription_id: str) -> str:
    return await asyncio.to_thread(_delete_rg, resource_group_name, subscription_id)

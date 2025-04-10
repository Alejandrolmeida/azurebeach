# tools/vm_actions.py

import asyncio
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

def _delete_vm(vm_name: str, resource_group: str, subscription_id: str) -> str:
    credential = DefaultAzureCredential()
    client = ComputeManagementClient(credential, subscription_id)
    delete_async_operation = client.virtual_machines.begin_delete(resource_group, vm_name)
    delete_async_operation.result()
    return f"🗑️ VM '{vm_name}' eliminada del grupo '{resource_group}'."

def _stop_vm(vm_name: str, resource_group: str, subscription_id: str) -> str:
    credential = DefaultAzureCredential()
    client = ComputeManagementClient(credential, subscription_id)
    stop_async_operation = client.virtual_machines.begin_power_off(resource_group, vm_name)
    stop_async_operation.result()
    return f"🛑 VM '{vm_name}' detenida correctamente en el grupo '{resource_group}'."

def _handle_by_os(vm_name: str, resource_group: str, subscription_id: str) -> str:
    credential = DefaultAzureCredential()
    client = ComputeManagementClient(credential, subscription_id)
    vm = client.virtual_machines.get(resource_group, vm_name)
    os_type = vm.storage_profile.os_disk.os_type.value.lower()

    if os_type == "windows":
        return _delete_vm(vm_name, resource_group, subscription_id)
    elif os_type == "linux":
        return _stop_vm(vm_name, resource_group, subscription_id)
    else:
        return f"⚠️ Tipo de SO no reconocido para VM '{vm_name}'. No se tomó acción."

async def delete_virtual_machine(vm_name: str, resource_group: str, subscription_id: str) -> str:
    return await asyncio.to_thread(_delete_vm, vm_name, resource_group, subscription_id)

async def stop_virtual_machine(vm_name: str, resource_group: str, subscription_id: str) -> str:
    return await asyncio.to_thread(_stop_vm, vm_name, resource_group, subscription_id)

async def handle_vm_by_os_type(vm_name: str, resource_group: str, subscription_id: str) -> str:
    return await asyncio.to_thread(_handle_by_os, vm_name, resource_group, subscription_id)

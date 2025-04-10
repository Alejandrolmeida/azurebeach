import json
from tools.delete_resource_group import delete_resource_group
from tools.disable_user import disable_user
from tools.vm_actions import (
    delete_virtual_machine,
    stop_virtual_machine,
    handle_vm_by_os_type
)

async def mitigate_alert(alert_json: str) -> str:
    """
    Enruta la alerta a la función de mitigación correspondiente según el tipo de operación.
    """

    try:
        alert = json.loads(alert_json)

        operation = alert.get("operation", "").lower()
        subscription = alert.get("subscription", "")
        resource = alert.get("resource", "")
        resource_group = alert.get("resourceGroup", "")
        user = alert.get("user", "")

        print("🧪 Mitigate input:", alert_json)

        # ✅ Eliminar grupo de recursos
        if "resourcegroups" in operation and "write" in operation:
            return await delete_resource_group(
                resource_group_name=resource,
                subscription_id=subscription
            )

        # ✅ Acciones condicionales según el tipo de SO de la VM
        if "virtualmachines" in operation and "write" in operation:
            return await handle_vm_by_os_type(
                vm_name=resource,
                resource_group=resource_group,
                subscription_id=subscription
            )

        # ✅ Eliminar VM directamente (por ejemplo, si es explícito en la alerta)
        if "virtualmachines" in operation and "delete" in operation:
            return await delete_virtual_machine(
                vm_name=resource,
                resource_group=resource_group,
                subscription_id=subscription
            )

        # ✅ Deshabilitar usuario
        if "disable_user" in operation or "graph.microsoft.com/v1.0/users" in operation:
            return await disable_user(user_principal_name=user)

        # 🟡 Acción no necesaria
        return (
            f"Acción ejecutada: Ninguna\n"
            f"Motivo: Operación no requiere mitigación ({operation})\n"
            f"Resultado: Acción no requerida"
        )

    except Exception as e:
        return (
            f"Acción ejecutada: Ninguna\n"
            f"Motivo: Error al procesar la alerta\n"
            f"Resultado: Error - {str(e)}"
        )

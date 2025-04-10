import json

async def evaluate_alert(alert_json: str) -> str:
    """
    Evalúa una alerta y devuelve un juicio con los datos necesarios para la mitigación.
    Solo evalúa eventos de la suscripción '8d2c636f-918d-4ef6-8454-8f5f4b086e72'.
    """

    try:
        alert = json.loads(alert_json)

        operation = alert.get("operationName", "").lower()
        user = alert.get("caller", "desconocido")
        resource_id = alert.get("resourceId", "")
        subscription = alert.get("subscriptionId", "")
        resource_group = alert.get("resourceGroupName", "")

        # Solo se evalúa si es de la suscripción esperada
        monitored_subscription = "8d2c636f-918d-4ef6-8454-8f5f4b086e72"
        if subscription != monitored_subscription:
            return json.dumps({
                "evaluacion": "BENIGNA",
                "motivo": f"Suscripción fuera del alcance de evaluación ({subscription})",
                "accion_recomendada": "Ninguna"
            })

        # Análisis crítico
        if "resourcegroups" in operation and "write" in operation:
            return json.dumps({
                "evaluacion": "CRITICA",
                "motivo": f"Creación de grupo de recursos por {user}",
                "accion_recomendada": "Requiere mitigación",
                "operation": operation,
                "resource": resource_id.split("/")[-1],
                "resourceGroup": resource_group,
                "subscription": subscription,
                "user": user
            })

        return json.dumps({
            "evaluacion": "BENIGNA",
            "motivo": f"Operación sin riesgo detectado ({operation})",
            "accion_recomendada": "Ninguna"
        })

    except Exception as e:
        return json.dumps({
            "evaluacion": "ERROR",
            "motivo": f"No se pudo procesar la alerta: {str(e)}",
            "accion_recomendada": "Revisión manual"
        })

#!/bin/bash

echo "🔧 Deploying GPT-4o environment to Azure..."

# Cargar configuración desde .env
ENV_FILE="workshop/.env"

if [ -f "$ENV_FILE" ]; then
  echo "📥 Loading configuration from $ENV_FILE"
  set -o allexport
  source "$ENV_FILE"
  set +o allexport
else
  echo "❌ .env file not found at $ENV_FILE"
  exit 1
fi


# Crear grupo de recursos si no existe
echo "📦 Checking resource group..."
az group show --name "$RG_NAME" >/dev/null 2>&1 || {
    echo "📁 Resource group not found. Creating..."
    az group create --name "$RG_NAME" --location "$RG_LOCATION"
}

# Desplegar recursos y guardar salida
echo "🚀 Starting Bicep deployment..."
az deployment group create \
  --resource-group "$RG_NAME" \
  --template-file setup/main.bicep \
  --parameters \
      aiHubName="$AI_HUB_NAME" \
      aiHubFriendlyName="$AI_HUB_FRIENDLY_NAME" \
      aiHubDescription="$AI_HUB_DESCRIPTION" \
      aiProjectName="$AI_PROJECT_NAME" \
      aiProjectFriendlyName="$AI_PROJECT_FRIENDLY_NAME" \
      aiProjectDescription="$AI_PROJECT_DESCRIPTION" \
      modelName="$MODEL_NAME" \
      modelFormat="OpenAI" \
      modelVersion="$MODEL_VERSION" \
      modelSkuName="$MODEL_SKU" \
      modelCapacity="$MODEL_CAPACITY" \
      modelLocation="$MODEL_LOCATION" \
      storageName="$STORAGE_NAME" \
      aiServicesName="$AI_SERVICES_NAME" \
      location="$RG_LOCATION" \
      tags='{"project": "AzureBeach", "owner": "Jose"}' \
  --output none

if [ $? -ne 0 ]; then
    echo "❌ Deployment failed."
    exit 1
fi

echo "✅ Deployment completed successfully!"

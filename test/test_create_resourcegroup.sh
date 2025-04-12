#!/bin/bash

# This script creates an Azure Resource Group and a Storage Account.

# Variables
RESOURCE_GROUP="Test"
LOCATION="eastus2"
STORAGE_ACCOUNT_NAME="storage$RANDOM$RANDOM" # Genera un nombre único para la cuenta de almacenamiento

# Crear el grupo de recursos
echo "Creando el grupo de recursos '$RESOURCE_GROUP' en la ubicación '$LOCATION'..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

# Crear la cuenta de almacenamiento
echo "Creando la cuenta de almacenamiento '$STORAGE_ACCOUNT_NAME' en el grupo de recursos '$RESOURCE_GROUP'..."
az storage account create --name "$STORAGE_ACCOUNT_NAME" --resource-group "$RESOURCE_GROUP" --location "$LOCATION" --sku Standard_LRS

echo "✅ Grupo de recursos y cuenta de almacenamiento creados exitosamente."
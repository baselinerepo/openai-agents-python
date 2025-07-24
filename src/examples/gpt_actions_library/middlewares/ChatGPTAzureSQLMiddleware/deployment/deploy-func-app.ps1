#-------------------------------------------------------------------------------------
# Go into the directory where the file exists
# cd:/deployment
# az login # enter login credentials
# RUN ./deploy-func-app.ps1

# the following powershell script create a azure function resources using the azure cli commands
# 1. Resource Group
# 2. Storage account
# 3. Function App
# 4. App service plan (Consumption plan)
# Application insights (and an Action Group and Smart Detector Alert Rule used with Application Insights)

# Configuration keys
# Resource Name and Location
$ResourceGroupName = 'vstiara_openai_rg'
$StorageAccountName = 'vstiara_funcapp_sa'
$FunctionAppName = 'ChatGPTAzureSQLMiddleware'
$Location = 'eastasia' # to see the list of all locations use: az account list-locations

# Create resource group
az group create --name $ResourceGroupName --location $Location

# Create general-purpose storage account
az storage account create --name $StorageAccountName --location $Location --resource-group $ResourceGroupName --sku Standard_LRS

# Create function app
az functionapp create --name $FunctionAppName --resource-group $ResourceGroupName --consumption-plan-location $Location --runtime python --runtime-version 3.12 --functions-version 4 --os-type linux --storage-account $StorageAccountName

# To delete the resource group and all resources in it
# az group delete --name $ResourceGroupName
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource group
resource "azurerm_resource_group" "rg" {
  name     = "email-logic-app-rg"
  location = "West Europe"
}

# Logic App (Consumption)
resource "azurerm_logic_app_workflow" "email_logic_app" {
  name                = "email-notification-logic-app"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# HTTP Request Trigger
resource "azurerm_logic_app_trigger_http_request" "email_trigger" {
  name         = "http-request-trigger"
  logic_app_id = azurerm_logic_app_workflow.email_logic_app.id

  schema = <<SCHEMA
{
  "type": "object",
  "properties": {
    "to": {
      "type": "string"
    },
    "subject": {
      "type": "string"
    },
    "body": {
      "type": "string"
    }
  },
  "required": ["to", "subject", "body"]
}
SCHEMA
}

# Office 365 API Connection
resource "azurerm_api_connection" "office365" {
  name                = "office365-connection"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  
  api_management_name = "Office365"
  display_name        = "Office 365 Outlook"
  
  # The connection requires authentication
  lifecycle {
    ignore_changes = [
      # Ignore changes to the connection because authentication will be configured separately
      api_management_name,
    ]
  }
}

# Email Action using Office 365
resource "azurerm_logic_app_action_custom" "send_email" {
  name         = "send-email-action"
  logic_app_id = azurerm_logic_app_workflow.email_logic_app.id
  
  body = <<BODY
{
  "inputs": {
    "host": {
      "connection": {
        "name": "@parameters('$connections')['office365']['connectionId']"
      }
    },
    "method": "post",
    "path": "/v2/Mail",
    "body": {
      "To": "@triggerBody()?['to']",
      "Subject": "@triggerBody()?['subject']",
      "Body": "<p>@{triggerBody()?['body']}</p>"
    }
  },
  "type": "ApiConnection",
  "runAfter": {}
}
BODY

  depends_on = [
    azurerm_logic_app_trigger_http_request.email_trigger,
    azurerm_api_connection.office365
  ]
}

# Output the Logic App HTTP endpoint URL
output "logic_app_trigger_url" {
  value       = azurerm_logic_app_trigger_http_request.email_trigger.callback_url
  description = "HTTP URL to trigger the Logic App"
  sensitive   = true
}
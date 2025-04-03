# my_flows = [
#     {"properties": {
#                 "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
#                 "displayName": "Brown Knows Good",
#                 "definition": {
#                 "metadata": {
#                     "workflowEntityId": "None",
#                     "processAdvisorMetadata": "None",
#                     "flowChargedByPaygo": "None",
#                     "flowclientsuspensionreason": "None",
#                     "flowclientsuspensiontime": "None",
#                     "flowclientsuspensionreasondetails": "None",
#                     "creator": {
#                     "id": "67c7ec85-5ebf-41db-85f2-238260635b73",
#                     "type": "User",
#                     "tenantId": "7e1c5bc5-e201-4917-8255-619176a3e046"
#                     },
#                     "provisioningMethod": "FromDefinition",
#                     "failureAlertSubscription": True,
#                     "clientLastModifiedTime": "2025-03-17T23:32:30.8957956Z",
#                     "connectionKeySavedTimeKey": "2025-03-17T23:32:30.8957956Z",
#                     "creationSource": "Portal",
#                     "modifiedSources": "Portal"
#                 },
#                 "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
#                 "contentVersion": "undefined",
#                 "parameters": {
#                     "$authentication": {
#                     "defaultValue": {},
#                     "type": "SecureObject"
#                     },
#                     "$connections": {
#                     "defaultValue": {},
#                     "type": "Object"
#                     }
#                 },
#                 "triggers": {
#                     "manual": {
#                     "type": "Request",
#                     "kind": "Button",
#                     "inputs": {
#                         "schema": {
#                         "type": "object",
#                         "properties": {
#                             "text": {
#                             "description": "Please enter your input",
#                             "title": "Question",
#                             "type": "string",
#                             "x-ms-content-hint": "TEXT",
#                             "x-ms-dynamically-added": True
#                             }
#                         },
#                         "required": [
#                             "text"
#                         ]
#                         }
#                     }
#                     }
#                 },
#                 "actions": {
#                     "HTTP_-_Keyword_Extractor": {
#                     "runAfter": {
#                         "Initialize_variable": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Http",
#                     "inputs": {
#                         "uri": "https://email-reading-tools.onrender.com/extract_keywords",
#                         "method": "POST",
#                         "headers": {
#                         "accept": "application/json"
#                         },
#                         "queries": {
#                         "text": "@{triggerBody()?['text']}"
#                         }
#                     },
#                     "runtimeConfiguration": {
#                         "contentTransfer": {
#                         "transferMode": "Chunked"
#                         }
#                     }
#                     },
#                     "HTTP_-_Analyze_Emails": {
#                     "runAfter": {
#                         "Compose": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Http",
#                     "inputs": {
#                         "uri": "https://email-reading-tools.onrender.com/analyze_emails",
#                         "method": "POST",
#                         "headers": {
#                         "accept": "application/json"
#                         },
#                         "queries": {
#                         "question": "@{triggerBody()?['text']}"
#                         },
#                         "body": {
#                         "emails": "@variables('Emails')"
#                         }
#                     },
#                     "runtimeConfiguration": {
#                         "contentTransfer": {
#                         "transferMode": "Chunked"
#                         }
#                     }
#                     },
#                     "Initialize_variable": {
#                     "runAfter": {},
#                     "type": "InitializeVariable",
#                     "inputs": {
#                         "variables": [
#                         {
#                             "name": "Emails",
#                             "type": "array",
#                             "value": []
#                         }
#                         ]
#                     }
#                     },
#                     "For_each": {
#                     "foreach": "@outputs('Get_emails_(V3)')?['body/value']",
#                     "actions": {
#                         "Html_to_text": {
#                         "type": "OpenApiConnection",
#                         "inputs": {
#                             "parameters": {
#                             "Content": "<p class=\"editor-paragraph\">@{items('For_each')?['body']}</p>"
#                             },
#                             "host": {
#                             "apiId": "/providers/Microsoft.PowerApps/apis/shared_conversionservice",
#                             "connectionName": "shared_conversionservice",
#                             "operationId": "HtmlToText"
#                             },
#                             "authentication": {
#                             "value": "@json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$ConnectionKey']",
#                             "type": "Raw"
#                             }
#                         }
#                         },
#                         "Condition": {
#                         "actions": {
#                             "Append_to_array_variable": {
#                             "type": "AppendToArrayVariable",
#                             "inputs": {
#                                 "name": "Emails",
#                                 "value": {
#                                 "body": "@body('Html_to_text')"
#                                 }
#                             }
#                             }
#                         },
#                         "runAfter": {
#                             "Html_to_text": [
#                             "Succeeded"
#                             ]
#                         },
#                         "else": {
#                             "actions": {}
#                         },
#                         "expression": {
#                             "and": [
#                             {
#                                 "contains": [
#                                 "@item()?['from']",
#                                 "4th-ir.com"
#                                 ]
#                             }
#                             ]
#                         },
#                         "type": "If"
#                         }
#                     },
#                     "runAfter": {
#                         "Get_emails_(V3)": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Foreach"
#                     },
#                     "Parse_JSON": {
#                     "runAfter": {
#                         "HTTP_-_Keyword_Extractor": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "ParseJson",
#                     "inputs": {
#                         "content": "@body('HTTP_-_Keyword_Extractor')",
#                         "schema": {
#                         "type": "object",
#                         "properties": {
#                             "keywords": {
#                             "type": "array",
#                             "items": {
#                                 "type": "string"
#                             }
#                             }
#                         }
#                         }
#                     }
#                     },
#                     "Get_emails_(V3)": {
#                     "runAfter": {
#                         "Parse_JSON": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "OpenApiConnection",
#                     "inputs": {
#                         "parameters": {
#                         "importance": "Any",
#                         "folderPath": "Inbox",
#                         "fetchOnlyUnread": False,
#                         "includeAttachments": True,
#                         "searchQuery": "@first(body('Parse_JSON')?['keywords'])",
#                         "top": 3
#                         },
#                         "host": {
#                         "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
#                         "connectionName": "shared_office365",
#                         "operationId": "GetEmailsV3"
#                         },
#                         "authentication": {
#                         "value": "@json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$ConnectionKey']",
#                         "type": "Raw"
#                         }
#                     }
#                     },
#                     "Compose": {
#                     "runAfter": {
#                         "For_each": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Compose",
#                     "inputs": "@variables('Emails')"
#                     }
#                 }
#                 },
#                 "connectionReferences": {
#                 "shared_conversionservice": {
#                     "connectionName": "shared-conversionser-b258989e-a71f-450e-b185-3dbe970a573f",
#                     "source": "Invoker",
#                     "id": "/providers/Microsoft.PowerApps/apis/shared_conversionservice",
#                     "tier": "NotSpecified",
#                     "apiName": "conversionservice"
#                 },
#                 "shared_office365": {
#                     "connectionName": "7ff22b98148442d2a1ce36794c0027bd",
#                     "source": "Invoker",
#                     "id": "/providers/Microsoft.PowerApps/apis/shared_office365",
#                     "tier": "NotSpecified",
#                     "apiName": "office365"
#                 }
#                 },
#                 "flowFailureAlertSubscribed": False,
#                 "isManaged": False
#             }},
#     {"properties": {
#                 "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
#                 "displayName": "Brown Knows Better",
#                 "definition": {
#                 "metadata": {
#                     "workflowEntityId": "None",
#                     "processAdvisorMetadata": "None",
#                     "flowChargedByPaygo": "None",
#                     "flowclientsuspensionreason": "None",
#                     "flowclientsuspensiontime": "None",
#                     "flowclientsuspensionreasondetails": "None",
#                     "creator": {
#                     "id": "67c7ec85-5ebf-41db-85f2-238260635b73",
#                     "type": "User",
#                     "tenantId": "7e1c5bc5-e201-4917-8255-619176a3e046"
#                     },
#                     "provisioningMethod": "FromDefinition",
#                     "failureAlertSubscription": True,
#                     "clientLastModifiedTime": "2025-03-17T23:32:30.8957956Z",
#                     "connectionKeySavedTimeKey": "2025-03-17T23:32:30.8957956Z",
#                     "creationSource": "Portal",
#                     "modifiedSources": "Portal"
#                 },
#                 "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
#                 "contentVersion": "undefined",
#                 "parameters": {
#                     "$authentication": {
#                     "defaultValue": {},
#                     "type": "SecureObject"
#                     },
#                     "$connections": {
#                     "defaultValue": {},
#                     "type": "Object"
#                     }
#                 },
#                 "triggers": {
#                     "manual": {
#                     "type": "Request",
#                     "kind": "Button",
#                     "inputs": {
#                         "schema": {
#                         "type": "object",
#                         "properties": {
#                             "text": {
#                             "description": "Please enter your input",
#                             "title": "Question",
#                             "type": "string",
#                             "x-ms-content-hint": "TEXT",
#                             "x-ms-dynamically-added": True
#                             }
#                         },
#                         "required": [
#                             "text"
#                         ]
#                         }
#                     }
#                     }
#                 },
#                 "actions": {
#                     "HTTP_-_Keyword_Extractor": {
#                     "runAfter": {
#                         "Initialize_variable": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Http",
#                     "inputs": {
#                         "uri": "https://email-reading-tools.onrender.com/extract_keywords",
#                         "method": "POST",
#                         "headers": {
#                         "accept": "application/json"
#                         },
#                         "queries": {
#                         "text": "@{triggerBody()?['text']}"
#                         }
#                     },
#                     "runtimeConfiguration": {
#                         "contentTransfer": {
#                         "transferMode": "Chunked"
#                         }
#                     }
#                     },
#                     "HTTP_-_Analyze_Emails": {
#                     "runAfter": {
#                         "Compose": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Http",
#                     "inputs": {
#                         "uri": "https://email-reading-tools.onrender.com/analyze_emails",
#                         "method": "POST",
#                         "headers": {
#                         "accept": "application/json"
#                         },
#                         "queries": {
#                         "question": "@{triggerBody()?['text']}"
#                         },
#                         "body": {
#                         "emails": "@variables('Emails')"
#                         }
#                     },
#                     "runtimeConfiguration": {
#                         "contentTransfer": {
#                         "transferMode": "Chunked"
#                         }
#                     }
#                     },
#                     "Initialize_variable": {
#                     "runAfter": {},
#                     "type": "InitializeVariable",
#                     "inputs": {
#                         "variables": [
#                         {
#                             "name": "Emails",
#                             "type": "array",
#                             "value": []
#                         }
#                         ]
#                     }
#                     },
#                     "For_each": {
#                     "foreach": "@outputs('Get_emails_(V3)')?['body/value']",
#                     "actions": {
#                         "Html_to_text": {
#                         "type": "OpenApiConnection",
#                         "inputs": {
#                             "parameters": {
#                             "Content": "<p class=\"editor-paragraph\">@{items('For_each')?['body']}</p>"
#                             },
#                             "host": {
#                             "apiId": "/providers/Microsoft.PowerApps/apis/shared_conversionservice",
#                             "connectionName": "shared_conversionservice",
#                             "operationId": "HtmlToText"
#                             },
#                             "authentication": {
#                             "value": "@json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$ConnectionKey']",
#                             "type": "Raw"
#                             }
#                         }
#                         },
#                         "Condition": {
#                         "actions": {
#                             "Append_to_array_variable": {
#                             "type": "AppendToArrayVariable",
#                             "inputs": {
#                                 "name": "Emails",
#                                 "value": {
#                                 "body": "@body('Html_to_text')"
#                                 }
#                             }
#                             }
#                         },
#                         "runAfter": {
#                             "Html_to_text": [
#                             "Succeeded"
#                             ]
#                         },
#                         "else": {
#                             "actions": {}
#                         },
#                         "expression": {
#                             "and": [
#                             {
#                                 "contains": [
#                                 "@item()?['from']",
#                                 "4th-ir.com"
#                                 ]
#                             }
#                             ]
#                         },
#                         "type": "If"
#                         }
#                     },
#                     "runAfter": {
#                         "Get_emails_(V3)": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Foreach"
#                     },
#                     "Parse_JSON": {
#                     "runAfter": {
#                         "HTTP_-_Keyword_Extractor": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "ParseJson",
#                     "inputs": {
#                         "content": "@body('HTTP_-_Keyword_Extractor')",
#                         "schema": {
#                         "type": "object",
#                         "properties": {
#                             "keywords": {
#                             "type": "array",
#                             "items": {
#                                 "type": "string"
#                             }
#                             }
#                         }
#                         }
#                     }
#                     },
#                     "Get_emails_(V3)": {
#                     "runAfter": {
#                         "Parse_JSON": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "OpenApiConnection",
#                     "inputs": {
#                         "parameters": {
#                         "importance": "Any",
#                         "folderPath": "Inbox",
#                         "fetchOnlyUnread": False,
#                         "includeAttachments": True,
#                         "searchQuery": "@first(body('Parse_JSON')?['keywords'])",
#                         "top": 3
#                         },
#                         "host": {
#                         "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
#                         "connectionName": "shared_office365",
#                         "operationId": "GetEmailsV3"
#                         },
#                         "authentication": {
#                         "value": "@json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$ConnectionKey']",
#                         "type": "Raw"
#                         }
#                     }
#                     },
#                     "Compose": {
#                     "runAfter": {
#                         "For_each": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Compose",
#                     "inputs": "@variables('Emails')"
#                     }
#                 }
#                 },
#                 "connectionReferences": {
#                 "shared_conversionservice": {
#                     "connectionName": "shared-conversionser-b258989e-a71f-450e-b185-3dbe970a573f",
#                     "source": "Invoker",
#                     "id": "/providers/Microsoft.PowerApps/apis/shared_conversionservice",
#                     "tier": "NotSpecified",
#                     "apiName": "conversionservice"
#                 },
#                 "shared_office365": {
#                     "connectionName": "7ff22b98148442d2a1ce36794c0027bd",
#                     "source": "Invoker",
#                     "id": "/providers/Microsoft.PowerApps/apis/shared_office365",
#                     "tier": "NotSpecified",
#                     "apiName": "office365"
#                 }
#                 },
#                 "flowFailureAlertSubscribed": False,
#                 "isManaged": False
#             }},
#     {"properties": {
#                 "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
#                 "displayName": "Brown Knows Best",
#                 "definition": {
#                 "metadata": {
#                     "workflowEntityId": "None",
#                     "processAdvisorMetadata": "None",
#                     "flowChargedByPaygo": "None",
#                     "flowclientsuspensionreason": "None",
#                     "flowclientsuspensiontime": "None",
#                     "flowclientsuspensionreasondetails": "None",
#                     "creator": {
#                     "id": "67c7ec85-5ebf-41db-85f2-238260635b73",
#                     "type": "User",
#                     "tenantId": "7e1c5bc5-e201-4917-8255-619176a3e046"
#                     },
#                     "provisioningMethod": "FromDefinition",
#                     "failureAlertSubscription": True,
#                     "clientLastModifiedTime": "2025-03-17T23:32:30.8957956Z",
#                     "connectionKeySavedTimeKey": "2025-03-17T23:32:30.8957956Z",
#                     "creationSource": "Portal",
#                     "modifiedSources": "Portal"
#                 },
#                 "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
#                 "contentVersion": "undefined",
#                 "parameters": {
#                     "$authentication": {
#                     "defaultValue": {},
#                     "type": "SecureObject"
#                     },
#                     "$connections": {
#                     "defaultValue": {},
#                     "type": "Object"
#                     }
#                 },
#                 "triggers": {
#                     "manual": {
#                     "type": "Request",
#                     "kind": "Button",
#                     "inputs": {
#                         "schema": {
#                         "type": "object",
#                         "properties": {
#                             "text": {
#                             "description": "Please enter your input",
#                             "title": "Question",
#                             "type": "string",
#                             "x-ms-content-hint": "TEXT",
#                             "x-ms-dynamically-added": True
#                             }
#                         },
#                         "required": [
#                             "text"
#                         ]
#                         }
#                     }
#                     }
#                 },
#                 "actions": {
#                     "HTTP_-_Keyword_Extractor": {
#                     "runAfter": {
#                         "Initialize_variable": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Http",
#                     "inputs": {
#                         "uri": "https://email-reading-tools.onrender.com/extract_keywords",
#                         "method": "POST",
#                         "headers": {
#                         "accept": "application/json"
#                         },
#                         "queries": {
#                         "text": "@{triggerBody()?['text']}"
#                         }
#                     },
#                     "runtimeConfiguration": {
#                         "contentTransfer": {
#                         "transferMode": "Chunked"
#                         }
#                     }
#                     },
#                     "HTTP_-_Analyze_Emails": {
#                     "runAfter": {
#                         "Compose": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Http",
#                     "inputs": {
#                         "uri": "https://email-reading-tools.onrender.com/analyze_emails",
#                         "method": "POST",
#                         "headers": {
#                         "accept": "application/json"
#                         },
#                         "queries": {
#                         "question": "@{triggerBody()?['text']}"
#                         },
#                         "body": {
#                         "emails": "@variables('Emails')"
#                         }
#                     },
#                     "runtimeConfiguration": {
#                         "contentTransfer": {
#                         "transferMode": "Chunked"
#                         }
#                     }
#                     },
#                     "Initialize_variable": {
#                     "runAfter": {},
#                     "type": "InitializeVariable",
#                     "inputs": {
#                         "variables": [
#                         {
#                             "name": "Emails",
#                             "type": "array",
#                             "value": []
#                         }
#                         ]
#                     }
#                     },
#                     "For_each": {
#                     "foreach": "@outputs('Get_emails_(V3)')?['body/value']",
#                     "actions": {
#                         "Html_to_text": {
#                         "type": "OpenApiConnection",
#                         "inputs": {
#                             "parameters": {
#                             "Content": "<p class=\"editor-paragraph\">@{items('For_each')?['body']}</p>"
#                             },
#                             "host": {
#                             "apiId": "/providers/Microsoft.PowerApps/apis/shared_conversionservice",
#                             "connectionName": "shared_conversionservice",
#                             "operationId": "HtmlToText"
#                             },
#                             "authentication": {
#                             "value": "@json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$ConnectionKey']",
#                             "type": "Raw"
#                             }
#                         }
#                         },
#                         "Condition": {
#                         "actions": {
#                             "Append_to_array_variable": {
#                             "type": "AppendToArrayVariable",
#                             "inputs": {
#                                 "name": "Emails",
#                                 "value": {
#                                 "body": "@body('Html_to_text')"
#                                 }
#                             }
#                             }
#                         },
#                         "runAfter": {
#                             "Html_to_text": [
#                             "Succeeded"
#                             ]
#                         },
#                         "else": {
#                             "actions": {}
#                         },
#                         "expression": {
#                             "and": [
#                             {
#                                 "contains": [
#                                 "@item()?['from']",
#                                 "4th-ir.com"
#                                 ]
#                             }
#                             ]
#                         },
#                         "type": "If"
#                         }
#                     },
#                     "runAfter": {
#                         "Get_emails_(V3)": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Foreach"
#                     },
#                     "Parse_JSON": {
#                     "runAfter": {
#                         "HTTP_-_Keyword_Extractor": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "ParseJson",
#                     "inputs": {
#                         "content": "@body('HTTP_-_Keyword_Extractor')",
#                         "schema": {
#                         "type": "object",
#                         "properties": {
#                             "keywords": {
#                             "type": "array",
#                             "items": {
#                                 "type": "string"
#                             }
#                             }
#                         }
#                         }
#                     }
#                     },
#                     "Get_emails_(V3)": {
#                     "runAfter": {
#                         "Parse_JSON": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "OpenApiConnection",
#                     "inputs": {
#                         "parameters": {
#                         "importance": "Any",
#                         "folderPath": "Inbox",
#                         "fetchOnlyUnread": False,
#                         "includeAttachments": True,
#                         "searchQuery": "@first(body('Parse_JSON')?['keywords'])",
#                         "top": 3
#                         },
#                         "host": {
#                         "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
#                         "connectionName": "shared_office365",
#                         "operationId": "GetEmailsV3"
#                         },
#                         "authentication": {
#                         "value": "@json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$ConnectionKey']",
#                         "type": "Raw"
#                         }
#                     }
#                     },
#                     "Compose": {
#                     "runAfter": {
#                         "For_each": [
#                         "Succeeded"
#                         ]
#                     },
#                     "type": "Compose",
#                     "inputs": "@variables('Emails')"
#                     }
#                 }
#                 },
#                 "connectionReferences": {
#                 "shared_conversionservice": {
#                     "connectionName": "shared-conversionser-b258989e-a71f-450e-b185-3dbe970a573f",
#                     "source": "Invoker",
#                     "id": "/providers/Microsoft.PowerApps/apis/shared_conversionservice",
#                     "tier": "NotSpecified",
#                     "apiName": "conversionservice"
#                 },
#                 "shared_office365": {
#                     "connectionName": "7ff22b98148442d2a1ce36794c0027bd",
#                     "source": "Invoker",
#                     "id": "/providers/Microsoft.PowerApps/apis/shared_office365",
#                     "tier": "NotSpecified",
#                     "apiName": "office365"
#                 }
#                 },
#                 "flowFailureAlertSubscribed": False,
#                 "isManaged": False
#             }},
#     {"properties": {
#     "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
#     "displayName": "Brown Knows All",
#     "definition": {
#       "metadata": {
#         "workflowEntityId": "None",
#         "processAdvisorMetadata": "None",
#         "flowChargedByPaygo": "None",
#         "flowclientsuspensionreason": "None",
#         "flowclientsuspensiontime": "None",
#         "flowclientsuspensionreasondetails": "None",
#         "creator": {
#           "id": "67c7ec85-5ebf-41db-85f2-238260635b73",
#           "type": "User",
#           "tenantId": "7e1c5bc5-e201-4917-8255-619176a3e046"
#         },
#         "provisioningMethod": "FromDefinition",
#         "failureAlertSubscription": True,
#         "clientLastModifiedTime": "2025-03-19T23:21:00.124647Z",
#         "connectionKeySavedTimeKey": "2025-03-19T23:21:00.124647Z",
#         "creationSource": "Portal"
#       },
#       "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
#       "contentVersion": "1.0.0.0",
#       "parameters": {
#         "$authentication": {
#           "defaultValue": {},
#           "type": "SecureObject"
#         },
#         "$connections": {
#           "defaultValue": {},
#           "type": "Object"
#         }
#       },
#       "triggers": {
#         "manual": {
#           "metadata": {
#             "operationMetadataId": "d1bb1163-b416-4d62-9b2d-2dabd29719a9"
#           },
#           "type": "Request",
#           "kind": "Http",
#           "inputs": {
#             "schema": {
#               "type": "object",
#               "properties": {
#                 "Email Address": {
#                   "type": "string"
#                 },
#                 "Subject": {
#                   "type": "string"
#                 },
#                 "Message": {
#                   "type": "string"
#                 }
#               }
#             },
#             "method": "POST",
#             "triggerAuthenticationType": "All"
#           }
#         }
#       },
#       "actions": {
#         "Send_an_email_(V2)": {
#           "runAfter": {},
#           "metadata": {
#             "operationMetadataId": "57978e6b-8826-4a56-a6d4-fdda40404e51"
#           },
#           "type": "OpenApiConnection",
#           "inputs": {
#             "parameters": {
#               "emailMessage/To": "@triggerBody()?['Email Address']",
#               "emailMessage/Subject": "@triggerBody()?['Subject']",
#               "emailMessage/Body": "<p class=\"editor-paragraph\">@{triggerBody()?['Message']}</p>",
#               "emailMessage/Importance": "Normal"
#             },
#             "host": {
#               "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
#               "connectionName": "shared_office365-1",
#               "operationId": "SendEmailV2"
#             },
#             "authentication": "@parameters('$authentication')"
#           }
#         },
#         "Response": {
#           "runAfter": {
#             "Send_an_email_(V2)": [
#               "Succeeded"
#             ]
#           },
#           "metadata": {
#             "operationMetadataId": "2e116e58-cccf-49c8-bea0-eb1050e202d5"
#           },
#           "type": "Response",
#           "kind": "Http",
#           "inputs": {
#             "statusCode": 200,
#             "body": "Message Sent Successfuly"
#           }
#         }
#       },
#       "outputs": {}
#     },
#     "connectionReferences": {
#       "shared_office365-1": {
#                     "connectionName": "7ff22b98148442d2a1ce36794c0027bd",
#                     "source": "Invoker",
#                     "id": "/providers/Microsoft.PowerApps/apis/shared_office365",
#                     "tier": "NotSpecified",
#                     "apiName": "office365"
#                 }
#     },
#     "flowFailureAlertSubscribed": False,
#     "isManaged": False
#   }}
# ]


quest_flows = [
    {
        "properties": {
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
            "displayName": "Brown Knows All",
            "definition": {
                "metadata": {
                    "workflowEntityId": "None",
                    "processAdvisorMetadata": "None",
                    "flowChargedByPaygo": "None",
                    "flowclientsuspensionreason": "None",
                    "flowclientsuspensiontime": "None",
                    "flowclientsuspensionreasondetails": "None",
                    "creator": {
                        "id": "67c7ec85-5ebf-41db-85f2-238260635b73",
                        "type": "User",
                        "tenantId": "7e1c5bc5-e201-4917-8255-619176a3e046",
                    },
                    "provisioningMethod": "FromDefinition",
                    "failureAlertSubscription": True,
                    "clientLastModifiedTime": "2025-03-19T23:21:00.124647Z",
                    "connectionKeySavedTimeKey": "2025-03-19T23:21:00.124647Z",
                    "creationSource": "Portal",
                },
                "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
                "contentVersion": "1.0.0.0",
                "parameters": {
                    "$authentication": {"defaultValue": {}, "type": "SecureObject"},
                    "$connections": {"defaultValue": {}, "type": "Object"},
                },
                "triggers": {
                    "manual": {
                        "metadata": {
                            "operationMetadataId": "d1bb1163-b416-4d62-9b2d-2dabd29719a9"
                        },
                        "type": "Request",
                        "kind": "Http",
                        "inputs": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "Email Address": {"type": "string"},
                                    "Subject": {"type": "string"},
                                    "Message": {"type": "string"},
                                },
                            },
                            "method": "POST",
                            "triggerAuthenticationType": "All",
                        },
                    }
                },
                "actions": {
                    "Send_an_email_(V2)": {
                        "runAfter": {},
                        "metadata": {
                            "operationMetadataId": "57978e6b-8826-4a56-a6d4-fdda40404e51"
                        },
                        "type": "OpenApiConnection",
                        "inputs": {
                            "parameters": {
                                "emailMessage/To": "@triggerBody()?['Email Address']",
                                "emailMessage/Subject": "@triggerBody()?['Subject']",
                                "emailMessage/Body": "<p class=\"editor-paragraph\">@{triggerBody()?['Message']}</p>",
                                "emailMessage/Importance": "Normal",
                            },
                            "host": {
                                "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365",
                                "connectionName": "shared_office365-1",
                                "operationId": "SendEmailV2",
                            },
                            "authentication": "@parameters('$authentication')",
                        },
                    },
                    "Response": {
                        "runAfter": {"Send_an_email_(V2)": ["Succeeded"]},
                        "metadata": {
                            "operationMetadataId": "2e116e58-cccf-49c8-bea0-eb1050e202d5"
                        },
                        "type": "Response",
                        "kind": "Http",
                        "inputs": {
                            "statusCode": 200,
                            "body": "Message Sent Successfuly",
                        },
                    },
                },
                "outputs": {},
            },
            "connectionReferences": {
                "shared_office365-1": {
                    "connectionName": "7ff22b98148442d2a1ce36794c0027bd",
                    "source": "Invoker",
                    "id": "/providers/Microsoft.PowerApps/apis/shared_office365",
                    "tier": "NotSpecified",
                    "apiName": "office365",
                }
            },
            "flowFailureAlertSubscribed": False,
            "isManaged": False,
        }
    }
]


url_collection_flow_template = [
    {
        "properties": {
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
            "displayName": "Http -> List Callback URL,Response,Compose,Compose-copy",
            "definition": {
                "metadata": {
                    "workflowEntityId": "None",
                    "processAdvisorMetadata": "None",
                    "flowChargedByPaygo": "None",
                    "flowclientsuspensionreason": "None",
                    "flowclientsuspensiontime": "None",
                    "flowclientsuspensionreasondetails": "None",
                    "creator": {
                        "id": "67c7ec85-5ebf-41db-85f2-238260635b73",
                        "type": "User",
                        "tenantId": "7e1c5bc5-e201-4917-8255-619176a3e046",
                    },
                    "provisioningMethod": "FromDefinition",
                    "failureAlertSubscription": True,
                    "clientLastModifiedTime": "2025-04-01T22:46:57.3908287Z",
                    "connectionKeySavedTimeKey": "2025-04-01T22:46:57.3908287Z",
                    "creationSource": "Portal",
                    "modifiedSources": "Portal",
                },
                "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
                "contentVersion": "1.0.0.0",
                "parameters": {
                    "$authentication": {"defaultValue": {}, "type": "SecureObject"},
                    "$connections": {"defaultValue": {}, "type": "Object"},
                },
                "triggers": {
                    "Recurrence": {
                        "recurrence": {
                            "interval": 60,
                            "frequency": "Second",
                            "timeZone": "UTC",
                        },
                        "type": "Recurrence",
                    }
                },
                "actions": {
                    "List_Callback_URL": {
                        "runAfter": {},
                        "type": "OpenApiConnection",
                        "inputs": {
                            "parameters": {
                                "environmentName": "None",
                                "flowName": "None",
                            },
                            "host": {
                                "apiId": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
                                "connectionName": "shared_flowmanagement",
                                "operationId": "ListCallbackUrl",
                            },
                            "authentication": "@parameters('$authentication')",
                        },
                    },
                    "Compose": {
                        "runAfter": {"List_Callback_URL": ["Succeeded"]},
                        "type": "Compose",
                        "inputs": "@outputs('List_Callback_URL')?['body/response/value']",
                    },
                    "Compose-copy": {
                        "runAfter": {"Compose": ["Succeeded"]},
                        "type": "Compose",
                        "inputs": "@body('List_Callback_URL')",
                    },
                },
                "outputs": {},
            },
            "connectionReferences": {
                "shared_flowmanagement": {
                    "connectionName": "shared-flowmanagemen-eeadf6eb-1c04-410b-9391-cc66b5807873",
                    "source": "Embedded",
                    "id": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
                    "tier": "NotSpecified",
                    "apiName": "flowmanagement",
                }
            },
            "flowFailureAlertSubscribed": False,
            "isManaged": False,
        }
    }
]

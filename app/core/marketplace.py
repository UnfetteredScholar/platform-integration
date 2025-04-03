print("Quest AI Marketplace Flows Loaded")
quest_flows = [
    {
        "properties": {
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
            "displayName": "Send Work Email",
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
                    "clientLastModifiedTime": "2025-04-02T18:18:25.0069011Z",
                    "connectionKeySavedTimeKey": "2025-04-02T18:18:25.0069011Z",
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
                    "manual": {
                        "metadata": {},
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
                                "connectionName": "shared_office365",
                                "operationId": "SendEmailV2",
                            },
                            "authentication": "@parameters('$authentication')",
                        },
                    },
                    "Response": {
                        "runAfter": {"Send_an_email_(V2)": ["Succeeded"]},
                        "type": "Response",
                        "kind": "Http",
                        "inputs": {
                            "statusCode": 200,
                            "body": "Email successfully sent to @{triggerBody()?['Email Address']}",
                        },
                    },
                },
                "outputs": {},
            },
            "connectionReferences": {
                "shared_office365": {
                    "connectionName": "None",
                    "source": "Embedded",
                    "id": "/providers/Microsoft.PowerApps/apis/shared_office365",
                    "tier": "NotSpecified",
                    "apiName": "office365",
                }
            },
            "flowFailureAlertSubscribed": False,
            "isManaged": False,
        }
    },
    {
        "properties": {
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
            "displayName": "Get Work Email",
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
                    "clientLastModifiedTime": "2025-04-02T18:38:58.8383756Z",
                    "connectionKeySavedTimeKey": "2025-04-02T18:38:58.8383756Z",
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
                    "manual": {
                        "metadata": {},
                        "type": "Request",
                        "kind": "Http",
                        "inputs": {
                            "schema": {
                                "type": "object",
                                "properties": {"name": {"type": "string"}},
                            },
                            "method": "POST",
                            "triggerAuthenticationType": "All",
                        },
                    }
                },
                "actions": {
                    "Search_for_users_(V2)": {
                        "runAfter": {},
                        "type": "OpenApiConnection",
                        "inputs": {
                            "parameters": {
                                "top": 3,
                                "isSearchTermRequired": True,
                                "searchTerm": "@triggerBody()?['name']",
                            },
                            "host": {
                                "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365users",
                                "connectionName": "shared_office365users",
                                "operationId": "SearchUserV2",
                            },
                            "authentication": "@parameters('$authentication')",
                        },
                    },
                    "For_each": {
                        "foreach": "@outputs('Search_for_users_(V2)')?['body/value']",
                        "actions": {
                            "Append_to_array_variable": {
                                "type": "AppendToArrayVariable",
                                "inputs": {
                                    "name": "Emails",
                                    "value": "@item()?['Mail']",
                                },
                            }
                        },
                        "runAfter": {"Initialize_variable": ["Succeeded"]},
                        "type": "Foreach",
                    },
                    "Initialize_variable": {
                        "runAfter": {"Search_for_users_(V2)": ["Succeeded"]},
                        "type": "InitializeVariable",
                        "inputs": {
                            "variables": [
                                {"name": "Emails", "type": "array", "value": []}
                            ]
                        },
                    },
                    "Response": {
                        "runAfter": {"For_each": ["Succeeded"]},
                        "type": "Response",
                        "kind": "Http",
                        "inputs": {"statusCode": 200, "body": "@variables('Emails')"},
                    },
                },
                "outputs": {},
            },
            "connectionReferences": {
                "shared_office365users": {
                    "connectionName": "shared-office365user-08b66d50-9459-4fc6-ad82-0e8cdf3c5227",
                    "source": "Embedded",
                    "id": "/providers/Microsoft.PowerApps/apis/shared_office365users",
                    "tier": "NotSpecified",
                    "apiName": "office365users",
                }
            },
            "flowFailureAlertSubscribed": False,
            "isManaged": False,
        }
    },
]

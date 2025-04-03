import copy

url_collection_flow_template = [
    {
        "properties": {
            "apiId": "/providers/Microsoft.PowerApps/apis/shared_logicflows",
            "displayName": "Send Flow URL",
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
                    "clientLastModifiedTime": "2025-04-03T05:55:01.1066754Z",
                    "connectionKeySavedTimeKey": "2025-04-03T05:55:01.1066754Z",
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
                                "environmentName": "Default-7e1c5bc5-e201-4917-8255-619176a3e046",
                                "flowName": "5cc25a6f-830a-42ac-a5fb-49a43ea99a4f",
                            },
                            "host": {
                                "apiId": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
                                "connectionName": "shared_flowmanagement",
                                "operationId": "ListCallbackUrl",
                            },
                            "authentication": "@parameters('$authentication')",
                        },
                    },
                    "HTTP": {
                        "runAfter": {"Get_my_profile_(V2)": ["Succeeded"]},
                        "type": "Http",
                        "inputs": {
                            "uri": "https://userflowservice.onrender.com/users/@{outputs('Get_my_profile_(V2)')?['body/mail']}/flows",
                            "method": "POST",
                            "body": {
                                "@outputs('Get_Flow')?['body/properties/displayName']": {
                                    "flow_id": "@outputs('Get_Flow')?['body/name']",
                                    "flow_url": "@outputs('List_Callback_URL')?['body/response/value']",
                                }
                            },
                        },
                        "runtimeConfiguration": {
                            "contentTransfer": {"transferMode": "Chunked"}
                        },
                    },
                    "Get_my_profile_(V2)": {
                        "runAfter": {"Get_Flow": ["Succeeded"]},
                        "type": "OpenApiConnection",
                        "inputs": {
                            "host": {
                                "apiId": "/providers/Microsoft.PowerApps/apis/shared_office365users",
                                "connectionName": "shared_office365users",
                                "operationId": "MyProfile_V2",
                            },
                            "authentication": "@parameters('$authentication')",
                        },
                    },
                    "Get_Flow": {
                        "runAfter": {"List_Callback_URL": ["Succeeded"]},
                        "type": "OpenApiConnection",
                        "inputs": {
                            "parameters": {
                                "environmentName": "Default-7e1c5bc5-e201-4917-8255-619176a3e046",
                                "flowName": "5cc25a6f-830a-42ac-a5fb-49a43ea99a4f",
                            },
                            "host": {
                                "apiId": "/providers/Microsoft.PowerApps/apis/shared_flowmanagement",
                                "connectionName": "shared_flowmanagement",
                                "operationId": "GetFlow",
                            },
                            "authentication": "@parameters('$authentication')",
                        },
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
                },
                "shared_office365users": {
                    "connectionName": "shared-office365user-54c8b4a0-8f6c-4f21-aac6-d777db81701a",
                    "source": "Embedded",
                    "id": "/providers/Microsoft.PowerApps/apis/shared_office365users",
                    "tier": "NotSpecified",
                    "apiName": "office365users",
                },
            },
            "flowFailureAlertSubscribed": False,
            "isManaged": False,
        }
    }
]


def update_flow_properties(environment_id, flow_name):
    """
    Updates the environmentName and flowName within a flow template structure
    and returns it in the specified format {"properties": updated_properties}.

    Args:
      flow_template_list (list): A list containing one dictionary,
                                 representing the flow template structure.
                                 Assumes the structure matches the provided example.
      environment_id (str): The new environment ID to set.
      flow_name (str): The new flow name to set.

    Returns:
      dict: A new dictionary in the format {"properties": updated_properties}
            containing the modified flow properties, or None if the input
            structure is invalid or keys are missing.
    """
    # Use deepcopy to avoid modifying the original template object
    try:
        template_copy = copy.deepcopy(url_collection_flow_template[0])
    except (TypeError, IndexError):
        print("Error: Could not copy input template structure.")
        return None

    # Navigate through the nested structure and update the values
    # Using .get() for safer access in case keys are missing
    try:
        properties_data = template_copy.get("properties")
        if properties_data is None:
            raise KeyError("'properties' key not found")

        # Update List_Callback_URL parameters
        list_callback_params = (
            properties_data.get("definition", {})
            .get("actions", {})
            .get("List_Callback_URL", {})
            .get("inputs", {})
            .get("parameters")
        )

        if list_callback_params is None:
            raise KeyError(
                "Nested path to List_Callback_URL parameters not found or incomplete"
            )

        list_callback_params["environmentName"] = environment_id
        list_callback_params["flowName"] = flow_name

        # Update Get_Flow parameters
        get_flow_params = (
            properties_data.get("definition", {})
            .get("actions", {})
            .get("Get_Flow", {})
            .get("inputs", {})
            .get("parameters")
        )

        if get_flow_params is None:
            raise KeyError("Nested path to Get_Flow parameters not found or incomplete")

        get_flow_params["environmentName"] = environment_id
        get_flow_params["flowName"] = flow_name

    except KeyError as e:
        print(f"Error: Missing key in template structure - {e}")
        return None
    except AttributeError as e:
        print(f"Error: Problem accessing attribute, structure might differ - {e}")
        return None

    # Construct the final output object in the desired format
    output_object = {"properties": properties_data}

    return output_object

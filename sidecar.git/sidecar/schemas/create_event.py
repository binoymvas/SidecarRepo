schema = {
    "type" : "object",
    "required": ["event"],
    "properties" : {
        "event": {
            "type": "object",
            "required": ["name", "node_uuid", "vm_uuid_list"],
            "properties": {
                "name": {
                    "type": "string",
                    "pattern": r"^[a-zA-Z0-9]([\w\s-]+[a-zA-Z0-9])$"
                },
                "node_uuid": {
                    "type": "string"
                },
                "vm_uuid_list": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "uniqueItems": True
                }
            }
        }
    }    
}

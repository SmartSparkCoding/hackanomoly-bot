def get_maintainer_dm_modal():
    return {
        "type": "modal",
        "callback_id": "maintainer_dm",
        "title": {
            "type": "plain_text",
            "text": ":hackanomoly-v1: dm",
            "emoji": True,
        },
        "blocks": [
            {
                "type": "input",
                "block_id": "recipient",
                "label": {
                    "type": "plain_text",
                    "text": "who",
                    "emoji": True,
                },
                "element": {
                    "type": "users_select",
                    "action_id": "recipient",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a user",
                    },
                },
            },
            {
                "type": "input",
                "block_id": "message",
                "label": {
                    "type": "plain_text",
                    "text": "message",
                    "emoji": True,
                },
                "element": {
                    "type": "rich_text_input",
                    "action_id": "message",
                },
            },
        ],
        "submit": {
            "type": "plain_text",
            "text": ":hackanomoly-v1: send",
            "emoji": True,
        },
    }
TOOL_SCHEMAS = {
    "none": {
        "label": "No tool",
        "description": "Evaluate the prompt without executing a local action.",
        "fields": [],
    },
    "write_note": {
        "label": "Write Note",
        "description": "Write a .txt note into artifacts/notes/",
        "fields": [
            {"name": "title", "label": "Title"},
            {"name": "content", "label": "Content"},
        ],
    },
    "save_json": {
        "label": "Save JSON",
        "description": "Write a .json file into artifacts/data/",
        "fields": [
            {"name": "filename", "label": "Filename"},
            {"name": "data", "label": "JSON Content"},
        ],
    },
    "create_folder": {
        "label": "Create Folder",
        "description": "Create a folder inside artifacts/workspaces/",
        "fields": [
            {"name": "name", "label": "Folder Name"},
        ],
    },
}


def get_tool_names() -> list[str]:
    return list(TOOL_SCHEMAS.keys())

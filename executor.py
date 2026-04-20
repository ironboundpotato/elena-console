import os
import json

BASE_DIR = os.path.join(os.getcwd(), "artifacts")


def ensure_dirs():
    os.makedirs(os.path.join(BASE_DIR, "notes"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
    os.makedirs(os.path.join(BASE_DIR, "workspaces"), exist_ok=True)


def execute_tool(tool_name, params, governance):
    ensure_dirs()

    decision = governance.get("decision", "UNKNOWN")

    if tool_name == "none":
        return {
            "status": "NO_ACTION",
            "tool": "none",
            "path": None,
            "message": "No tool selected. Governance evaluation only.",
        }

    if decision != "APPROVED":
        return {
            "status": "BLOCKED",
            "tool": tool_name,
            "path": None,
            "message": f"Execution blocked because governance decision was {decision}.",
        }

    try:
        if tool_name == "create_folder":
            folder_name = params.get("name", "default_folder")
            path = os.path.join(BASE_DIR, "workspaces", folder_name)
            os.makedirs(path, exist_ok=True)
            return {
                "status": "SUCCESS",
                "tool": tool_name,
                "path": path,
                "message": f"Folder created: {path}",
            }

        elif tool_name == "write_note":
            title = params.get("title", "note")
            content = params.get("content", "")
            file_path = os.path.join(BASE_DIR, "notes", f"{title}.txt")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

            return {
                "status": "SUCCESS",
                "tool": tool_name,
                "path": file_path,
                "message": f"Note saved: {file_path}",
            }

        elif tool_name == "save_json":
            filename = params.get("filename", "data.json")
            data = params.get("data", "{}")

            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    return {
                        "status": "ERROR",
                        "tool": tool_name,
                        "path": None,
                        "message": "Invalid JSON content.",
                    }

            file_path = os.path.join(BASE_DIR, "data", filename)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            return {
                "status": "SUCCESS",
                "tool": tool_name,
                "path": file_path,
                "message": f"JSON saved: {file_path}",
            }

        return {
            "status": "ERROR",
            "tool": tool_name,
            "path": None,
            "message": f"Unknown tool: {tool_name}",
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "tool": tool_name,
            "path": None,
            "message": f"Execution error: {str(e)}",
        }
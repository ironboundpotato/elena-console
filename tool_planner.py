def infer_tool_from_prompt(prompt: str) -> tuple[str, dict]:
    text = (prompt or "").strip().lower()

    if any(phrase in text for phrase in ["create a folder", "make a folder", "new folder"]):
        name = "project_workspace"
        trigger_phrases = ["called ", "named ", "for "]

        for phrase in trigger_phrases:
            if phrase in text:
                candidate = text.split(phrase, 1)[1].strip()
                candidate = candidate.replace(" ", "_")
                candidate = "".join(ch for ch in candidate if ch.isalnum() or ch in "_-")
                if candidate:
                    name = candidate[:80]
                    break

        return "create_folder", {"name": name}

    if any(phrase in text for phrase in ["write a note", "save a note", "create a note"]):
        return "write_note", {
            "title": "generated_note",
            "content": prompt,
        }

    if any(phrase in text for phrase in ["save json", "save this as json", "write json"]):
        return "save_json", {
            "filename": "generated_data.json",
            "data": '{"source": "prompt", "content": "placeholder"}',
        }

    return "none", {}
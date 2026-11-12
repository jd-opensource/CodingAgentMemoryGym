from __future__ import annotations

from unidiff import PatchSet

def _strip_path(value: str) -> str:
    if value == "/dev/null":
        return value
    if value.startswith("a/") or value.startswith("b/"):
        return value[2:]
    return value

def _line_value(value: str) -> str:
    return value[:-1] if value.endswith("\n") else value

def unified_to_codex_patch(unified: str, *, reverse: bool = False) -> str:

    parsed = PatchSet(unified)
    output = ["*** Begin Patch"]
    for file_patch in parsed:
        source = _strip_path(str(file_patch.source_file))
        target = _strip_path(str(file_patch.target_file))
        if reverse:
            source, target = target, source
        if source == "/dev/null":
            output.append(f"*** Add File: {target}")
            for hunk in file_patch:
                expected_type = "-" if reverse else "+"
                for line in hunk:
                    if line.line_type == expected_type:
                        output.append("+" + _line_value(line.value))
            continue
        if target == "/dev/null":
            output.append(f"*** Delete File: {source}")
            continue
        output.append(f"*** Update File: {source}")
        if source != target:
            output.append(f"*** Move to: {target}")
        for hunk in file_patch:
            section = str(hunk.section_header or "").strip()
            output.append(f"@@ {section}" if section else "@@")
            for line in hunk:
                if line.line_type in {" ", "+", "-"}:
                    line_type = line.line_type
                    if reverse and line_type in {"+", "-"}:
                        line_type = "+" if line_type == "-" else "-"
                    output.append(line_type + _line_value(line.value))
    output.append("*** End Patch")
    if len(output) <= 2:
        raise ValueError("unified patch produced no file operations")
    return "\n".join(output)

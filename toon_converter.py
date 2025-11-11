import json
import re

class ToonEncodeError(Exception):
    pass

class ToonDecodeError(Exception):
    pass

def _quote_string(s):
    return json.dumps(s)

def _is_simple_identifier(s):
    return re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', s) is not None

def _needs_quoting_string(s, delimiter=','):
    if s == "":
        return True
    if any(ch.isspace() for ch in s):
        return True
    if delimiter in s or ':' in s:
        return True
    if s in ("null", "true", "false"):
        return True
    if re.match(r'^-?\d+(\.\d+)?$', s):
        return True
    if '"' in s or "'" in s:
        return True
    return False

def encode(obj, *, indent_size=2, delimiter=',', length_marker=False):
    def _encode(value, indent_level):
        indent = ' ' * (indent_size * indent_level)
        if value is None:
            return indent + 'null'
        if isinstance(value, bool):
            return indent + ('true' if value else 'false')
        if isinstance(value, (int, float)):
            return indent + str(value)
        if isinstance(value, str):
            if _needs_quoting_string(value, delimiter):
                return indent + _quote_string(value)
            else:
                return indent + value
        if isinstance(value, dict):
            lines = []
            for k in sorted(value.keys()):
                v = value[k]
                key_repr = k if _is_simple_identifier(k) else _quote_string(k)
                if isinstance(v, (dict, list)):
                    lines.append(indent + f"{key_repr}:")
                    lines.append(_encode(v, indent_level+1))
                else:
                    val_line = _encode(v, 0).lstrip()
                    lines.append(indent + f"{key_repr}: {val_line}")
            return "\n".join(lines)
        if isinstance(value, list):
            n = len(value)
            if n>0 and all(isinstance(item, dict) for item in value):
                keys = sorted(value[0].keys())
                uniform = all(set(item.keys()) == set(keys) and all(not isinstance(item[k], (dict, list)) for k in keys) for item in value)
                if uniform:
                    lm = "#" if length_marker else ""
                    header = indent + f"[{lm}{n}]{{{','.join(keys)}}}:"
                    lines = [header]
                    for item in value:
                        row = delimiter.join(
                            (_quote_string(str(item[k])) if _needs_quoting_string(str(item[k]), delimiter) else str(item[k]))
                            for k in keys
                        )
                        lines.append(indent + ' ' * indent_size + row)
                    return "\n".join(lines)
            if all(not isinstance(item, (dict, list)) for item in value):
                lm = "#" if length_marker else ""
                inner = delimiter.join(
                    (_quote_string(str(item)) if isinstance(item, str) and _needs_quoting_string(item, delimiter) else str(item))
                    for item in value
                )
                return indent + f"[{lm}{n}]: " + inner
            lm = "#" if length_marker else ""
            lines = [indent + f"[{lm}{n}]:"]
            for item in value:
                if isinstance(item, (list, dict)):
                    lines.append(indent + ' ' * indent_size + "- " + "")
                    lines.append(_encode(item, indent_level+2))
                else:
                    val = _quote_string(item) if isinstance(item, str) and _needs_quoting_string(item, delimiter) else str(item)
                    lines.append(indent + ' ' * indent_size + f"- {val}")
            return "\n".join(lines)
        return indent + json.dumps(value)
    return _encode(obj, 0)

def decode(toon_str, *, indent_size=2, delimiter=','):
    raise NotImplementedError("Decoding not yet implemented.")
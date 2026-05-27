# io_handlers.py

def remove_comment(line):
    """Removes comments from a line. Everything after '#' is ignored."""
    return line.split("#", 1)[0].strip()


def load_vertices(filename):
    """Loads station names from a text file."""
    vertices = []
    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = remove_comment(line)
            if not line:
                continue
            if line in vertices:
                raise ValueError(f"Duplicate vertex '{line}' in {filename}, line {line_number}")
            vertices.append(line)

    if not vertices:
        raise ValueError("Vertices file is empty.")
    return vertices


def load_edges(filename):
    """Loads edges from a text file."""
    edges = []
    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = remove_comment(line)
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(
                    f"Invalid edge format in {filename}, line {line_number}. "
                    f"Expected: station1 station2"
                )
            u, v = parts
            edges.append((u, v))
    return edges


def load_settings(filename):
    """Loads program settings."""
    settings = {
        "START": None,
        "B": None,
        "FORBIDDEN": set()
    }
    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = remove_comment(line)
            if not line:
                continue
            if "=" not in line:
                raise ValueError(
                    f"Invalid settings format in {filename}, line {line_number}. "
                    f"Expected KEY=VALUE."
                )

            key, value = line.split("=", 1)
            key = key.strip().upper()
            value = value.strip()

            if key == "START":
                settings["START"] = value
            elif key == "B":
                try:
                    settings["B"] = int(value)
                except ValueError:
                    raise ValueError(f"B must be an integer in {filename}, line {line_number}")
            elif key == "FORBIDDEN":
                settings["FORBIDDEN"] = set(value.split()) if value else set()
            else:
                raise ValueError(f"Unknown setting '{key}' in {filename}, line {line_number}")

    if settings["START"] is None:
        raise ValueError("Missing START setting.")
    if settings["B"] is None:
        raise ValueError("Missing B setting.")
    if settings["B"] < 0:
        raise ValueError("B cannot be negative.")

    return settings
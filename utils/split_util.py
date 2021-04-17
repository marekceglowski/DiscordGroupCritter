def split(text, wrap_at=2000):
    lines = text.split("\n")
    response_lines = []
    chunk = ''

    for line in lines:
        if (len(chunk) + len(line)) > wrap_at:
            response_lines.append(chunk)
            chunk = ''
        chunk += line + "\n"
    if response_lines[-1] != chunk:
        response_lines.append(chunk)

    return response_lines

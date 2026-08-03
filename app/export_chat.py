from datetime import datetime

def export_chat(messages):

    filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    content = ""

    for msg in messages:

        role = msg["role"].upper()

        content += f"{role}\n"

        content += msg["content"]

        content += "\n\n"

    return filename, content
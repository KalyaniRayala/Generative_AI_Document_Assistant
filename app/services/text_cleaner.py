import re
def remove_extra_spaces(text:str)->str:
     return re.sub(r"[\t]+", "",text)

def remove_blank_lines(text:str)->str:
     return re.sub(r"\n\s*\n+","\n\n",text)

def remove_section_separators(text:str)->str:

     text=re.sub(r"^=+$","",text, flags=re.MULTILINE)
     text=re.sub(r"^=-$","",text, flags=re.MULTILINE)
     return text

def remove_double_backticks(text:str)->str:

     return text.replace("``","")

def remove_rst_directives(text:str)-> str:

     return re.sub(r"^\.\.\s.*$", "",text, flags=re.MULTILINE)

def clean_text(text: str) -> str:
    text = remove_extra_spaces(text)
    text = remove_blank_lines(text)
    text = remove_section_separators(text)
    text = remove_double_backticks(text)
    text = remove_rst_directives(text)

    return text.strip()
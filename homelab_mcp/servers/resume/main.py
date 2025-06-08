from fastmcp import FastMCP
import pypdf
import os

resume_mcp = FastMCP("resume")

@resume_mcp.tool
def get_resume() -> str:
    """Get Subhranshu's Resume"""
    reader = pypdf.PdfReader(f'{os.getcwd()}\\resources\\Subhranshu_Resume_2025.pdf')
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
#!/usr/bin/env python3
import os
import re
import base64

base_dir = "/home/tsuki/Documents/coda/2026-2027/project/tasks-api/randu"
md_path = os.path.join(base_dir, "DOSSIER_RENDU.md")
html_path = os.path.join(base_dir, "DOSSIER_RENDU.html")

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

def get_base64_image(rel_path):
    full_path = os.path.join(base_dir, rel_path)
    if os.path.exists(full_path):
        ext = os.path.splitext(full_path)[1].lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        with open(full_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode("utf-8")
        return f"data:{mime};base64,{encoded}"
    return rel_path

css = """
<style>
@page {
    size: A4;
    margin: 15mm;
}
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1a1a1a;
    line-height: 1.5;
    font-size: 11pt;
    margin: 0;
    padding: 0;
}
.page-break {
    page-break-before: always;
}
h1 {
    color: #0969da;
    border-bottom: 2px solid #eaecef;
    padding-bottom: 6px;
    margin-top: 24px;
    font-size: 18pt;
}
h2 {
    color: #1f2328;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 4px;
    margin-top: 20px;
    font-size: 14pt;
}
h3 {
    color: #24292f;
    margin-top: 16px;
    margin-bottom: 6px;
    font-size: 12pt;
}
p {
    margin: 6px 0;
}
ul, ol {
    margin: 6px 0;
    padding-left: 24px;
}
li {
    margin-bottom: 4px;
}
code {
    background-color: #f6f8fa;
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 9.5pt;
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}
.header-box {
    background-color: #f6f8fa;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    padding: 16px;
    margin-bottom: 24px;
}
.header-box h1 {
    border-bottom: none;
    margin-top: 0;
    padding-bottom: 0;
}
.capture-box {
    margin: 12px 0 16px 0;
    text-align: center;
    page-break-inside: avoid;
}
.capture-box img {
    max-width: 95%;
    max-height: 380px;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
strong {
    color: #000;
}
a {
    color: #0969da;
    text-decoration: none;
}
</style>
"""

lines = text.split("\n")
html_out = ["<!DOCTYPE html><html><head><meta charset='utf-8'><title>Dossier GitOps & CI/CD - Alban ELIE</title>", css, "</head><body>"]

i = 0
while i < len(lines):
    line = lines[i]
    
    if line.startswith("# Dossier de rendu"):
        html_out.append("<div class='header-box'>")
        html_out.append(f"<h1>{line.replace('# ', '')}</h1>")
        i += 1
        while i < len(lines) and not lines[i].startswith("---"):
            if lines[i].strip():
                hl = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", lines[i])
                hl = re.sub(r"\[(.*?)\]\((.*?)\)", r"<a href='\2'>\1</a>", hl)
                html_out.append(f"<p>{hl}</p>")
            i += 1
        html_out.append("</div>")
        i += 1
        continue

    if line.startswith("# TP") or line.startswith("# Bilan"):
        html_out.append(f"<div class='page-break'></div><h1>{line.replace('# ', '')}</h1>")
        i += 1
        continue

    if line.startswith("### "):
        html_out.append(f"<h3>{line.replace('### ', '')}</h3>")
        i += 1
        continue

    if line.startswith("## "):
        html_out.append(f"<h2>{line.replace('## ', '')}</h2>")
        i += 1
        continue

    # Image
    img_match = re.match(r"!\[(.*?)\]\((.*?)\)", line.strip())
    if img_match:
        alt, src = img_match.groups()
        b64 = get_base64_image(src)
        html_out.append(f"<div class='capture-box'><img src='{b64}' alt='{alt}'></div>")
        i += 1
        continue

    # Capture item line followed by image
    if line.startswith("* **TP") or line.startswith("- **TP") or line.startswith("* **Q") or line.startswith("- **Q"):
        hl = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line[2:])
        hl = re.sub(r"`(.*?)`", r"<code>\1</code>", hl)
        hl = re.sub(r"\[(.*?)\]\((.*?)\)", r"<a href='\2'>\1</a>", hl)
        html_out.append(f"<p style='margin-top: 10px;'>{hl}</p>")
        i += 1
        continue

    if line.startswith("  !["):
        sub_img = re.match(r"\s*!\[(.*?)\]\((.*?)\)", line)
        if sub_img:
            alt, src = sub_img.groups()
            b64 = get_base64_image(src)
            html_out.append(f"<div class='capture-box'><img src='{b64}' alt='{alt}'></div>")
        i += 1
        continue

    if line.strip():
        hl = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", line)
        hl = re.sub(r"`(.*?)`", r"<code>\1</code>", hl)
        hl = re.sub(r"\[(.*?)\]\((.*?)\)", r"<a href='\2'>\1</a>", hl)
        if line.startswith("- ") or line.startswith("* "):
            html_out.append(f"<ul><li>{hl[2:]}</li></ul>")
        elif re.match(r"^\d+\.\s", line):
            num_match = re.match(r"^\d+\.\s(.*)", hl)
            html_out.append(f"<ol><li>{num_match.group(1)}</li></ol>")
        else:
            html_out.append(f"<p>{hl}</p>")
    i += 1

html_out.append("</body></html>")

with open(html_path, "w", encoding="utf-8") as f:
    f.write("\n".join(html_out))

print("HTML generated successfully with base64 embedded images!")

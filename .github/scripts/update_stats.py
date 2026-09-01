import os
import requests

GITHUB_TOKEN = os.getenv("GH_TOKEN")
GITHUB_USER = os.getenv("GH_USER", "adolforopeza")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "Stats-Script"
}

# Diccionario ampliado con más de 100 colores oficiales de lenguajes (GitHub Linguist)
COLORS = {
    "PHP": "4F5D95", "JavaScript": "F1E05A", "HTML": "E34C26", "CSS": "563D7C",
    "Less": "1D365D", "Shell": "89E051", "GDScript": "355570", "Vue": "41B883",
    "SCSS": "C6538C", "PLpgSQL": "336791", "VCL": "1B887A", "Hack": "878787",
    "Python": "3776AB", "Rust": "DEA584", "C++": "F34B7D", "C": "555555",
    "TypeScript": "3178C6", "Go": "00ADD8", "Java": "B07219", "Ruby": "701516",
    "C#": "178600", "Swift": "F05138", "Kotlin": "A97BFF", "Dart": "00B4AB",
    "Lua": "000080", "Perl": "0298C3", "R": "198CE7", "Scala": "C22D40",
    "Shell": "89E051", "PowerShell": "012456", "Dockerfile": "384d54", "SQL": "E38C00",
    "Assembly": "6E4C13", "Batch": "C1F12E", "Clojure": "DB5855", "CoffeeScript": "244776",
    "Crystal": "000100", "Elixir": "6e4a7e", "Elm": "60B5CC", "Erlang": "B83998",
    "F#": "B845FC", "Fortun": "4D41B1", "Go Module": "00ADD8", "Groovy": "4298B8",
    "Haskell": "5e5086", "Julia": "a270ba", "Lisp": "3fb68b", "Makefile": "427819",
    "Matlab": "e16737", "Nim": "ffc200", "Objective-C": "438eff", "OCaml": "3be133",
    "Pascal": "E3F171", "Perl": "0298C3", "PHP": "4F5D95", "PostScript": "da291c",
    "Prolog": "74283c", "Puppet": "302B6D", "PureScript": "1D222D", "Racket": "3c5b8f",
    "Reason": "ff5847", "Rebol": "358a5b", "Ring": "2A5484", "RobotFramework": "00c0b5",
    "Roff": "ecdebe", "RPMSpec": "c7254e", "Ruby": "701516", "Rust": "DEA584",
    "SAS": "B34936", "Sass": "a53b70", "Scala": "C22D40", "Scheme": "1e4aec",
    "Scilab": "ca0f21", "Solidity": "AA6746", "SourcePawn": "f69e1d", "SQF": "3F3F3F",
    "Standard ML": "dc566d", "Stata": "1a5f91", "SuperCollider": "46390b",
    "Svelte": "ff3e00", "Tcl": "e4cc91", "TeX": "3D6117", "Thrift": "D12127",
    "Turing": "cf142b", "TypeScript": "3178C6", "Unified Parallel C": "4e3629",
    "Unity3D": "222c37", "Vala": "fbe5cd", "Verilog": "b2b7f8", "VHDL": "adb2cb",
    "Visual Basic": "945db7", "WebAssembly": "04133b", "WGSL": "1b64d1",
    "XML": "0060ac", "XSLT": "EB8CEB", "Yacc": "4b6c4b", "YAML": "cb171e",
    "Zig": "ec915c", "ZAP": "db6b00", "C#": "178600", "GDScript": "355570"
}

def get_all_repositories():
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100&page={page}&type=all"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def main():
    repos = get_all_repositories()
    global_languages = {}
    total_bytes = 0

    for repo in repos:
        if repo.get("fork"): # Opcional: ignorar forks si se desea
            continue
        lang_url = repo.get("languages_url")
        if not lang_url:
            continue
        
        lang_res = requests.get(lang_url, headers=HEADERS)
        if lang_res.status_code == 200:
            langs = lang_res.json()
            for lang, bytes_count in langs.items():
                global_languages[lang] = global_languages.get(lang, 0) + bytes_count
                total_bytes += bytes_count

    # Calcular porcentajes ordenados de mayor a menor
    sorted_langs = sorted(global_languages.items(), key=lambda x: x[1], reverse=True)
    
    markdown_badges = []
    for lang, bytes_count in sorted_langs:
        percentage = (bytes_count / total_bytes) * 100 if total_bytes > 0 else 0
        color = COLORS.get(lang, "777BB4") # Color por defecto si no existe en el diccionario
        pct_str = f"{percentage:.2f}%".replace("%", "%25")
        badge_url = f"https://img.shields.io/badge/{lang}-{pct_str}-{color}?style=for-the-badge&logo={lang.lower()}&logoColor=white"
        markdown_badges.f(f"![{lang}]({badge_url})")

    # Inyectar en README.md entre marcas específicas
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!--START_SECTION:languages-->"
    end_marker = "<!--END_SECTION:languages-->"

    badges_block = "\n".join(markdown_badges)
    
    if start_marker in content and end_marker in content:
        start_idx = content.find(start_marker) + len(start_marker)
        end_idx = content.find(end_marker)
        new_content = content[:start_idx] + "\n" + badges_block + "\n" + content[end_idx:]
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)

if __name__ == "__main__":
    main()

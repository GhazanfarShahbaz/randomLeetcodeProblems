messageSyntax = {
    "c": "c",
    "c++": "cpp",
    "c#": "c",
    "java": "java",
    "python": "py",
    "python3": "py",
    "javascript": "js",
    "ruby": "ruby",
    "swift": "swift",
    "go": "go",
    "scala": "scala",
    "kotlin": "kotlin",
    "rust": "rust",
    "php": "php",
    "typescript": "typescript"
}


def getLanguageCode(lang : str) -> None or str:
    return None if lang.lower() not in messageSyntax.keys() else messageSyntax[lang.lower()]

def checkLanguage(lang : str) -> str:
    return lang.title() in messageSyntax.keys()
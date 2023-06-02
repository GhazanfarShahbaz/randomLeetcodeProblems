from typing import Dict, Optional

messageSyntax: Dict[str, str] = {
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


def getLanguageCode(lang: str) -> Optional[str]:
    """
    Returns the language code that corresponds to the given language, or None if the language is not recognized.

    Args:
        lang (str): The name of the language.

    Returns:
        Optional[str]: The language code that corresponds to the given language, or None if the language is not recognized.
    """
    return None if lang.lower() not in messageSyntax.keys() else messageSyntax[lang.lower()]

def checkLanguage(lang: str) -> bool:
    """
    Returns whether the given language is currently supported by the bot.

    Args:
        lang (str): The language to check.

    Returns:
        bool: True if the language is supported, False otherwise.
    """
    return lang.lower() in messageSyntax.keys()
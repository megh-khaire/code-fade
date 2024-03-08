LANGUAGE_EXTENSIONS = {
    "Python": [".py"],
    "JavaScript": [".js"],
    "Java": [".java"],
    "C": [".c"],
    "C++": [".cpp", ".cxx", ".cc", ".h", ".hpp", ".hxx"],
    "C#": [".cs"],
    "Ruby": [".rb"],
    "PHP": [".php"],
    "Swift": [".swift"],
    "Kotlin": [".kt"],
    "Go": [".go"],
    "Rust": [".rs"],
    "TypeScript": [".ts"],
    "Scala": [".scala"],
    "Objective-C": [".m", ".h"],
    "Shell": [".sh", ".bash"],
    "Perl": [".pl", ".pm"],
    "Lua": [".lua"],
    "Haskell": [".hs", ".lhs"],
    "Erlang": [".erl"],
    "Clojure": [".clj", ".cljs", ".cljc"],
    "Dart": [".dart"],
    "R": [".r", ".R"],
    "Julia": [".jl"],
    "HTML": [".html", ".htm"],
    "CSS": [".css"],
    "SQL": [".sql"],
    "XML": [".xml"],
    "Markdown": [".md"],
    "YAML": [".yaml", ".yml"],
    "JSON": [".json"],
    "Dockerfile": ["Dockerfile"],
}


def get_extension_from_language(language):
    if language in LANGUAGE_EXTENSIONS:
        return LANGUAGE_EXTENSIONS[language][0]
    return None

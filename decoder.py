import os
import json
import sys

TEXT_EXTENSIONS = {
    ".py",".js",".ts",".tsx",".jsx",".java",".c",".cpp",".cxx",
    ".h",".hpp",".cs",".go",".rs",".php",".kt",".swift",".rb",
    ".sh",".sql",".html",".css",".json",".xml",".yml",".yaml",
    ".md",".txt",".properties",".gradle",".bat",".ps1"
}

SEPARATORS = {
    ' ','\t','\n','\r',
    '(',')','{','}','[',']',
    ';',',','.',
    ':','?','!','@','#','$','%','^','&','*',
    '+','-','=','<','>','/','\\','|','~',
    '"',"'",'`'
}

IGNORE_FILES = {
    "alias_to_token.json",
    "token_to_alias.json"
}

def is_text_file(path):
    return os.path.splitext(path)[1].lower() in TEXT_EXTENSIONS

def decode_content(content, alias_to_token):
    result = []
    token = []

    for ch in content:
        if ch in SEPARATORS:
            if token:
                t = ''.join(token)
                result.append(alias_to_token.get(t, t))
                token.clear()

            result.append(ch)
        else:
            token.append(ch)

    if token:
        t = ''.join(token)
        result.append(alias_to_token.get(t, t))

    return ''.join(result)

def restore_repository(compressed_dir, output_dir):
    mapping_file = os.path.join(compressed_dir, "alias_to_token.json")

    if not os.path.exists(mapping_file):
        raise FileNotFoundError(
            f"alias_to_token.json not found: {mapping_file}"
        )

    with open(mapping_file, "r", encoding="utf-8") as f:
        alias_to_token = json.load(f)

    for root, dirs, files in os.walk(compressed_dir):
        dirs[:] = [d for d in dirs if d != ".git"]

        rel_root = os.path.relpath(root, compressed_dir)

        target_root = (
            output_dir
            if rel_root == "."
            else os.path.join(output_dir, rel_root)
        )

        os.makedirs(target_root, exist_ok=True)

        for file_name in files:
            if file_name in IGNORE_FILES:
                continue

            src_path = os.path.join(root, file_name)
            dst_path = os.path.join(target_root, file_name)

            if not is_text_file(src_path):
                with open(src_path, "rb") as src:
                    data = src.read()

                with open(dst_path, "wb") as dst:
                    dst.write(data)

                continue

            with open(src_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            restored = decode_content(content, alias_to_token)

            with open(dst_path, "w", encoding="utf-8") as f:
                f.write(restored)

    print("Repository restored:")
    print(output_dir)

def main():
    if len(sys.argv) != 4:
        print(
            "Usage:\n"
            "python decoder.py restore <compressed_dir> <output_dir>"
        )
        sys.exit(1)

    command = sys.argv[1]

    if command != "restore":
        print("Only supported command: restore")
        sys.exit(1)

    compressed_dir = sys.argv[2]
    output_dir = sys.argv[3]

    restore_repository(compressed_dir, output_dir)

if __name__ == "__main__":
    main()
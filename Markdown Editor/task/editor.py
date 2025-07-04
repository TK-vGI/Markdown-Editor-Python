import tempfile
import webbrowser
from typing import List
import markdown

DATA_FILE = "output.md"


def formatter_help() -> None:
    print("Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line")
    print("Special commands: !help !done !preview")


def formatter_header() -> str:
    while True:
        try:
            user_level = int(get_input("Level: "))
            if 1 <= user_level <= 6:
                break
            print("The level should be within the range of 1 to 6")
        except ValueError:
            print("Please enter a valid number")

    user_text = get_input("Text: ")
    return f"{"#" * user_level} {user_text}\n"


def formatter_plaintext() -> str:
    user_text = get_input("Text: ")
    return f"{user_text}"


def formatter_bold() -> str:
    user_text = get_input("Text: ")
    return f"**{user_text}**"


def formatter_italic() -> str:
    user_text = get_input("Text: ")
    return f"*{user_text}*"


def formatter_link() -> str:
    user_label = get_input("Label: ")
    user_url = get_input("URL: ")
    return f"[{user_label}]({user_url})"


def formatter_inline_code() -> str:
    user_code = get_input("Text: ")
    return f"`{user_code}`"


def formatter_newline() -> str:
    return "\n"


def formatter_ordered_list(ordered: bool = True) -> str:
    while True:
        try:
            rows = int(get_input("Number of rows: "))
            if rows > 0:
                break
            print("The number of rows should be greater than zero")
        except ValueError:
            print("Please enter a valid number")

    items: List = get_list_items(rows)
    if ordered:
        return "\n".join(f"{i + 1}. {item}" for i, item in enumerate(items)) + "\n"
    else:
        return "\n".join(f"* {item}" for item in items) + "\n"


def get_list_items(count: int) -> list[str]:
    return [get_input(f"Row #{i + 1}: ") for i in range(count)]


def get_input(prompt: str) -> str:
    return input(prompt).strip()


def preview_markdown(markdown_text: str) -> None:
    html_content = markdown.markdown(markdown_text)
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as tmp:
        tmp.write(f"<html><body>{html_content}</body></html>")
        tmp_path = tmp.name
    webbrowser.open(f"file://{tmp_path}")


# Formatter dispatcher
formatters = {
    "!help": "help",
    "!done": "done",
    "!preview": preview_markdown,
    "plain": formatter_plaintext,
    "bold": formatter_bold,
    "italic": formatter_italic,
    "header": formatter_header,
    "link": formatter_link,
    "inline-code": formatter_inline_code,
    "new-line": formatter_newline,
    "ordered-list": lambda: formatter_ordered_list(True),
    "unordered-list": lambda: formatter_ordered_list(False),
}


def main():
    output = []

    while True:
        user_input = get_input("Choose a formatter: ").lower()

        if user_input == "!done":
            with open("output.md", "w", encoding="utf-8") as f:
                f.write("".join(output))
            # print("Markdown content saved to output.md")
            break

        elif user_input == "!help":
            formatter_help()

        elif user_input == "!preview":
            preview_markdown("".join(output))

        elif user_input in formatters:
            result = formatters[user_input]()
            if user_input == "header" and output:
                result = "\n" + result
            output.append(result)
            print("".join(output))

        else:
            print("Unknown formatting type or command")


if __name__ == '__main__':
    main()

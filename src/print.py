from typing import Any

# baztodo: Reuse these from bazpy

def print_line(
    break_before: bool,
    value: Any,
    break_after: bool = False,
) -> None:
    text = f"  {value}  "
    text = f"{text:_^68}"
    text = ("\n" if break_before else "") + text
    text = text + ("\n" if break_after else "")
    print(f"{text}")


def print_vertical_space(n: int, filler: Any = ".") -> None:
    print(" ", end="\r", flush=True)
    print(" ")
    line_contents = [filler] * (n)
    text = "\n".join(line_contents)
    print(text)

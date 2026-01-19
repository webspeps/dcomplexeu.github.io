
def info_hider(input_string: str) -> str:
    """Creates a string that is non-copiable.
    Returns:
        str: String that is non-copiable.
    """
    symbol_map: dict[str, str] = {
        "0": r'<b class="d-zero"></b>',
        "1": r'<b class="d-one"></b>',
        "2": r'<b class="d-two"></b>',
        "3": r'<b class="d-three"></b>',
        "4": r'<b class="d-four"></b>',
        "5": r'<b class="d-five"></b>',
        "6": r'<b class="d-six"></b>',
        "7": r'<b class="d-seven"></b>',
        "8": r'<b class="d-eight"></b>',
        "9": r'<b class="d-nine"></b>',
        # Symbols
        "+": r'<b class="d-plus"></b>',
        "@": r'<b class="d-at"></b>',
        ".": r'<b class="d-dot"></b>',
        ",": r'<b class="d-comma"></b>',
    }
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    for letter in letters:
        cls_name = f"ltr-l-{letter}"
        if letter.isupper():
            cls_name = f"ltr-u-{letter}"
        symbol_map[letter] = f'<b class="{cls_name}"></b>'

    res_str = ""
    for symbol in input_string:
        if symbol in symbol_map:
            res_str += symbol_map[symbol]
        else:
            res_str += symbol
    return res_str

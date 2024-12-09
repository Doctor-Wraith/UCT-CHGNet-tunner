
def get_input(msg: str, allow_blank: bool = False) -> str:
    while True:
        i = input(msg)
        if allow_blank:
            return i
        else:
            if i.strip() == "":
                continue
            else:
                return i


def sort_dict(d: dict) -> dict:
    """
    Sorts a dictionary using

    Args:
        d (dict): Input dict
    Returns:
        dict
    """

    return dict(sorted(d.items(), key=lambda item: item[1])[::-1])


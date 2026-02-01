def unit_converter(number_in_bytes) -> tuple[float, str]:
    """General memory unit converter"""
    if number_in_bytes < 1024.0:
        return (number_in_bytes, "B")
    number_in_kilobytes = number_in_bytes/1024.0
    if number_in_kilobytes < 1024:
        return (number_in_kilobytes, "KB")
    number_in_megabytes = number_in_kilobytes/1024.0
    if number_in_megabytes < 1024:
        return (number_in_megabytes, "MB")
    number_in_gigabtyes = number_in_megabytes/1024.0
    if number_in_gigabtyes < 1024.0:
        return (number_in_gigabtyes, "GB")
    number_in_terrabytes = number_in_gigabtyes/1024.0
    return (number_in_terrabytes, "TB")

def convert_mem_unit(kb_used: float, kb_total: float, same_units: bool=None, given_unit: str=None) -> tuple[float, str, float, str]:
    """
    Convert memory to suitable units for the RAM graph.

    Arguments:
        same_units: whether the total should be the same unit as used instead of the largest possible one
        given_unit: use the given unit instead of calculating it

    Returns:
        A tuple in a (used ram, used ram unit, total ram, total ram unit)
    """
    conv_used: float
    used_unit: str
    conv_total: float
    total_unit: str

    # kb
    if (kb_used/1024 < 1024.0 and not given_unit) or given_unit == "KiB":
        conv_used = kb_used
        used_unit = "KiB"
        if same_units:
            conv_total = kb_total
            total_unit = "KiB"
        elif kb_total/1024.0/1024 < 1024.0:
            conv_total = kb_total/1024.0/1024
            total_unit = "MiB"
        elif kb_total/1024.0/1024.0/1024 < 1024.0:
            conv_total = kb_total/1024.0/1024.0/1024
            total_unit = "GiB"
    # mb
    elif (kb_used/1024.0/1024 < 1024.0 and not given_unit) or given_unit == "MiB":
        conv_used = kb_used/1024.0/1024
        used_unit = "MiB"
        if (kb_total/1024.0/1024 < 1024.0) or same_units:
            conv_total = kb_total/1024.0/1024
            total_unit = "MiB"
        elif kb_total/1024.0/1024.0/1024 < 1024.0:
            conv_total = kb_total/1024.0/1024.0/1024
            total_unit = "GiB"
    # gb
    elif (kb_total/1024.0/1024.0/1024 < 1024.0 and not given_unit) or given_unit == "GiB":
        conv_used = kb_used/1024.0/1024.0/1024
        used_unit = "GiB"
        conv_total = kb_total/1024.0/1024.0/1024
        total_unit = "GiB"

    return (round(conv_used, 2), used_unit, round(conv_total, 2), total_unit)

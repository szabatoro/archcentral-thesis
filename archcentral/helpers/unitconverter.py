def unit_converter(number_in_bytes, as_tuple: bool = True) -> tuple[float, str] | str:
    """General memory unit converter"""
    if number_in_bytes < 1024.0:
        return (number_in_bytes, "B") if as_tuple else f"{number_in_bytes:.2f} B"
    number_in_kilobytes = number_in_bytes/1024.0
    if number_in_kilobytes < 1024:
        return (number_in_kilobytes, "KiB") if as_tuple else f"{number_in_kilobytes:.2f} KiB"
    number_in_megabytes = number_in_kilobytes/1024.0
    if number_in_megabytes < 1024:
        return (number_in_megabytes, "MiB") if as_tuple else f"{number_in_megabytes:.2f} MiB"
    number_in_gigabytes = number_in_megabytes/1024.0
    if number_in_gigabytes < 1024.0:
        return (number_in_gigabytes, "GiB") if as_tuple else f"{number_in_gigabytes:.2f} GiB"
    number_in_terrabytes = number_in_gigabytes/1024.0
    return (number_in_terrabytes, "TiB") if as_tuple else f"{number_in_terrabytes:.2f} TiB"

def convert_mem_unit(bytes_used: float, bytes_total: float) -> tuple[float, str, float, str]:
    """
    Convert memory to suitable units for the RAM graph.

    Automatically chooses the best unit for used memory and shows
    total in the largest appropriate unit (often different from used).

    Arguments:
        bytes_used: used memory in bytes
        bytes_total: total memory in bytes

    Returns:
        A tuple in the format (used ram, used ram unit, total ram, total ram unit)
    """
    # KiB
    if bytes_used / 1024 < 1024.0:
        conv_used = bytes_used / 1024
        used_unit = "KiB"

        # Total: prefer MiB, fall back to GiB if large
        if bytes_total / 1024 / 1024 < 1024.0:
            conv_total = bytes_total / 1024 / 1024
            total_unit = "MiB"
        else:
            conv_total = bytes_total / 1024 / 1024 / 1024
            total_unit = "GiB"

    # MiB
    elif bytes_used / 1024 / 1024 < 1024.0:
        conv_used = bytes_used / 1024 / 1024
        used_unit = "MiB"

        if bytes_total / 1024 / 1024 < 1024.0:
            conv_total = bytes_total / 1024 / 1024
            total_unit = "MiB"
        else:
            conv_total = bytes_total / 1024 / 1024 / 1024
            total_unit = "GiB"

    # GiB
    else:
        conv_used = bytes_used / 1024 / 1024 / 1024
        used_unit = "GiB"
        conv_total = bytes_total / 1024 / 1024 / 1024
        total_unit = "GiB"

    return (round(conv_used, 2), used_unit, round(conv_total, 2), total_unit)

# Convert memory to suitable units
# same_units: whether the total should be the same unit as used instead of the largest possible one
# given_unit: use the given unit instead of calculating it
def convert_mem_unit(kb_used: float, kb_total: float, same_units: bool=None, given_unit: str=None) -> tuple[float, str, float, str]:
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

from .utils import apply_color


def item_details(item, color_id):
    _cls_name_str = f"\t\t\t\t{item.__class__.__name__} --------------\n"
    _cls_name_str_len = len(_cls_name_str)
    txt_output = _cls_name_str
    txt_output += f"\t\t\t\t   |\n"
    txt_output += f"\t\t\t\t   • ID           --->  {item.rule_id!r}\n"
    txt_output += f"\t\t\t\t   |\n"
    txt_output += f"\t\t\t\t   • HEAD         --->  {item.rule_head!r}\n"
    txt_output += f"\t\t\t\t   |\n"
    txt_output += f"\t\t\t\t   • BODY         --->  {list(item.rule_body)!r}\n"
    txt_output += f"\t\t\t\t   |\n"
    txt_output += f"\t\t\t\t   • STATUS       --->  {list(item.status())!r}\n"
    txt_output += f"\t\t\t\t   |\n"
    txt_output += f"\t\t\t\t   • NEXT SYMBOL  --->  {list(item.next_symbol(default=[]))!r}\n"
    txt_output += f"\t\t\t\t   |\n"
    txt_output += f"\t\t\t\t   • PREV SYMBOL  --->  {list(item.prev_symbol(default=[]))!r}\n"
    txt_output += f"\t\t\t\t   |\n\t\t\t\t   • "
    _temp_end = "-"
    while True:
        if len(_temp_end) + 7 > _cls_name_str_len - 4:
            break
        _temp_end += f"-"
    txt_output += _temp_end
    return apply_color(color_id, txt_output)


if __name__ == "__main__":
    pass

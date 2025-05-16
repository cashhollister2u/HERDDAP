import html

def render_text(value, width):
    return f'<span style="display: inline-block; width: {width};" >{value}</span>'

def render_link(value, data_label):
    return f"<a href='{value}'>{data_label}</a>"

def render_img(value, src):
    return f"<a href='{value}'><img src='{src}'></a>"

def render_popup(value, data_label):
    escaped_value = html.escape(value).replace('\n', '\\n').replace("'", "\\'")
    return f'<button onclick="showPopup(\'{escaped_value}\')">{data_label}</button>'

def truncate_string(value, length=20):
    if len(value) > length:
        return value[:length] + "..."
    return value
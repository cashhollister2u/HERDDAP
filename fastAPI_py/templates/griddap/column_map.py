from utilities.render_tools import render_text, render_link, render_img, render_popup, truncate_string

column_render_map = {
        "griddap": {
            "label": "Griddap", 
            "class": "content",
            "render": render_link,
            "render_param": "data",
            },
        "Subset": {
            "label": "Subset", 
            "class": ""
            },
        "tabledap": {
            "label": "Table DAP Data", 
            "class": ""
            },
        "Make A Graph": {
            "label": "Make A Graph", 
            "class": "",
            "render": render_link,
            "render_param": "graph"
            },
        "wms": {
            "label": "WMS", 
            "class": ""
            },
        "files": {
            "label": "Source Data Files", 
            "class": ""
            },
        "Title": {
            "label": "Title", 
            "class": "content",
            "render": render_text,
            "render_param": '10rem'
            },
        "Summary": {
            "label": "Summary", 
            "class": "",
            "render": render_popup,
            "render_param": "Summary"
            },
        "Info": {
            "label": "Meta Data", 
            "class": "",
            "render": render_link,
            "render_param": "M"
            },
        "Background Info": {
            "label": "Background Info", 
            "class": "",
            "render": render_link,
            "render_param": "background"
            },
        "RSS": {
            "label": "RSS", 
            "class": "",
            "render": render_img,
            "render_param": "/static/images/rss.gif"
            },
        "Institution": {
            "label": "Institution", 
            "class": "",
            "render": truncate_string,
            "render_param": 15
            },
        "Dataset ID": {
            "label": "Dataset ID", 
            "class": "content"
            }
    }
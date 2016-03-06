import json

html = "<html>"


def generate_website():
    global html
    add_headers("data/headers.json")
    html += "\n\t<body>\n\t\t<div class=\"container\">"
    add_body()
    html += "\n\t\t</div>\n\t</body>"
    print(html)


def add_body():
    global html
    html += "\n\t\t\t<div class=\"row\">"
    html += "\n\t\t\t\t<div class=\"col s12 m12 l10\">"
    add_about_me("data/about-me.json")
    add_education("data/education.json")
    add_experience("data/experience.json")
    add_skills("data/skills.json")
    add_projects("data/projects.json")
    add_timeline("data/timeline.json")
    html += "\n\t\t\t\t</div>"
    html += "\n\t\t\t\t<div class=\"col hide-on-small-only l2\">"
    add_table_of_contents()
    html += "\n\t\t\t\t</div>"
    html += "\n\t\t\t</div>"


def add_headers(filename):
    global html
    data = read_json_file(filename)
    html += "\n\t<head>\n\t\t<title>" + data['title'] + "</title>"
    html += "\n\t\t<meta charset=\"" + data['charset'] + "\" />"
    for meta in data['content-metas']:
        html += "\n\t\t"
        html += get_meta_tag(meta['name'], meta['content'])
    for link in data['links']:
        html += "\n\t\t"
        if link['type'] == 'css':
            html += get_css_link(link['source'])
        elif link['type'] == 'js':
            html += get_js_link(link['source'])
        elif link['type'] == 'font':
            html += get_font_link(link['source'])
    html += "\n\t</head>"


def get_meta_tag(name, content):
    return "<meta name\"" + name + "\" content=\"" + content + "\" />"


def read_json_file(filename):
    return json.loads(open(filename).read())


def get_css_link(src):
    return "<link href=\"" + src + "\" rel=\"stylesheet\" type=\"text/css\" />"


def get_js_link(src):
    return "<script src=\"" + src + "\"></script>"


def get_font_link(src):
    return "<link href=\"" + src + "\" rel=\"stylesheet\" />"


def add_about_me(file):
    global html
    print("TODO")


def add_education(file):
    global html
    print("TODO")


def add_experience(file):
    global html
    print("TODO")


def add_skills(file):
    global html
    print("TODO")


def add_projects(file):
    global html
    print("TODO")


def add_timeline(file):
    global html
    print("TODO")


def add_table_of_contents():
    print("TODO")


generate_website()

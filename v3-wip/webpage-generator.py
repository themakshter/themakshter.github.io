import json

html = "<html>"


def generate_website():
    global html
    add_headers("data/headers.json")
    html += "\n<body>"
    add_body()


def add_body():
    add_about_me("data/about-me.json")
    add_education("data/education.json")
    add_experience("data/experience.json")
    add_skills("data/skills.json")
    add_projects("data/projects.json")
    add_timeline("data/timeline.json")


def add_headers(filename):
    global html
    data = read_json_file(filename)
    html += "\n\t<head>\n\t\t<title>" + data['title'] + "</title>"
    for link in data['links']:
        html += "\n\t\t"
        if link['type'] == 'css':
            html += get_css_link(link['source'])
        elif link['type'] == 'js':
            html += get_js_link(link['source'])
        elif link['type'] == 'font':
            html += get_font_link(link['source'])
    html += "\n\t</head>"
    print(html)


def read_json_file(filename):
    return json.loads(open(filename).read())


def get_css_link(src):
    return "<link href=\"" + src + "\" rel=\"stylesheet\" type=\"text/css\" />"


def get_js_link(src):
    return "<script src=\"" + src + "\"></script>"


def get_font_link(src):
    return "<link href=\"" + src + "\" rel=\"stylesheet\" />"


def add_about_me(file):
    print("TODO")


def add_education(file):
    print("TODO")


def add_experience(file):
    print("TODO")


def add_skills(file):
    print("TODO")


def add_projects(file):
    print("TODO")


def add_timeline(file):
    print("TODO")


generate_website()

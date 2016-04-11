import json
import time
import math


class webpage_generator:
    html = ""
    indent_level = 0

    def __init__(self):
        self.generate_website()

    def append_to_html(self,text):
        self.html += get_indentation(self.indent_level) + text

    def generate_website(self):
        self.html += "<html>"
        self.indent_level += 1
        self.add_headers("data/headers.json")
        self.add_body()
        self.indent_level -= 1
        self.append_to_html("<html>")
        write_to_file(self.html)
        print(self.html)

    def add_headers(self, file):
        data = read_json_file(file)
        self.append_to_html("<head>")
        self.indent_level += 1
        self.append_to_html("<title>" + data['title'] + "</title>")
        self.append_to_html("<meta charset=\"" + data['charset'] + "\" />")
        for meta in data['content-metas']:
            self.append_to_html(get_meta_tag(meta['name'], meta['content']))
        for link in data['links']:
            if link['type'] == 'css':
                self.append_to_html(get_css_link(link['source']))
            elif link['type'] == 'js':
                self.append_to_html(get_js_link(link['source']))
            elif link['type'] == 'font':
                self.append_to_html(get_font_link(link['source']))
        self.indent_level -= 1
        self.append_to_html("</head>")

    def add_body(self):
        self.append_to_html("<body>")
        self.indent_level += 1
        self.append_to_html("<div class=\"container\">")
        self.indent_level += 1
        self.append_to_html("<div class=\"row\">")
        self.indent_level += 1
        self.append_to_html("<div class=\"col s12 m12 l10\">")
        self.indent_level += 1
        self.add_about_me("data/about-me.json")
        self.add_education("data/education.json")
        #add_experience("data/experience.json")
        #add_skills("data/skills.json")
        #add_projects("data/projects.json")
        #add_timeline("data/timeline.json")
        self.indent_level -= 1
        self.append_to_html("</div>")
        self.append_to_html("<div class=\"col hide-on-small-only l2\">")
        #add_table_of_contents()
        self.append_to_html("</div>")
        self.indent_level -= 1
        self.append_to_html("</div>")
        self.indent_level -= 1
        self.append_to_html("</div>")
        self.indent_level -= 1
        self.append_to_html("</body>")

    def add_about_me(self,file):
        data = read_json_file(file)
        self.append_to_html("<div class=\"center-align\">")
        self.indent_level += 1
        self.append_to_html("<h1>Mohammad Ali Khan</h1>")
        self.append_to_html("<img class=\"responsive-img circle\" src=\"img/" + data['picture'] + "\" alt=\"Picture of Ali\" >")
        self.append_to_html("<br/>")
        self.append_to_html("<div id=\"social-network-icons\">")
        self.indent_level += 1
        for icon in data['social-icons']:
            self.append_to_html(get_social_icon(icon))
        self.indent_level -= 1
        self.append_to_html("</div>")
        self.append_to_html("<div id=\"about-me\" class=\"section scrollspy\">")
        self.indent_level += 1
        self.append_to_html("<p class =\"flow-text\">")
        self.indent_level += 1
        self.append_to_html(data['description'])
        self.indent_level -= 1
        self.append_to_html("</p>")
        self.indent_level -= 1
        self.append_to_html("</div>")
        self.indent_level -= 1
        self.append_to_html("</div>")

    def add_education(self, file):
        data = read_json_file(file)
        self.add_div_and_heading(data['title'], data['icon'])
        for education in data['educations']:
            self.append_to_html("<div class=\"education-instance\">")
            self.indent_level += 1
            self.append_to_html("<h3>" + education['education'] + "</h3>")
            self.append_to_html("<h4>" + education['degree'] + " - " + education['grade'] + "</h4>")
            self.add_footnotes(education['footnotes'])
            self.indent_level -= 1
            self.append_to_html("</div>")
        self.indent_level -= 1
        self.append_to_html("</div>")

    def add_div_and_heading(self, title, icon):
        self.append_to_html("<div id=\"" + title.lower() + "\" class=\"section scrollspy\">")
        self.indent_level += 1
        self.append_to_html("<h2 class=\"section-heading\" >" + title + "<i class=\"material-icons heading-icon\" >" + icon + "</i></h2>")

    def add_footnotes(self, footnotes):
        self.append_to_html("<div class=\"flex-list\">")
        self.indent_level += 1
        self.append_to_html("<ul>")
        self.indent_level += 1
        for footnote in footnotes:
            self.append_to_html("<li>" + add_footnote(footnote) + "</li>")
        self.indent_level -= 1
        self.append_to_html("</ul>")
        self.indent_level -= 1
        self.append_to_html("</div>")

def get_indentation(indent_level):
    return "\n" + ("\t" * indent_level)


def write_to_file(text):
    file = open("generated_site.html", 'w+')
    file.write(text)


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


def get_social_icon(icon):
    return "<a href=\"" + icon['link'] + "\"><img class=\"responsive-img icon\" src=\"img/" + icon['image'] + " \" alt=\"" + icon['name'] + "\" ></a>"


def add_education(file):
    global html
    data = read_json_file(file)
    html += add_div_and_heading(data['title'], data['icon'])
    for education in data['educations']:
        html += "\n\t\t\t\t\t\t<h3>" + education['education'] + "</h3>"
        html += "\n\t\t\t\t\t\t<h4>" + education['degree'] + " - " + education['grade'] + "</h4>"
        html += add_footnotes(education['footnotes'])
    html += "\n\t\t\t\t\t</div>"


def add_footnotes(footnotes):
    html = "\n\t\t\t\t\t\t<div class=\"flex-list\"><ul>"
    for footnote in footnotes:
        html += "\n\t\t\t\t\t\t\t\t\t\t<li>" + add_footnote(footnote) + "</li>"
    html += "\n\t\t\t\t\t\t</ul></div>"
    return html


def add_footnote(footnote):
    html = "<i class=\"material-icons\" >"
    text = ""
    if footnote['type'] == 'time':
        html += "date_range"
        text += get_date(footnote['time'])
    elif footnote['type'] == 'location':
        html += "place"
        text += get_location(footnote['location'])
    elif footnote['type'] == 'link':
        html += "link"
        text += get_link(footnote['link'])
    elif footnote['type'] == 'code':
        html += "code"
        text += get_link(footnote['code'])
    elif footnote['type'] == 'documentation':
        html += "insert_drive_file"
        text += get_link(footnote['documentation'])
    html += "</i>" + text
    return html


def get_date(date):
    start_date = time.strptime(date['start'], "%Y-%m-%d")
    text = time.strftime("%B %Y", start_date)
    if 'end' in date:
        end_date = time.strptime(date['end'], "%Y-%m-%d")
        text += " to " + time.strftime("%B %Y", end_date)
    return text


def get_location(location):
    return location['city'] + ", " + location['country']


def get_link(link):
    return "<a href=\"" + link['source'] + "\" > " + link['title'] + " </a>"


def add_div_and_heading(title, icon):
    html = "\n\t\t\t\t\t<div id=\"" + title.lower() + "\" class=\"section scrollspy\">"
    html += "\n\t\t\t\t\t\t<h2 class=\"section-heading\" >" + title + "<i class=\"material-icons heading-icon\" >" + icon + "</i></h2>"
    return html


def add_experience(file):
    global html
    data = read_json_file(file)
    html += add_div_and_heading(data['title'], data['icon'])
    for experience in data['experiences']:
        html += "\n\t\t\t\t\t\t<h3>" + experience['company'] + "</h3>"
        html += "\n\t\t\t\t\t\t<h4>" + experience['position'] + "</h4>"
        html += add_footnotes(experience['footnotes'])
    html += "\n\t\t\t\t\t</div>"


def add_skills(file):
    global html
    data = read_json_file(file)
    html += add_div_and_heading(data['title'], data['icon'])
    count = 0
    for section in data['sections']:
        if(count % 2 == 0):
            html += "\n\t\t\t\t\t\t<div class=\"row\">"
        html += "\n\t\t\t\t\t\t\t<div class\"col s6\">"
        html += add_section_data(section)
        html += "\n\t\t\t\t\t\t\t</div>"
        if(count % 2 == 1):
            html += "\n\t\t\t\t\t\t</div>"
        count += 1
    if(count % 2 != 0):
        html += "\n\t\t\t\t\t\t</div>"
    html += "\n\t\t\t\t\t</div>"


def add_section_data(section):
    html = "\n\t\t\t\t\t\t\t\t<h4>" + section['title'] + "</h4>"
    html += "\n\t\t\t\t\t\t\t\t<ul class=\"skill-list\" >"
    for rating in section['ratings']:
        html += "\n\t\t\t\t\t\t\t\t\t<li>" + add_rating(rating)
        html += "\n\t\t\t\t\t\t\t\t\t</li>"
    html += "\n\t\t\t\t\t\t\t\t</ul>"
    return html


def add_rating(rating):
    html = "\n\t\t\t\t\t\t\t\t\t\t<div class=\"row\" >"
    html += "\n\t\t\t\t\t\t\t\t\t\t\t<div class=\"col s6\" >"
    html += "\n\t\t\t\t\t\t\t\t\t\t\t\t<h5> " + rating['skill'] + " </h5>"
    html += "\n\t\t\t\t\t\t\t\t\t\t\t</div>"
    html += "\n\t\t\t\t\t\t\t\t\t\t\t<div class=\"col s6\" >"
    html += get_rating_level(float(rating['rating']))
    html += "\n\t\t\t\t\t\t\t\t\t\t\t</div>"
    html += "\n\t\t\t\t\t\t\t\t\t\t</div>"
    return html


def get_rating_level(rating):
    full_stars = math.floor(rating / 1)
    half_stars = math.ceil(rating % 1)
    empty_stars = 5 - full_stars - half_stars
    return get_stars(full_stars, "star") + get_stars(half_stars, "star_half") + get_stars(empty_stars, "star_border")


def get_stars(number, icon):
    stars = ""
    for i in range(number):
        stars += "\n\t\t\t\t\t\t\t\t\t\t\t\t<i class=\"small material-icons\" >" + icon + "</i>"
    return stars


def add_projects(file):
    global html
    data = read_json_file(file)
    html += add_div_and_heading(data['title'], data['icon'])
    count = 0
    for project in data['projects']:
        if(count % 2 == 0):
            html += "\n\t\t\t\t\t\t\t<div class=\"row\">"
        html += "\n\t\t\t\t\t\t\t\t<div class=\"col s12 m6 l6\">"
        html += create_card_for_project(project)
        html += "\n\t\t\t\t\t\t\t\t</div>"
        if(count % 2 == 1):
            html += "\n\t\t\t\t\t\t\t</div>"
        count += 1
    if(count % 2 != 0):
        html += "\n\t\t\t\t\t\t\t</div>"
    html += "\n\t\t\t\t\t</div>"
    print("TODO")


def create_card_for_project(project):
    html = "\n\t\t\t\t\t\t\t\t\t<div class=\"card\" >"
    html += "\n\t\t\t\t\t\t\t\t\t\t<div class=\"card-image waves-effect waves-block waves-light\">"
    html += "\n\t\t\t\t\t\t\t\t\t\t\t<img class=\"activator\" src=\"img/office.jpg\">"
    html += "\n\t\t\t\t\t\t\t\t\t\t</div>"
    html += "\n\t\t\t\t\t\t\t\t\t\t<div class=\"card-content\">"
    html += "\n\t\t\t\t\t\t\t\t\t\t\t<span class=\"card-title activator grey-text text-darken-4\"><b>" + project['name']
    html += "</b><i class=\"material-icons right\">more_vert</i><span>"
    html += add_footnotes(project['footnotes'])
    html += "\n\t\t\t\t\t\t\t\t\t\t</div>"
    html += "\n\t\t\t\t\t\t\t\t\t\t<div class=\"card-reveal\">"
    html += "\n\t\t\t\t\t\t\t\t\t\t\t<span class=\"card-title grey-text text-darken-4\"><b>" + project['name']
    html += "</b><i class=\"material-icons right\">close</i><span>"
    html += "\n\t\t\t\t\t\t\t\t\t\t\t<p>" + project['description'] + "</p>"
    html += add_footnotes(project['footnotes'])
    html += "\n\t\t\t\t\t\t\t\t\t\t</div>"
    html += "\n\t\t\t\t\t\t\t\t\t</div>"
    return html


def add_timeline(file):
    global html
    data = read_json_file(file)
    html += add_div_and_heading(data['title'], data['icon'])
    html += "\n\t\t\t\t\t\t<p> " + data['description'] + " </p>"
    html += "\n\t\t\t\t\t\t<div id=\"chart\"></div>"
    html += "\n\t\t\t\t\t</div>"
    print("TODO")


def add_table_of_contents():
    print("TODO")


#generate_website()

webpage_generator()

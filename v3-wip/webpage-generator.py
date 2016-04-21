import json
import time
import math


class webpage_generator:
    html = ""
    indent_level = 0
    headings = []

    def __init__(self):
        self.generate_website()

    def generate_website(self):
        self.html += "<html>"
        self.indent_level += 1
        self.add_headers("data/headers.json")
        self.add_body()
        self.decrement_add_to_html("<html>")
        write_to_file(self.html)
        print(self.html)

    def add_headers(self, file):
        data = read_json_file(file)
        self.add_increment_to_html("<head>")
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
        self.decrement_add_to_html("</head>")

    def add_body(self):
        self.add_increment_to_html("<body>")
        self.add_increment_to_html("<div class=\"container\">")
        self.add_increment_to_html("<div class=\"row\">")
        self.add_increment_to_html("<div class=\"col m12 l10\">")
        self.add_about_me("data/about-me.json")
        self.add_education("data/education.json")
        self.add_experience("data/experience.json")
        self.add_skills("data/skills.json")
        self.add_projects("data/projects.json")
        self.add_timeline("data/timeline.json")
        self.decrement_add_to_html("</div>")
        self.add_increment_to_html("<div class=\"col hide-on-med-and-down l2\">")
        self.add_table_of_contents()
        self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</body>")

    def add_about_me(self, file):
        data = read_json_file(file)
        self.add_increment_to_html("<div class=\"center-align\">")
        self.add_increment_to_html("<div id=\"about-me\" class=\"section scrollspy\">")
        self.append_to_html("<h1>Mohammad Ali Khan</h1>")
        self.append_to_html("<img class=\"responsive-img circle\" src=\"img/" + data['picture'] + "\" alt=\"Picture of Ali\" >")
        self.append_to_html("<br/>")
        self.add_increment_to_html("<div id=\"social-network-icons\">")
        for icon in data['social-icons']:
            self.append_to_html(get_social_icon(icon))
        self.decrement_add_to_html("</div>")
        self.append_to_html("<p class =\"flow-text\">" + data['description'] + "</p>")
        self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</div>")
        self.headings.append("About Me")

    def add_education(self, file):
        data = read_json_file(file)
        self.add_div_and_heading(data['title'], data['icon'])
        for education in data['educations']:
            self.add_increment_to_html("<div class=\"education-instance\">")
            self.append_to_html("<h3>" + education['education'] + "</h3>")
            self.append_to_html("<h4>" + education['degree'] + " - " + education['grade'] + "</h4>")
            self.add_footnotes(education['footnotes'])
            self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</div>")

    def add_experience(self, file):
        data = read_json_file(file)
        self.add_div_and_heading(data['title'], data['icon'])
        count = 0
        for experience in data['experiences']:
            count += 1
            self.add_increment_to_html("<div class =\"experience-instance\" >")
            self.append_to_html("<h3>" + experience['company'] + "</h3>")
            self.append_to_html("<h4>" + experience['position'] + "</h4>")
            self.add_footnotes(experience['footnotes'])
            self.decrement_add_to_html("</div>")
            if(count != len(data['experiences'])):
                self.append_to_html("<div class=\"divider\" ></div>")
        self.decrement_add_to_html("</div>")

    def add_skills(self, file):
        data = read_json_file(file)
        self.add_div_and_heading(data['title'], data['icon'])
        count = 0
        for section in data['sections']:
            if(count % 2 == 0):
                self.add_increment_to_html("<div class=\"row\">")
            self.add_increment_to_html("<div class\"col s6\">")
            self.add_section_data(section)
            self.decrement_add_to_html("</div>")
            if(count % 2 == 1):
                self.decrement_add_to_html("</div>")
            count += 1
        if(count % 2 != 0):
            self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</div>")

    def add_section_data(self, section):
        self.add_increment_to_html("<div class=\"skill-section\">")
        self.append_to_html("<h4>" + section['title'] + "</h4>")
        self.add_increment_to_html("<ul class=\"skill-list\" >")
        for rating in section['ratings']:
            self.add_increment_to_html("<li class=\"skill-item\">")
            self.add_rating(rating)
            self.decrement_add_to_html("</li>")
        self.decrement_add_to_html("</ul>")
        self.decrement_add_to_html("</div>")

    def add_rating(self, rating):
        self.add_increment_to_html("<div class=\"row valign-wrapper\" >")
        self.add_increment_to_html("<div class=\"col s6\" >")
        self.append_to_html("<h5> " + rating['skill'] + " </h5>")
        self.decrement_add_to_html("</div>")
        self.add_increment_to_html("<div class=\"col s6 stars\" >")
        self.get_rating_level(float(rating['rating']))
        self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</div>")

    def get_rating_level(self, rating):
        full_stars = math.floor(rating / 1)
        half_stars = math.ceil(rating % 1)
        empty_stars = 5 - full_stars - half_stars
        self.get_stars(full_stars, "star")
        self.get_stars(half_stars, "star_half")
        self.get_stars(empty_stars, "star_border")

    def get_stars(self, number, icon):
        for i in range(number):
            self.append_to_html("<i class=\"small material-icons\">" + icon + "</i>")

    def add_projects(self, file):
        data = read_json_file(file)
        self.add_div_and_heading(data['title'], data['icon'])
        count = 0
        for project in data['projects']:
            if(count % 2 == 0):
                self.add_increment_to_html("<div class=\"row\">")
            self.add_increment_to_html("<div class=\"col m12 l6\">")
            self.create_card_for_project(project)
            self.decrement_add_to_html("</div>")
            if(count % 2 == 1):
                self.decrement_add_to_html("</div>")
            count += 1
        if(count % 2 != 0):
            self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</div>")

    def create_card_for_project(self, project):
        self.add_increment_to_html("<div class=\"card hoverable\">")
        self.add_increment_to_html("<div class=\"card-image waves-effect waves-block waves-light\">")
        self.append_to_html("<img class=\"activator\" src=\"img/office.jpg\">")
        self.decrement_add_to_html("</div>")
        self.add_increment_to_html("<div class=\"card-content\">")
        self.add_increment_to_html("<span class=\"card-title activator grey-text text-darken-4\">")
        self.append_to_html("<b>" + project['name'] + "</b><i class=\"material-icons right\">more_vert</i>")
        self.decrement_add_to_html("</span>")
        for tag in project['tags']:
            self.create_tag(tag)
        self.decrement_add_to_html("</div>")
        self.add_increment_to_html("<div class=\"card-action\">")
        self.add_footnotes(project['footnotes'])
        self.decrement_add_to_html("</div>")
        self.add_increment_to_html("<div class=\"card-reveal\">")
        self.append_to_html("<span class=\"card-title grey-text text-darken-4\"><b>" + project['name'] + "</b><i class=\"material-icons right\">close</i></span>")
        self.append_to_html("<p>" + project['description'] + "</p>")
        self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</div>")

    def create_tag(self, tag):
        self.add_increment_to_html("<div class=\"chip " + tag['type'].lower() + "\">")
        self.append_to_html(tag['tag'])
        self.decrement_add_to_html("</div>")

    def add_timeline(self, file):
        global html
        data = read_json_file(file)
        self.add_div_and_heading(data['title'], data['icon'])
        self.append_to_html("<p> " + data['description'] + " </p>")
        self.append_to_html("<div id=\"chart\"></div>")
        self.decrement_add_to_html("</div>")

    def add_div_and_heading(self, title, icon):
        self.headings.append(title)
        self.add_increment_to_html("<div id=\"" + title.lower() + "\" class=\"section scrollspy\">")
        self.append_to_html("<h2 class=\"section-heading\" >" + title + "<i class=\"material-icons heading-icon\" >" + icon + "</i></h2>")

    def add_footnotes(self, footnotes):
        self.add_increment_to_html("<div class=\"flex-list\">")
        self.add_increment_to_html("<ul>")
        for footnote in footnotes:
            self.append_to_html("<li>" + add_footnote(footnote) + "</li>")
        self.decrement_add_to_html("</ul>")
        self.decrement_add_to_html("</div>")

    def add_increment_to_html(self, text):
        self.append_to_html(text)
        self.indent_level += 1

    def decrement_add_to_html(self, text):
        self.indent_level -= 1
        self.append_to_html(text)

    def append_to_html(self, text):
        self.html += get_indentation(self.indent_level) + text

    def add_table_of_contents(self):
        self.add_increment_to_html("<div class=\"toc-wrapper\">")
        self.add_increment_to_html("<ul class=\"section table-of-contents\">")
        for heading in self.headings:
            heading_id = heading.replace(' ', '-').lower()
            self.append_to_html("<li><a href=\"#" + heading_id + "\">" + heading + "</a><li>")
        self.decrement_add_to_html("</ul>")
        self.decrement_add_to_html("</div>")


def get_indentation(indent_level):
    return "\n" + ("\t" * indent_level)


def write_to_file(text):
    file = open("index.html", 'w+')
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
    elif footnote['type'] == 'video':
        html += "play_circle_filled"
        text += get_link(footnote['video'])
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


webpage_generator()

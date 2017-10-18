import json
import time
import math
import dominate
from dominate.tags import *

class webpage_generator:
    html = ""
    body = ""
    content_div = ""
    indent_level = 0
    headings = []

    def __init__(self):
        self.generate_website()

    def generate_website(self):
        self.html += html()
        self.add_headers("data/headers.json")
        self.add_body()
        self.decrement_add_to_html("<html>")
        write_to_file(self.html)
        print(self.html)

    def add_headers(self, file):
        data = read_json_file(file)
        page_header = head()
        page_header.add(title(data['title']))
        page_header.add(meta(charset=data['charset']))
        for content_meta in data['content-metas']:
            page_header.add(meta(name=content_meta['name'], content=content_meta['content']))
        for import_link in data['links']:
            if import_link['type'] == 'css':
                page_header.add(link(href=import_link['source'], rel='stylesheet', type='text/css'))
            elif import_link['type'] == 'js':
                page_header.add(script(href=import_link['source'], type='text/javascript'))
            elif import_link['type'] == 'font':
                page_header.add(link(href=import_link['source'], rel='stylesheet'))
        self.html.add(page_header)

    def add_body(self):
        self.add_increment_to_html("<body>")
        self.body = body()
        self.body.add(div(div(_class="row"), _class="container"))
        self.add_body_content()
        self.add_increment_to_html("<div class=\"col hide-on-med-and-down l2\">")
        self.add_table_of_contents()
        self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</div>")
        self.decrement_add_to_html("</body>")

    def add_body_content(self):
        self.content_div = div(_class="col m12 l10")
        self.add_about_me("data/about-me.json")
        self.add_education("data/education.json")
        self.add_experience("data/experience.json")
        self.add_skills("data/skills.json")
        self.add_projects("data/projects.json")
        self.add_timeline("data/timeline.json")
        self.decrement_add_to_html("</div>")

    def add_about_me(self, file):
        data = read_json_file(file)
        about_me_div = div(id="about-me", _class="section scrollspy center-align")
        about_me_div.add(h1("Mohammad Ali Khan"))
        about_me_div.add(img(_class="responsive-img circle", src="img/" + data['picture'], alt="Picture of Ali"))
        about_me_div.add(br())
        about_me_div.add(self.get_social_media_icons(data['social-icons']))
        about_me_div.add(p(data['description'], _class="flow-text"))
        self.content_div.add(about_me_div)
        self.headings.append("About Me")

    def get_social_media_icons(self, icons):
        social_media_icons = div(_id="social-network-icons")
        for icon in icons:
            social_media_icons.add(self.get_social_icon(icon))
        return social_media_icons

    def get_social_icon(self, icon):
        return a(img(_class="responsive-img icon", src="img/" + icon['image'], alt=icon['name']), href=icon['link'])

    def add_education(self, file):
        data = read_json_file(file)
        education_div = self.get_div_and_heading(data['title'], data['icon'])
        education_div.add(self.get_educations_div(data['educations']))
        self.content_div.add(education_div)

    def get_div_and_heading(self, section_title, icon):
        section_div = div(id=section_title.lower(), _class="section scrollspy")
        section_div.add(h2(section_title,i(icon, _class="material-icons heading-icon"), _class="section-heading"))
        self.headings.append(section_title)
        return section_div
    
    def get_educations_div(self, educations):
        educations_div = div(_class="educations")
        for education in educations:
            educations_div.add(self.get_education_instance_div(education))
        return educations_div

    def get_education_instance_div(self, education):
        education_instance_div = div(_class="education-instance")
        education_instance_div.add(h3(education['education']))
        education_instance_div.add(h4(education['degree'] + " - " + education['grade']))
        education_instance_div.add(self.get_footnotes(education['footnotes']))

    def get_footnotes(self, footnotes):
        footnotes = div(_class="flext-list")
        footnote_list = ul()
        for footnote in footnotes:
            footnote_list.add(self.get_footnote(footnote))
        footnotes.add(footnote_list)

    def get_footnote(self, footnote):
        footnote_item = li()
        icon_type = ""
        text = ""
        if footnote['type'] == 'time':
            icon_type = "date_range"
            text = get_date(footnote['time'])
        elif footnote['type'] == 'location':
            icon_type = "place"
            text = get_location(footnote['location'])
        elif footnote['type'] == 'link':
            icon_type = "link"
            text = get_link(footnote['link'])
        elif footnote['type'] == 'code':
            icon_type = "code"
            text = get_link(footnote['code'])
        elif footnote['type'] == 'documentation':
            icon_type = "insert_drive_file"
            text = get_link(footnote['documentation'])
        elif footnote['type'] == 'video':
            icon_type = "play_circle_filled"
            text = get_link(footnote['video'])
        footnote_item.add(i(icon_type, _class="material-icons"))
        footnote_item.add(text)
        return footnote_item

    def get_date(self, date):
        start_date = time.strptime(date['start'], "%Y-%m-%d")
        text = time.strftime("%B %Y", start_date)
        if 'end' in date:
            end_date = time.strptime(date['end'], "%Y-%m-%d")
            text += " to " + time.strftime("%B %Y", end_date)
        return text

    def get_location(self, location):
        return location['city'] + ", " + location['country']

    def get_link(self, web_link):
        return a(web_link['title'], href=web_link['source'])

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
            if(count == 2):
                self.add_increment_to_html("<div class=\"col m12 l8 offset-l2\">")
            else:
                self.add_increment_to_html("<div class=\"col m12 l6\">")
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
        self.add_increment_to_html("<div class=\"col s6 left-align\" >")
        self.append_to_html("<h5> " + rating['skill'] + " </h5>")
        self.decrement_add_to_html("</div>")
        self.add_increment_to_html("<div class=\"col s6 stars centre-align\" >")
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
        self.append_to_html("<img class=\"activator\" src=\" " + project['image'] + " \">")
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

    def add_div_and_heading(self, section_title, icon):
        self.headings.append(section_title)
        self.add_increment_to_html("<div id=\"" + section_title.lower() + "\" class=\"section scrollspy\">")
        self.append_to_html("<h2 class=\"section-heading\" >" + section_title + "<i class=\"material-icons heading-icon\" >" + icon + "</i></h2>")

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

import json
import time
import math
import dominate
from dominate.tags import *

class webpage_generator:
    html = ""
    content_div = ""
    indent_level = 0
    headings = []

    def __init__(self):
        self.generate_website()

    def generate_website(self):
        self.html = html()
        self.add_headers("data/headers.json")
        self.add_body()
        write_to_file(self.html.render())
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
        page_body = body()
        container_row = div(_class="row")
        self.add_body_content()
        container_row.add(self.content_div)
        self.add_table_of_contents()
        container_row.add(self.toc_div)
        page_body.add(div(container_row, _class="container"))
        self.html.add(page_body)
        
    def add_body_content(self):
        self.content_div = div(_class="col m12 l10")
        self.add_about_me("data/about-me.json")
        self.add_education("data/education.json")
        self.add_experience("data/experience.json")
        self.add_skills("data/skills.json")
        self.add_projects("data/projects.json")
        self.add_timeline("data/timeline.json")
    
    def add_table_of_contents(self):
        self.toc_div = div(_class="col hide-on-med-and-down l2")
        self.toc_div.add(self.get_table_of_contents())

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
        return education_instance_div

    def get_footnotes(self, footnotes):
        footnotes_list_div = div(_class="flex-list")
        footnote_list = ul()
        for footnote in footnotes:
            footnote_list.add(self.get_footnote(footnote))
        footnotes_list_div.add(footnote_list)
        return footnotes_list_div

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
        experience_div = self.get_div_and_heading(data['title'], data['icon'])
        experience_div.add(self.get_experiences_div(data['experiences']))
        self.content_div.add(experience_div)

    def get_experiences_div(self, experiences):
        experiences_div = div(_class="experiences")
        count = 0
        for experience in experiences:
            count += 1
            experiences_div.add(self.get_experience_instance_div(experience))
            if(count != len(experiences)):
                experiences_div.add(div(_class="divider"))
        return experiences_div

    def get_experience_instance_div(self, experience):
        experience_instance_div = div(_class="experience-instance")
        experience_instance_div.add(h3(experience['company']))
        experience_instance_div.add(h4(experience['position']))
        experience_instance_div.add(self.get_footnotes(experience['footnotes']))
        return experience_instance_div

    def add_skills(self, file):
        data = read_json_file(file)
        skills_div = self.get_div_and_heading(data['title'], data['icon'])
        skills_div.add(self.get_skills_div(data['sections']))
        self.content_div.add(skills_div)

    def get_skills_div(self, sections):
        skills_div = div(_class="skills")
        count = 0
        skills_row = ""
        skills_column = ""
        for skills_section in sections:
            if(count % 2 == 0):
                skills_div.add(skills_row)
                skills_row = div(_class="row")
            if(count == 2):
                skills_column = div(_class="col m12 l8 offset-l2")
            else:
                skills_column = div(_class="col m12 l6")
            skills_column.add(self.get_skills_section_instance(skills_section))
            skills_row.add(skills_column)
            count += 1
        return skills_div

    def get_skills_section_instance(self, skill_section):
        skill_section_instance_div = div(_class="skill-section")
        skill_section_instance_div.add(h4(skill_section['title']))
        skill_section_instance_div.add(self.get_skills_section_skill_list(skill_section['ratings']))
        return skill_section_instance_div

    def get_skills_section_skill_list(self, ratings):
        skill_list = ul(_class="skill-list")
        for rating in ratings:
            skill_item = li(_class="skill-item")
            skill_item.add(self.get_skill_item(rating))
            skill_list.add(skill_item)
        return skill_list

    def get_skill_item(self, rating):
        skill_item_div = div(_class="row valign-wrapper")
        heading_column = div(_class="col s6 left-align")
        heading_column.add(h5(rating['skill']))
        skill_item_div.add(heading_column)
        rating_column = div(_class="col s6 starts centre-align")
        rating_column.add(self.get_rating(float(rating['rating'])))
        skill_item_div.add(rating_column)
        return skill_item_div

    def get_rating(self, rating):
        rating_div = div(_class="rating")
        full_stars = math.floor(rating / 1)
        half_stars = math.ceil(rating % 1)
        empty_stars = 5 - full_stars - half_stars
        rating_div.add(self.get_stars(full_stars, "star"))
        rating_div.add(self.get_stars(half_stars, "star_half"))
        rating_div.add(self.get_stars(empty_stars, "star_border"))
        return rating_div

    def get_stars(self, number, icon):
        stars_div = div(_class="stars")
        for index in range(number):
            stars_div += i(icon, _class="small material-icons")
        return stars_div

    def add_projects(self, file):
        data = read_json_file(file)
        project_div = self.get_div_and_heading(data['title'], data['icon'])
        project_div.add(self.get_projects(data['projects']))
        self.content_div.add(project_div)

    def get_projects(self, projects):
        projects_div = div(_class="projects")
        count = 0
        project_row = ""
        for project in projects:
            if(count % 2 == 0):
                projects_div.add(project_row)
                project_row = div(_class="row")
            project_column = div(_class="col m12 l6")
            project_column.add(self.get_project_card(project))
            project_row.add(project_column)
            count += 1 
        return projects_div

    def get_project_card(self, project):
        project_card = div(_class="card hoverable")
        project_card.add(self.get_card_activator(project['image']))
        project_card.add(self.get_card_content(project['name'], project['tags']))
        project_card.add(self.get_card_action(project['footnotes']))
        project_card.add(self.get_card_reveal(project['name'], project['description']))
        return project_card

    def get_card_activator(self, image):
        activator_div = div(_class="card-image waves-effect waves-block waves-light")
        activator_div.add(img(src=image, _class="activator"))
        return activator_div

    def get_card_content(self, name, tags):
        card_content_div = div(_class="card-content")
        card_content_div.add(self.get_card_title_span(name, "more_vert"))
        card_content_div.add(self.get_project_tags(tags))
        return card_content_div

    def get_card_title_span(self, name, icon):
        card_title_span = span(_class="card-title activator grey-text text-darken-4")
        card_title_span.add(b(name))
        card_title_span.add(i(icon,_class="material-icons right"))
        return card_title_span

    def get_project_tags(self, tags):
        project_tags_divs = div(_class="project-tags")
        for tag in tags:
            project_tags_divs.add(self.get_project_tag(tag))
        return project_tags_divs
    
    def get_project_tag(self, tag):
        return  div(tag['tag'], _class="chip " + tag['type'].lower())

    def get_card_action(self, footnotes):
        card_action_div = div(_class="card-action")
        card_action_div.add(self.get_footnotes(footnotes))
        return card_action_div

    def get_card_reveal(self, name, description):
        card_reveal_div = div(_class="card-reveal")
        card_reveal_div.add(self.get_card_title_span(name, "close"))
        card_reveal_div.add(p(description))
        return card_reveal_div

    def create_tag(self, tag):
        self.add_increment_to_html("<div class=\"chip " + tag['type'].lower() + "\">")
        self.append_to_html(tag['tag'])
        self.decrement_add_to_html("</div>")

    def add_timeline(self, file):
        data = read_json_file(file)
        timeline_div = self.get_div_and_heading(data['title'], data['icon'])
        timeline_div.add(p(data['description']))
        timeline_div.add(div(id="chart"))
        self.content_div.add(timeline_div)

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

    def get_table_of_contents(self):
        toc_div = div(_class="toc-wrapper")
        toc_div.add(self.get_toc_list(self.headings))
        return toc_div

    def get_toc_list(self, headings):
        toc_list = ul(_class="section table-of-contents")
        for heading in headings:
            toc_list.add(self.get_toc_item(heading))
        return toc_list
    
    def get_toc_item(self, heading):
        heading_id = self.get_heading_item_id(heading)
        return li(a(heading, href="#"+heading_id))

    def get_heading_item_id(self, heading):
        return heading.replace(' ', '-').lower()


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
    return a(link['title'], href=link['source'])


webpage_generator()

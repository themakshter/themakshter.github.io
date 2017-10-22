import json
import time
import math
import dominate
from dominate.tags import *
from abc import ABCMeta, abstractmethod

class HtmlWidget:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_html(self): pass

class WebpageGenerator:
    headings = []

    def __init__(self):
        self.generate_website()

    def generate_website(self):
        with html() as page_html:
            self.get_headers("data/headers.json")
            self.get_body()
        write_to_file(page_html.render())
        print(page_html)

    def get_headers(self, file):
        header_data = read_json_file(file)
        with head() as page_header:
            title(header_data['title'])
            meta(charset=header_data['charset'])
            for content_meta in header_data['content-metas']:
                meta(name=content_meta['name'], content=content_meta['content'])
            for import_link in header_data['links']:
                if import_link['type'] == 'css':
                    link(href=import_link['source'], rel='stylesheet', type='text/css')
                elif import_link['type'] == 'js':
                    script(src=import_link['source'], type='text/javascript')
                elif import_link['type'] == 'font':
                    link(href=import_link['source'], rel='stylesheet')
        return page_header

    def get_body(self):
        container = div(_class="container")
        with container.add(div(_class="row")):
            self.get_body_content()
            self.get_table_of_contents()
        return body(container)

    def get_body_content(self):
        with div(_class="col m12 l10") as content_div:
            self.get_about_me("data/about-me.json")
            self.get_education("data/education.json")
            self.get_experience("data/experience.json")
            self.get_skills("data/skills.json")
            self.get_projects_section("data/projects.json")
            self.get_timeline("data/timeline.json")
        return content_div

    def get_table_of_contents(self):
        toc_div = div(_class="col hide-on-med-and-down l2")
        toc_div.add(self.get_table_of_contents_wrapper())
        return toc_div

    def get_about_me(self, file):
        about_me_data = read_json_file(file)
        with div(id="about-me", _class="section scrollspy center-align") as about_me_div:
            h1("Mohammad Ali Khan")
            img(_class="responsive-img circle", src="img/" + about_me_data['picture'], alt="Picture of Ali")
            br()
            self.get_social_media_icons(about_me_data['social-icons'])
            p(about_me_data['description'], _class="flow-text")
        self.headings.append("About Me")
        return about_me_div

    def get_social_media_icons(self, icons):
        with div(_id="social-network-icons") as social_media_icons:
            for icon in icons:
                social_media_icons.add(self.get_social_icon(icon))
        return social_media_icons

    def get_social_icon(self, icon):
        return a(img(_class="responsive-img icon", src="img/" + icon['image'], alt=icon['name']), href=icon['link'])

    def get_education(self, file):
        data = read_json_file(file)
        education_div = self.get_div_and_heading(data['title'], data['icon'])
        education_div.add(self.get_educations_div(data['educations']))
        return education_div

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
        with div(_class="education-instance") as education_instance_div:
            h3(education['education'])
            h4(education['degree'] + " - " + education['grade'])
            self.get_footnotes(education['footnotes'])
        return education_instance_div

    def get_footnotes(self, footnotes):
        with div(_class="flex-list") as footnotes_list_div:
            with ul():
                for footnote in footnotes:
                    self.get_footnote(footnote)
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

    def get_experience(self, file):
        data = read_json_file(file)
        experience_div = self.get_div_and_heading(data['title'], data['icon'])
        experience_div.add(self.get_experiences_div(data['experiences']))
        return experience_div

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
        with div(_class="experience-instance") as experience_instance_div:
            h3(experience['company'])
            h4(experience['position'])
            self.get_footnotes(experience['footnotes'])
        return experience_instance_div

    def get_skills(self, file):
        data = read_json_file(file)
        skills_div = self.get_div_and_heading(data['title'], data['icon'])
        skills_div.add(self.get_skills_div(data['sections']))
        return skills_div

    def get_skills_div(self, sections):
        skills_div = div(_class="skills")
        count = 0
        skills_row = ""
        skills_column = ""
        for skills_section in sections:
            if(count % 2 == 0):
                skills_row = div(_class="row")
            if(count == 2):
                skills_column = div(_class="col m12 l8 offset-l2")
            else:
                skills_column = div(_class="col m12 l6")
            skills_column.add(self.get_skills_section_instance(skills_section))
            skills_row.add(skills_column)
            if(count % 2 == 0):
                skills_div.add(skills_row)
            count += 1
        return skills_div

    def get_skills_section_instance(self, skill_section):
        with div(_class="skill-section") as skill_section_instance_div:
            h4(skill_section['title'])
            self.get_skills_section_skill_list(skill_section['ratings'])
        return skill_section_instance_div

    def get_skills_section_skill_list(self, ratings):
        with ul(_class="skill-list") as skill_list:
            for rating in ratings:
                with li(_class="skill-item"):
                    self.get_skill_item(rating)
        return skill_list

    def get_skill_item(self, rating):
        with div(_class="row valign-wrapper") as skill_item_div:
            with div(_class="col s6 skills left-align"):
                h5(rating['skill'])
            with div(_class="col s6 ratings centre-align"):
                self.get_rating(float(rating['rating']))
        return skill_item_div

    def get_rating(self, rating):
        full_stars = math.floor(rating / 1)
        half_stars = math.ceil(rating % 1)
        empty_stars = 5 - full_stars - half_stars
        with div(_class="rating") as rating_div:
            self.get_stars(full_stars, "star")
            self.get_stars(half_stars, "star_half")
            self.get_stars(empty_stars, "star_border")
        return rating_div

    def get_stars(self, number, icon):
        stars_div = div(_class="stars")
        for index in range(number):
            stars_div += i(icon, _class="small material-icons")
        return stars_div

    def get_projects_section(self, file):
        data = read_json_file(file)
        project_div = self.get_div_and_heading(data['title'], data['icon'])
        project_div.add(self.get_projects(data['projects']))
        return project_div

    def get_projects(self, projects):
        projects_div = div(_class="projects")
        count = 0
        project_row = ""
        for project in projects:
            if(count % 2 == 0):
                project_row = div(_class="row")
            project_column = div(_class="col m12 l6")
            project_column.add(self.get_project_card(project))
            project_row.add(project_column)
            if(count % 2 == 0):
                projects_div.add(project_row)
            count += 1
        return projects_div

    def get_project_card(self, project):
        with div(_class="card hoverable") as project_card:
            self.get_card_activator(project['image'])
            self.get_card_content(project['name'], project['tags'])
            self.get_card_action(project['footnotes'])
            self.get_card_reveal(project['name'], project['description'])
        return project_card

    def get_card_activator(self, image):
        activator_div = div(_class="card-image waves-effect waves-block waves-light")
        activator_div.add(img(src=image, _class="activator"))
        return activator_div

    def get_card_content(self, name, tags):
        with div(_class="card-content") as card_content_div:
            self.get_card_title_span(name, "more_vert")
            self.get_project_tags(tags)
        return card_content_div

    def get_card_title_span(self, name, icon):
        with span(_class="card-title activator grey-text text-darken-4") as card_title_span:
            b(name)
            i(icon,_class="material-icons right")
        return card_title_span

    def get_project_tags(self, tags):
        with div(_class="project-tags") as project_tags_divs:
            for tag in tags:
                self.get_project_tag(tag)
        return project_tags_divs

    def get_project_tag(self, tag):
        return  div(tag['tag'], _class="chip " + tag['type'].lower())

    def get_card_action(self, footnotes):
        card_action_div = div(_class="card-action")
        card_action_div.add(self.get_footnotes(footnotes))
        return card_action_div

    def get_card_reveal(self, name, description):
        with div(_class="card-reveal") as card_reveal_div:
            self.get_card_title_span(name, "close")
            p(description)
        return card_reveal_div

    def get_timeline(self, file):
        data = read_json_file(file)
        timeline_div = self.get_div_and_heading(data['title'], data['icon'])
        timeline_div.add(p(data['description']))
        timeline_div.add(div(id="chart"))
        return timeline_div

    def get_table_of_contents_wrapper(self):
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

def write_to_file(text):
    file = open("index.html", 'w+')
    file.write(text)

def get_meta_tag(name, content):
    return "<meta name\"" + name + "\" content=\"" + content + "\" />"

def read_json_file(filename):
    return json.loads(open(filename).read())

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


class ProjectCard(HtmlWidget):

    def __init__(self, project):
        self.project = project

    def get_html(self):
        return self.__get_project_card(self.project)

    def __get_project_card(self, project):
        with div(_class="card hoverable") as project_card:
            self.__get_card_activator(project['image'])
            self.__get_card_content(project['name'], project['tags'])
            self.__get_card_action(project['footnotes'])
            self.__get_card_reveal(project['name'], project['description'])
        return project_card

    def __get_card_activator(self, image):
        activator_div = div(_class="card-image waves-effect waves-block waves-light")
        activator_div.add(img(src=image, _class="activator"))
        return activator_div

    def __get_card_content(self, name, tags):
        with div(_class="card-content") as card_content_div:
            self.__get_card_title_span(name, "more_vert")
            self.__get_project_tags(tags)
        return card_content_div

    def __get_card_title_span(self, name, icon):
        with span(_class="card-title activator grey-text text-darken-4") as card_title_span:
            b(name)
            i(icon, _class="material-icons right")
        return card_title_span

    def __get_project_tags(self, tags):
        with div(_class="project-tags") as project_tags_divs:
            for tag in tags:
                self.__get_project_tag(tag)
        return project_tags_divs

    def __get_project_tag(self, tag):
        return  div(tag['tag'], _class="chip " + tag['type'].lower())

    def __get_card_action(self, footnotes):
        card_action_div = div(_class="card-action")
        card_action_div.add(self.get_footnotes(footnotes))
        return card_action_div

    def __get_card_reveal(self, name, description):
        with div(_class="card-reveal") as card_reveal_div:
            self.__get_card_title_span(name, "close")
            p(description)
        return card_reveal_div

class Footnotes(HtmlWidget):

    def __init__(self, footnotes):
        self.footnotes = footnotes

    def get_html(self):
        return self.__get_footnotes(self.footnotes)

    def __get_footnotes(self, footnotes):
        with div(_class="flex-list") as footnotes_list_div:
            with ul():
                for footnote in footnotes:
                    self.__get_footnote(footnote)
        return footnotes_list_div

    def __get_footnote(self, footnote):
        footnote_item = li()
        footnote_item.add(self.__get_footnote_icon(footnote['type']))
        footnote_item.add(self.__get_footnote_text(footnote))
        return footnote_item

    def __get_footnote_icon(self, footnote_type):
        icons = {
            'time' : "date_range",
            'location' : "place",
            'link' : "link",
            'code' : "code",
            'documentation' : "insert_drive_file",
            'video' : "play_circle_filled"
        }
        return i(icons[footnote_type], _class="material-icons")

    def __get_footnote_text(self, footnote):
        if footnote['type'] == 'time':
            return  get_date(footnote['time'])
        elif footnote['type'] == 'location':
            return  get_location(footnote['location'])
        else:
            return  get_link(footnote[footnote['type']])

WebpageGenerator()

import datetime
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from dataclasses import dataclass

from info_hider import info_hider

PATH_TO_TEMPLATES = Path('TEMPLATES/')
PATH_TO_RESOURCES = Path('../generator/RESOURCES/')
PATH_TO_OUTPUT = Path('../docs/')
URL_ROOT = "https://cz-manufacturing.org/"

link_to_homepage = "/"  # TODO: always / in production
html_file_suffix = ".html"


@dataclass()
class Page(object):
    title: str
    name: str
    keywords: str
    description: str
    content_file: str
    url: str
    language: str
    last_mod: datetime.datetime
    phone = info_hider("+420 777 256 077")  # TODO: Change
    email = info_hider("jaros@cz-manufacturing.org")  # TODO: Change
    address = info_hider("Kaprova 42/14, Prague, Czechia")  # TODO: Change

    def keys(self):
        """Get keys that allows conversion of this class to dictionary.

        Returns:
            List[str]: List of the keys to be passed to template.
        """
        return ['title', 'keywords', 'description', 'url', 'content_file',
                'language', 'email', 'phone', 'address', 'name']

    def __getitem__(self, key):
        """Allows conversion of this class to dictionary.
        """
        return getattr(self, key)

    def generate_site(self):
        with open(PATH_TO_TEMPLATES.joinpath('page.html')) as tem_han:
            template = Environment(
                loader=FileSystemLoader(PATH_TO_TEMPLATES)
            ).from_string(tem_han.read())
            html_str = template.render(
                **dict(self),
                link_to_homepage=link_to_homepage
            )
            return html_str

    @property
    def absolute_url(self):
        if self.url != 'index':
            return URL_ROOT + self.url + html_file_suffix
        return URL_ROOT

    @property
    def last_modified(self):
        if self.last_mod is None:
            return None
        return self.last_mod.strftime('%Y-%m-%d')


pages = [
    Page(title="CZ Manufacturing: Industrial solutions",
         name="Industrial solutions",
         keywords="automation, machine vision, production",  # noqa: E501
         description="We can help you with the automation of processes in your factory. Increase your production and cost efficiency with a lite help from our team of experts.",  # noqa: E501
         url="index",
         content_file='page_home.html',
         language="en",
         last_mod=datetime.datetime(2026, 12, 6)
         ),
    Page(title="CZ Manufacturing: About us",
         name="About CZ Manufacturing",
         keywords="industrial automation, process monitoring, machine vision, manufacturing efficiency, industrial software",  # noqa: E501
         description="CZ Manufacturing delivers automation and monitoring solutions with 20 plus years of experience, helping plants boost efficiency, reliability, and control.",  # noqa: E501
         url="about",
         content_file='page_about.html',
         language="en",
         last_mod=datetime.datetime(2026, 12, 6)
         ),
    Page(title="CZ Manufacturing: Services",
         name="Our Services",
         keywords="industrial automation, process monitoring, production analytics, smart manufacturing, industrial control systems",  # noqa: E501
         description="CZ Manufacturing provides industrial automation, monitoring, and analytics services that improve production efficiency, reliability, real-time process control.",  # noqa: E501
         url="services",
         content_file='page_services.html',
         language="en",
         last_mod=datetime.datetime(2026, 12, 6)
         ),
    Page(title="CZ Manufacturing: Contact",
         name="Contact Information",
         keywords="industrial automation, manufacturing services, process optimization, industrial monitoring, automation consulting",  # noqa: E501
         description="Contact CZ Manufacturing to discuss industrial automation, monitoring, and optimization solutions tailored to your plant and production goals worldwide today.",  # noqa: E501
         url="contact",
         content_file='page_contact.html',
         language="en",
         last_mod=datetime.datetime(2026, 12, 6)
         ),
    Page(title="CZ Manufacturing: How we meet standards",
         name="How We Meet Standards",
         keywords="quality management, industrial standards, system reliability, testing and validation, process documentation",  # noqa: E501
         description="How CZ Manufacturing meets industrial standards through quality management, validation, safety, cybersecurity, documentation, and continuous improvement.",  # noqa: E501
         url="how-we-meet-standards",
         content_file='page_how_we_meet_standards.html',
         language="en",
         last_mod=datetime.datetime(2026, 1, 26)
         ),
    Page(title="CZ Manufacturing: Industrial Automation and Smart Manufacturing Services",
         name="Industrial Automation and Smart Manufacturing Services",
         keywords="industrial automation, machine vision systems, production process optimization, industrial monitoring software, smart manufacturing solutions",  # noqa: E501
         description="Advanced industrial automation, machine vision, and monitoring solutions that improve efficiency, reduce costs, and optimize modern manufacturing processes.",  # noqa: E501
         url="smart-manufacturing-services",
         content_file='page_smart_manufacturing_services.html',
         language="en",
         last_mod=datetime.datetime(2026, 2, 7)
         )
]

# Remove all existing resources
if PATH_TO_OUTPUT.exists():
    shutil.rmtree(PATH_TO_OUTPUT)

# Create new dir
PATH_TO_OUTPUT.mkdir()

for page in pages:
    content = page.generate_site()
    with PATH_TO_OUTPUT.joinpath(page.url + html_file_suffix).open('w') as fp:
        fp.write(content)

# Copy resources
shutil.copytree(PATH_TO_RESOURCES, PATH_TO_OUTPUT, dirs_exist_ok=True)

# Generate resource map:
with open(PATH_TO_TEMPLATES.joinpath('site_map.xml')) as tem_han:
    template = Environment(
        loader=FileSystemLoader(PATH_TO_TEMPLATES)
    ).from_string(tem_han.read())
    html_str = template.render(
        sites=pages
    )
    with PATH_TO_OUTPUT.joinpath('sitemap.xml').open('w') as f_xml:
        f_xml.write(html_str)

robots_txt_content = f"""User-agent: *
Allow: /
Sitemap: {URL_ROOT}sitemap.xml"""
with PATH_TO_OUTPUT.joinpath('robots.txt').open('w') as robots_txt_h:
    robots_txt_h.write(robots_txt_content)

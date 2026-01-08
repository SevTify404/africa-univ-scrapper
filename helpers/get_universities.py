from selectolax.parser import HTMLParser
from aiohttp import ClientSession
from config import Config
from DirtUniversity import DirtUniversity

def clean_unprocessable_univs(universities: list[DirtUniversity]) -> list[DirtUniversity]:
    cleaned_univs = []
    for univ in universities:
        if univ.wikipdia_link not in ['#', '', None]:
            cleaned_univs.append(univ)
    return cleaned_univs


async def get_african_universities(session: ClientSession) -> list[DirtUniversity]:

    BASE_URL = Config.UNIVERSITY_PAGE_TO_SCRAP_LINK

    universities: list[DirtUniversity] = []

    async with session.get(BASE_URL) as response:
        html_content = await response.text()

    tree = HTMLParser(html_content)

    all_countries = tree.css("div.question")
    for country_div in all_countries:
        country_name = country_div.css_first("div.title").text(strip=True)

        university_list = country_div.css("div.answer ul")
        if not university_list:
            university_list = country_div.css("div.answer li")

        for univ in university_list:
            univ_name = univ.text(strip=True)
            wikipedia_link = univ.css_first("a").attributes.get("href", "")
            universities.append(
                DirtUniversity(name=univ_name, country=country_name, wikipdia_link=wikipedia_link)
            )

    return clean_unprocessable_univs(universities)
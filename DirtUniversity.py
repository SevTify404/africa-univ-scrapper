from dataclasses import dataclass

import aiohttp

from helpers.fetch_university_info import fetch_university_info
@dataclass
class GoodUniversity:
    name: str
    country: str
    create_date: str
    website_link: str

    def __str__(self):
        return f"{self.name} - {self.country} - {self.create_date} - {self.website_link}"

@dataclass
class DirtUniversity:
    name: str
    country: str
    wikipdia_link: str

    def get_wikipedia_page_name(self) -> str:
        if self.wikipdia_link == "#":
            return ""
        return self.wikipdia_link.split("/")[-1]

    async def get_full_info(self, session: aiohttp.ClientSession) -> GoodUniversity:
        print("Récupération des infos pour: ", self.name)
        info = await fetch_university_info(self.get_wikipedia_page_name(), session)
        if not info:
            return GoodUniversity(
                name=self.name,
                country=self.country,
                create_date="Introuvable",
                website_link="Introuvable"
            )
        return GoodUniversity(
            name=self.name,
            country=self.country,
            create_date=info[0],
            website_link=info[1]
        )

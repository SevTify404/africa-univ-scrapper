from dataclasses import dataclass


@dataclass
class University:
    name: str
    country: str
    wikipdia_link: str

    def get_wikipedia_name(self) -> str:
        return self.wikipdia_link.split("/")[-1]
    

class Config:
    CUSTOM_HEADERS: dict[str, str] = {
        "Content-Type": "text/html",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36"
    }

    WIKIDATA_API_URL: str = "https://www.wikidata.org/wiki/Special:EntityData/{page_id}.json"

    WIKIPEDIA_API_LINK: str = "https://en.wikipedia.org/w/api.php"

    UNIVERSITY_PAGE_TO_SCRAP_LINK: str = "https://aau.org/membership-list/#"
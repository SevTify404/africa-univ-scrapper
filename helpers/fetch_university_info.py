import aiohttp
from config import Config
async def get_wikidata_id(session: aiohttp.ClientSession, page_title: str) -> str | None:

    params = {
        "action": "query",
        "prop": "pageprops",
        "format": "json",
        "titles": page_title
    }

    async with session.get(Config.WIKIPEDIA_API_LINK, params=params, headers=Config.CUSTOM_HEADERS) as response:
        data = await response.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            pageprops = page_data.get("pageprops", {})
            wikidata_id = pageprops.get("wikibase_item")
            return wikidata_id
    return None


def find_web_site_url(claims: dict, wikidata_id: str) -> str | None:
    PROPRIETE_WIKIDATA = "P856"
    try:
        return claims['entities'][wikidata_id]['claims'][PROPRIETE_WIKIDATA][0]["mainsnak"]["datavalue"]["value"]
    except (KeyError, IndexError):
        return None

def format_p571_data(p571_node: dict[str, str | int]) -> str | None:
    if not p571_node:
        return None

    time_str = p571_node["time"].lstrip("+")
    precision = p571_node["precision"]

    year = time_str[0:4]
    month = time_str[5:7]
    day = time_str[8:10]

    if precision >= 11:
        return f"{year}-{month}-{day}"
    elif precision == 10:
        return f"{year}-{month}"
    elif precision == 9:
        return year
    elif precision == 8:
        return f"{year}s"
    else:
        return year

def find_creation_date(claims: dict, wikidata_id: str) -> str | None:
    PROPRIETE_WIKIDATA = "P571"
    try:
        date_node = claims['entities'][wikidata_id]['claims'][PROPRIETE_WIKIDATA][0]["mainsnak"]["datavalue"]["value"]
        formatted_date = format_p571_data(date_node)
        if formatted_date:
            return formatted_date
        # Fallback
        date_value = date_node["time"]
        return date_value.lstrip("+").split("T")[0]
    except (KeyError, IndexError):
        return None


async def get_wikiidata_content(session: aiohttp.ClientSession, wikisata_id: str) -> dict[str, str]:
    async with session.get(Config.WIKIDATA_API_URL.format(page_id=wikisata_id), headers=Config.CUSTOM_HEADERS) as response:
        try:
            if response.status != 200:
                return {}
            return await response.json()
        except Exception as e:
            print("Erreur lors de la récupération du contenu Wikidata: ", e.__class__.__name__)
            return {}



async def fetch_university_info(wikipedia_page_name: str, session: aiohttp.ClientSession) -> tuple[str, str | None] | None:
    """Ordre : Date de création et ensuite site web"""
    if not wikipedia_page_name:
        return None

    wikidata_id = await get_wikidata_id(session, wikipedia_page_name)
    if not wikidata_id:
        return None

    wikidata_content = await get_wikiidata_content(session, wikidata_id)

    date_value = find_creation_date(wikidata_content, wikidata_id) or "Introuvable"
    web_site_url = find_web_site_url(wikidata_content, wikidata_id) or "Introuvable"

    return date_value, web_site_url
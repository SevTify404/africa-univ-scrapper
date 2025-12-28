import asyncio
import csv
import time

import aiohttp
from DirtUniversity import GoodUniversity
from config import Config
from helpers.get_universities import get_african_universities
async def main():
    start_time = time.time()
    print("Recuperation des nom des universités africaines...")
    async with aiohttp.ClientSession(headers=Config.CUSTOM_HEADERS) as session:
        univs = await get_african_universities(session)
        end_get_names_time = time.time()
        print(f"Universités total trouvé: {len(univs)}")

        final_univs: list[GoodUniversity] = []
        # Requetes par batch de 30 universités pour optimisé

        print("Debut de la récuperation des sites et date de création...")
        batch_size = 40
        for i in range(0, len(univs), batch_size):
            batch = univs[i:i + batch_size]
            tasks = [univ.get_full_info(session) for univ in batch]
            full_info_univs = await asyncio.gather(*tasks, return_exceptions=True)
            full_info_univs = [u for u in full_info_univs if isinstance(u, GoodUniversity)]
            final_univs.extend(full_info_univs)
        end_get_info_time = time.time()

        print(f"Temps pour récupérer les noms: {end_get_names_time - start_time:.2f} secondes")

        print(f"Temps pour récupérer les infos: {end_get_info_time - end_get_names_time:.2f} secondes")


    print("Récuperation terminé, exportation vers CSV..")
    # Export brut vers csv
    with open("universites.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["nom", "pays", "date_creation", "site_web"])

        for univ in final_univs:
            writer.writerow([univ.name, univ.country, univ.create_date, univ.website_link])

    print("C'est terminé, tout est dans universites.csv")

asyncio.run(main())




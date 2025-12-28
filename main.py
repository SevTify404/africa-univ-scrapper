import asyncio

from DirtUniversity import GoodUniversity
from helpers.get_universities import get_african_universities
async def main():
    univs = await get_african_universities()
    print(f"Universités total trouvé: {len(univs)}")

    final_univs: list[GoodUniversity] = []
    # Requetes par batch de 10 universités pour optimisé

    print("Debut de la récuperation des sites et date de création...")
    batch_size = 10
    for i in range(0, len(univs), batch_size):
        batch = univs[i:i + batch_size]
        tasks = [univ.get_full_info() for univ in batch]
        full_info_univs = await asyncio.gather(*tasks)
        final_univs.extend(full_info_univs)

    print("Récuperation terminé ")
    # Export brut vers csv
    with open(f"universites.csv", "w") as file:
        file.write("nom,pays,date_creation,site_web\n")
        for univ in final_univs:
            file.write(f'"{univ.name}","{univ.country}","{univ.create_date}","{univ.website_link}"\n')

    print("C'est terminé, tout est dans universites.csv")

asyncio.run(main())




import requests
import pathlib
from tqdm import tqdm


def print_if_not_empty(target_list, print_string):
    if len(target_list) > 0:
        print(print_string)
        for element in target_list:
            print(element)


if __name__ == "__main__":
    wikipedia_link_fmt = "https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_{}_-_Série_A"
    target_years = list(range(2008, 2024))

    target_dir = pathlib.Path("../data/html/coaches_fired")
    target_dir.mkdir(parents=True, exist_ok=True)

    request_errors = list()
    couldnt_find_coaches_changes_table = list()
    for year in tqdm(target_years, desc="requests feitos"):
        target_link = wikipedia_link_fmt.format(year)
        response = requests.get(target_link)

        if response.status_code != 200:
            request_errors.append(target_link)
            continue

        html = response.content

        target_file_path = target_dir / f"campeonato_{year}.html"
        print(f"Escrevendo {target_file_path}")
        with open(target_file_path, 'wb') as target_file:
            target_file.write(html)

    print_if_not_empty(request_errors, "Erros de request nos links:")

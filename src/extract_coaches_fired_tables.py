from bs4 import BeautifulSoup, Tag
import utils
import config
from tqdm import tqdm

if __name__ == "__main__":

    target_htmls = sorted(
        list(config.COACHES_FIRED_WIKIS_DOWNLOAD_DIR_PATH.glob("*.html")))

    config.COACHES_FIRED_WIKIS_TABLE_DIR_PATH.mkdir(parents=True,
                                                    exist_ok=True)

    couldnt_find_coaches_changes_span = list()
    couldnt_find_coaches_changes_table = list()

    for html_file_path in tqdm(target_htmls, desc="Extracting html tables from html files"):
        with open(html_file_path) as target_file:
            soup = BeautifulSoup(target_file, 'html.parser')

        year = int(str(html_file_path).split("_")[-1].split(".")[-2])

        tag_list = soup.find_all(
            "span", id=["Mudança_de_técnicos", "Mudanças_de_técnicos"])
        if len(tag_list) == 0:
            couldnt_find_coaches_changes_span.append(str(html_file_path))
            continue

        target_span = tag_list[0]
        h2_parent = target_span.parent
        target_table: Tag = h2_parent.next_sibling.next_sibling
        if target_table.name != "table":
            couldnt_find_coaches_changes_table.append(str(html_file_path))
            continue

        target_table_file = config.COACHES_FIRED_WIKIS_TABLE_PATH_FMT.format(
            year)
        with open(target_table_file, "w") as table_file:
            table_file.write(str(target_table))

    utils.print_if_not_empty(couldnt_find_coaches_changes_span,
                             "Erros de encontrar span alvo:")
    utils.print_if_not_empty(couldnt_find_coaches_changes_table,
                             "Erros de encontrar tabela alvo:")

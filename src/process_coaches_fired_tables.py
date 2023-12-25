from bs4 import BeautifulSoup, NavigableString
import config
from tqdm import tqdm
import pandas as pd


def get_headers_dict(soup: BeautifulSoup):
    headers = soup.find_all("th")
    headers_order_dict = dict()
    curr_header_idx = 0
    for header in headers:
        for descendant in header.descendants:
            if isinstance(descendant, NavigableString):
                curr_str = str(descendant.string).strip()
                if curr_str not in ["\n", None, ""]:
                    headers_order_dict[curr_header_idx] = curr_str
                    curr_header_idx += 1

    return headers_order_dict


def extract_data_from_table_as_dict(soup: BeautifulSoup,
                                    headers_order_dict: dict):
    headers = list(headers_order_dict.values())
    table_dict = {key: list() for key in headers}
    table_rows = soup.find_all("tr")
    #Ignore header row
    for row in table_rows[1:]:
        curr_row_data_dict = {key: None for key in headers}
        table_data = row.find_all("td")
        for data_idx, data in enumerate(table_data):
            final_str = ""
            for descendant in data.descendants:
                if isinstance(descendant, NavigableString):
                    curr_str = str(descendant.string).strip().strip("\n")
                    final_str += " " + curr_str

            curr_row_data_dict[
                headers_order_dict[data_idx]] = final_str.strip()

        for key, value in curr_row_data_dict.items():
            if value is None:
                curr_row_data_dict[key] = ""

            table_dict[key].append(value if value is not None else "")

    return table_dict


if __name__ == "__main__":

    config.COACHES_FIRED_CSV_TABLE_DIR_PATH.mkdir(parents=True, exist_ok=True)
    tables_htmls_paths = sorted(
        list(config.COACHES_FIRED_WIKIS_TABLE_DIR_PATH.glob("*.html")))

    for table_html_path in tqdm(tables_htmls_paths):
        with open(table_html_path) as target_file:
            soup = BeautifulSoup(target_file, 'html.parser')

        year = int(str(table_html_path).split("_")[-1].split(".")[-2])
        headers_order_dict = get_headers_dict(soup)

        table_dict = extract_data_from_table_as_dict(soup, headers_order_dict)

        table_df = pd.DataFrame.from_dict(table_dict)
        table_df.to_csv(config.COACHES_FIRED_CSV_TABLE_PATH_FMT.format(year),
                        index=False)

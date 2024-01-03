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

    rowspan_cache_data = dict()
    #Ignore header row
    for row in table_rows[1:]:
        curr_row_data_dict = {key: None for key in headers}
        table_data = row.find_all("td")

        data_idx_offset = 0
        for header_n, header_val in headers_order_dict.items():
            # Check if there is rowspanned data for current col
            cached_data = rowspan_cache_data.get(header_val, None)
            if cached_data is not None:
                # There is rowspanned data for this col
                data_to_save = cached_data[0]
                cached_data_n = cached_data[1]
                data_idx_offset += 1
                new_cached_data_n = cached_data_n - 1
                if new_cached_data_n > 0:
                    rowspan_cache_data[header_val] = [
                        data_to_save, new_cached_data_n
                    ]
                else:
                    del rowspan_cache_data[header_val]

            else:
                data = table_data[header_n - data_idx_offset]
                final_str = ""
                for descendant in data.descendants:
                    if isinstance(descendant, NavigableString):
                        curr_str = str(descendant.string).strip(" \n")
                        final_str += " " + curr_str
                data_to_save = final_str.strip()

                row_span_curr_data = int(data.get("rowspan", 1))
                if row_span_curr_data > 1:
                    rowspan_cache_data[header_val] = [
                        data_to_save, row_span_curr_data - 1
                    ]

            curr_row_data_dict[header_val] = data_to_save

        for key, value in curr_row_data_dict.items():
            if value is None:
                curr_row_data_dict[key] = ""

            table_dict[key].append(curr_row_data_dict[key])

    return table_dict


if __name__ == "__main__":

    config.COACHES_FIRED_CSV_TABLE_DIR_PATH.mkdir(parents=True, exist_ok=True)
    tables_htmls_paths = sorted(
        list(config.COACHES_FIRED_WIKIS_TABLE_DIR_PATH.glob("*.html")))

    for table_html_path in tqdm(tables_htmls_paths, desc="Creating csv files from html tables"):
        with open(table_html_path) as target_file:
            soup = BeautifulSoup(target_file, 'html.parser')

        year = int(str(table_html_path).split("_")[-1].split(".")[-2])
        headers_order_dict = get_headers_dict(soup)

        table_dict = extract_data_from_table_as_dict(soup, headers_order_dict)

        table_df = pd.DataFrame.from_dict(table_dict)
        assert table_df.isna().sum().sum() == 0
        table_df.to_csv(config.COACHES_FIRED_CSV_TABLE_PATH_FMT.format(year),
                        index=False)

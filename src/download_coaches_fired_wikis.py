import requests
from tqdm import tqdm
from utils import print_if_not_empty
import config

if __name__ == "__main__":
    config.COACHES_FIRED_WIKIS_DOWNLOAD_DIR_PATH.mkdir(parents=True, exist_ok=True)

    request_errors = list()
    for year in tqdm(config.TARGET_YEARS, desc="Downloading target htmls"):
        target_link = config.COACHES_WIKI_LINK_FMT.format(year)
        response = requests.get(target_link)

        if response.status_code != 200:
            request_errors.append(target_link)
            continue

        html = response.content

        target_file_path = config.COACHES_FIRED_WIKIS_DOWNLOAD_PATH_FMT.format(year)
        with open(target_file_path, 'wb') as target_file:
            target_file.write(html)

    print_if_not_empty(request_errors, "Erros de request nos links:")

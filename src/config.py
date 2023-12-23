import pathlib

TARGET_YEARS = list(range(2008, 2024))
COACHES_WIKI_LINK_FMT = "https://pt.wikipedia.org/wiki/Campeonato_Brasileiro_de_Futebol_de_{}_-_Série_A"

COACHES_FIRED_WIKIS_DOWNLOAD_DIR_PATH = pathlib.Path(
    "../data/html/coaches_fired")
COACHES_FIRED_WIKIS_DOWNLOAD_PATH_FMT = str(
    COACHES_FIRED_WIKIS_DOWNLOAD_DIR_PATH) + "/campeonato_{}.html"

COACHES_FIRED_WIKIS_TABLE_DIR_PATH = pathlib.Path(
    "../data/html/coaches_fired_tables")
COACHES_FIRED_WIKIS_TABLE_PATH_FMT = str(
    COACHES_FIRED_WIKIS_TABLE_DIR_PATH) + "/campeonato_{}.html"

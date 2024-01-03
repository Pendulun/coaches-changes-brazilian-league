import config
from tqdm import tqdm
import pandas as pd
import re

month_to_number_map = {
    "Janeiro": 1,
    "Fevereiro": 2,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12
}

reason_to_english_map = {
    "Substituído": "Substituted",
    "Renunciado": "Resigned",
    "Resignado": "Resigned",
    "Contratado": "Changed team",
    "Despedido": "Fired",
    "Demitido": "Fired",
    "Remanejado": "Relocated",
    "Fim": "End of contract"
}


def remove_number_at_the_end(data: str) -> str:
    return " ".join(
        data.split(" ")[:-1]) if data.split(" ")[-1].isdigit() else data


def normalize_team_name(data: str) -> str:
    data = data.replace(" Mineiro", "-MG")
    data = data.replace(" Paranaense", "-PR")
    data = data.replace("Atlético-PR", "Athletico-PR")
    data = data.replace(" Goianiense", "-GO")
    data = data.replace(" da Gama", "")
    return data


def treat_2008_df(df: pd.DataFrame) -> pd.DataFrame:
    df["Saiu"] = df['Saiu'].apply(lambda x: x.replace("  ", " ").split())
    df['Antecessor'] = df["Saiu"].apply(lambda x: " ".join(x[0:-2]))
    df['Dia Saída'] = df['Saiu'].apply(lambda x: int(x[-2]))
    df['Mês Saída'] = df['Saiu'].apply(lambda x: month_to_number_map[x[-1]])

    df['Entrou'] = df['Entrou'].apply(lambda x: x.split(" "))
    df['Sucessor'] = df['Entrou'].apply(
        lambda x: remove_number_at_the_end(" ".join(x[0:-2]).strip()))
    df['Dia Entrada'] = df['Entrou'].apply(lambda x: int(x[-2]))
    df['Mês Entrada'] = df['Entrou'].apply(
        lambda x: month_to_number_map[x[-1]])

    df['Ano'] = 2008
    df.drop(['Saiu', 'Entrou'], axis=1, inplace=True)
    df['Clube'] = df['Clube'].apply(normalize_team_name)

    df.rename(
        {
            "Clube": 'Team',
            "Antecessor": 'Coach Out',
            "Dia Saída": "Day Out",
            "Mês Saída": "Month Out",
            "Sucessor": "Coach In",
            "Dia Entrada": "Day In",
            "Mês Entrada": "Month In",
            "Ano": "Year",
        },
        inplace=True,
        axis=1)

    df.sort_values(by=["Month Out", "Day Out"], inplace=True)
    df.reset_index(inplace=True, drop=True)
    return df


def remove_after_char(data: str, char: str) -> str:
    splited_data = data.split(char)
    if len(splited_data) > 1:
        return " ".join(splited_data[:-1])
    else:
        return splited_data[0]


def remove_final_ref(data: str) -> str:
    return remove_after_char(data, "[").strip()


def remove_final_parentesis(data: str) -> str:
    return remove_after_char(data, "(").strip()


def remove_before_comma(data: str) -> str:
    splited_data = data.replace(", ", ",").split(",")
    if len(splited_data) > 1:
        names_before_comma = splited_data[0].split(" ")
        names_after_comma = splited_data[1].split(" ")
        after_diff = len(names_after_comma) - len(names_before_comma)
        start_name = int(after_diff - (after_diff / 2))
        return " ".join(names_after_comma[start_name:])
    else:
        return splited_data[0]


def remove_anything_unwanted(data: str) -> str:
    treated_data = remove_number_at_the_end(data)
    treated_data = remove_final_ref(treated_data)
    treated_data = remove_final_parentesis(treated_data)
    treated_data = remove_before_comma(treated_data)
    return treated_data


def remove_non_numeric(data: str) -> str:
    return re.sub("[^0-9]", "", data)


def get_result_type(my_score: int, other_score: int) -> str:
    if my_score > other_score:
        return "Win"
    elif my_score < other_score:
        return "Lost"
    else:
        return "Draw"


def parse_last_match_result(row, target_index_cols):
    last_match_data = row['Última partida']
    team_name = row['Clube']
    splitted_last_match = last_match_data.split("–")
    home_team = " ".join(splitted_last_match[0].split(" ")[:-1])
    away_team = " ".join(splitted_last_match[1].split(" ")[1:])

    home_result = int(splitted_last_match[0].split(" ")[-1])
    away_result = int(splitted_last_match[1].split(" ")[-0])

    last_match_home = home_team == team_name
    if last_match_home:
        match_result = get_result_type(home_result, away_result)
        rival_name = away_team
        team_score = home_result
        rival_score = away_result
    else:
        match_result = get_result_type(away_result, home_result)
        rival_name = home_team
        team_score = away_result
        rival_score = home_result

    return pd.Series(
        [match_result, last_match_home, team_score, rival_score, rival_name],
        index=target_index_cols)


def treat_2009_to_2020_df(df: pd.DataFrame, year: int) -> pd.DataFrame:
    df = treat_2021_to_2023(df, year)
    df["Motivo"] = df['Motivo'].apply(
        lambda x: reason_to_english_map[x.split(" ")[0]])

    df.rename({"Motivo": "Reason"}, inplace=True, axis=1)

    return df


def treat_2021_to_2023(df: pd.DataFrame, year: int) -> pd.DataFrame:
    df['Dia Saída'] = df['Data'].apply(
        lambda x: int(x.split(" ")[0].capitalize()))
    df['Mês Saída'] = df['Data'].apply(
        lambda x: int(month_to_number_map[x.split(" ")[-1].capitalize()]))
    df['Rod'] = df['Rod'].apply(remove_non_numeric)
    df['Pos'] = df['Pos'].apply(remove_non_numeric)
    df['Ano'] = year
    df["Antecessor"] = df['Antecessor'].apply(remove_anything_unwanted)
    df["Sucessor"] = df['Sucessor'].apply(remove_anything_unwanted)
    df["Última partida"] = df['Última partida'].apply(remove_anything_unwanted)
    df['Clube'] = df['Clube'].apply(normalize_team_name)
    df["Última partida"] = df['Última partida'].apply(normalize_team_name)

    target_match_results_cols = [
        "Last Match Result", "Last Match at Home", "Team score", "Rival score",
        "Rival Team"
    ]
    df[target_match_results_cols] = df[['Última partida', 'Clube']].apply(
        parse_last_match_result, args=(target_match_results_cols, ), axis=1)

    df.rename(
        {
            "Clube": 'Team',
            "Antecessor": 'Coach Out',
            "Dia Saída": "Day Out",
            "Mês Saída": "Month Out",
            "Sucessor": "Coach In",
            "Dia Entrada": "Day In",
            "Mês Entrada": "Month In",
            "Ano": "Year",
            "Rod": "Round",
            "Pos": "Current Position"
        },
        inplace=True,
        axis=1)

    df.drop(["Ref.", "Data", "Última partida"], axis=1, inplace=True)
    df.sort_values(by=["Month Out", "Day Out"], inplace=True)
    df.reset_index(inplace=True, drop=True)
    df["Team score"] = df['Team score'].astype(int)
    df["Rival score"] = df['Rival score'].astype(int)
    return df


if __name__ == "__main__":
    target_paths = sorted(
        list(config.COACHES_FIRED_CSV_TABLE_DIR_PATH.glob("*.csv")))
    config.COACHES_FIRED_CSV_TREATED_TABLE_DIR_PATH.mkdir(parents=True,
                                                          exist_ok=True)

    final_df = pd.DataFrame()
    for path in tqdm(target_paths, desc="Treating and aggregating csv files"):
        year = int(str(path).split("_")[-1].split(".")[-2])
        curr_df = pd.read_csv(path)

        if year == 2008:
            curr_df = treat_2008_df(curr_df)

        elif year in list(range(2009, 2021)):
            curr_df = treat_2009_to_2020_df(curr_df, year)

        elif year in list(range(2021, 2024)):
            curr_df = treat_2021_to_2023(curr_df, year)

        final_df = pd.concat(
            [final_df, curr_df],
            ignore_index=True,
        )

    final_df.to_csv(config.COACHES_FIRED_CSV_TREATED_TABLE_PATH, index=False)
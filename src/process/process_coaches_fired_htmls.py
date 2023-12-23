from bs4 import BeautifulSoup

def print_if_not_empty(target_list, print_string):
    if len(target_list) > 0:
        print(print_string)
        for element in target_list:
            print(element)

if __name__ == "__main__":
    soup = BeautifulSoup(html, 'html.parser')

    tag_list = soup.find_all(
        "span", id=["Mudança_de_técnicos", "Mudanças_de_técnicos"])
    if len(tag_list) == 0:
        couldnt_find_coaches_changes_table.append(target_link)
        continue

    print_if_not_empty(couldnt_find_coaches_changes_table,
                       "Erros de encontrar tabela alvo:")
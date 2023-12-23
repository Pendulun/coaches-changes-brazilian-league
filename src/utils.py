def print_if_not_empty(target_list, print_string):
    if len(target_list) > 0:
        print(print_string)
        for element in target_list:
            print(element)
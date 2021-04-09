import pandas as pd

data = pd.read_csv('Pokemon/pokemon.csv')
counts = dict(data['Type1'].value_counts())
types = list(counts)
types.sort()
all_pokemon = list(data['Name'])

PER_PAGE = 15

def getPageNums(lst):
    total_page_nums = len(lst) // PER_PAGE if len(lst) % PER_PAGE == 0 else len(lst) // PER_PAGE + 1
    return total_page_nums


def getIndices(total_page_nums, page_num):
    print(total_page_nums, page_num)
    if int(page_num) == int(total_page_nums):
        return [(int(page_num) - 1) * PER_PAGE, None]
    else:
        return [(int(page_num) - 1) * PER_PAGE, int(page_num) * PER_PAGE]


if __name__ == "__main__":
    print(counts, types)
    print(all_pokemon)

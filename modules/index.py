from classes.Select import Select


def indexPage():
    select_url = Select.select_with_fzf(
        ['Choose url from clipboard', 'Select saved urls'])
    print(f'{select_url}: select_url')

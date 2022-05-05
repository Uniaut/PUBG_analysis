option_description = {
    'S': 'Get Sample Matches From API'
}

option_act = {
    'S': None
}


if __name__ == '__main__':
    for k, v in option_description.items():
        print(k, v)

    key = input('Select Option > ')

    option_act[key]()
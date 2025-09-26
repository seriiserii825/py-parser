from classes.Print import Print


def duplicate_ids(soup):
    ids = {}
    for tag in soup.find_all(True):
        if 'id' in tag.attrs:
            id_value = tag['id']
            if id_value in ids:
                ids[id_value] += 1
            else:
                ids[id_value] = 1

    duplicate_ids = {id_value: count for id_value, count in ids.items() if count > 1}

    if duplicate_ids:
        Print.error("Duplicate IDs found:")
        for id_value, count in duplicate_ids.items():
            Print.info(f"ID: {id_value}, Count: {count}")
    else:
        Print.success("No duplicate IDs found.")

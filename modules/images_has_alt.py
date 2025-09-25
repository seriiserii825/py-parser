from classes.Print import Print


def images_has_alt(sup):
    images = sup.find_all('img')
    without_alt = []
    for img in images:
        if not img.has_attr('alt') or img['alt'].strip() == '':
            without_alt.append(str(img))

    if without_alt:
        Print.error(f"Found {len(without_alt)} images without alt attribute:")
        for img in without_alt:
            Print.info(img)
    else:
        Print.success("All images have alt attributes.")

from classes.Print import Print


def phone_watsapp(soup):
    # find all links with tel: inside href
    phones = soup.find_all("a", href=lambda href: href and "tel:" in href)
    phones_fails = []
    for phone in phones:
        href = phone.get("href")
        phone_number = href.split("tel:")[1]
        if phone_number.startswith("39"):
            Print.error(f"Phone number {phone_number} does not start with +39")
            phones_fails.append(phone_number)
    if not phones_fails:
        Print.success("All phone numbers are correct")

    watsapp_links = soup.find_all("a", href=lambda href: href and "wa.me" in href)
    watsapp_fails = []
    for watsapp in watsapp_links:
        href = watsapp.get("href")
        phone_number = href.split("wa.me/")[1]
        if not phone_number.startswith("39"):
            Print.error(f"Watsapp number {phone_number} does not start with 39")
            watsapp_fails.append(phone_number)
    if not watsapp_fails:
        Print.success("All Watsapp numbers are correct")

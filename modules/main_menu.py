from classes.Domain import Domain
from classes.Print import Print
from classes.Select import Select


def main_menu():
    dm = Domain()
    domain_url = ""

    options = [
        "Select saved urls",
        "View all from file",
        "Remove from file",
        "Choose url from clipboard",
        "Exit",
    ]

    while True:
        choice = Select.select_one(options)

        if choice == "Choose url from clipboard":
            # clipboard path does not require urls.txt to exist
            url = dm.get_from_clipboard()
            if url:
                domain_url = url
            else:
                Print.error("No valid URL found in clipboard.")
                continue

        elif choice == "View all from file":
            dm.view_all_from_file()

        elif choice == "Remove from file":
            dm.remove_from_file()
            dm.view_all_from_file()

        elif choice == "Select saved urls":
            urls = dm.get_urls_from_file()
            if not urls:
                Print.error("urls.txt is empty.")
                continue
            picked = Select.select_one(urls)
            if picked:
                domain_url = picked
            else:
                Print.error("No URL selected.")
                # back to menu
        elif choice == "Exit":
            Print.error("Exiting.")
            return ""
        else:
            Print.error("Unknown option. Try again.")

        if domain_url:
            Print.info(f"Selected URL: {domain_url}")
            return domain_url

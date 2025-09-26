from classes.Clipboard import Clipboard
from classes.PathHelper import PathHelper
from classes.Print import Print
from classes.Select import Select


def get_url():
    url = ""
    options = ['Select saved urls', 'Choose url from clipboard']
    select_url = Select.select_with_fzf(options)
    ph = PathHelper()
    script_dir = ph.script_dir.parent   # ✅ works
    url_file = script_dir / 'urls.txt'
    if select_url == ['Choose url from clipboard']:
        clipboard = Clipboard.paste()
        if not clipboard.startswith('http') or not clipboard.startswith('https'):
            Print.error("Clipboard does not contain a valid URL.")
            return
        else:
            url = clipboard
            print("Do you want to save this URL? (y/n): ", end="")
            if input().lower() == 'y':
                with open(url_file, 'a') as f:
                    f.write(url + '\n')
                Print.success(f"URL saved to {url_file}")
            return url
    else:
        url_file = url_file
        if not url_file.exists():
            Print.error(f"No urls.txt file found at {url_file}")
            return
        with open(url_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        selected_url = Select.select_with_fzf(urls)
        if selected_url:
            url = selected_url[0]
            return url
        else:
            Print.error("No URL selected.")
            return

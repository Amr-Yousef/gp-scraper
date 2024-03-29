import requests
from bs4 import BeautifulSoup


def write_to_file(filename, data):
    mode = 'w+'
    try:
        with open(filename, mode, encoding='utf-8') as file:
            if isinstance(data, str):
                file.write(data)
            else:
                for line in data:
                    if "\n" in line:  # Remove new line characters if found, for consistency
                        line = line.replace("\n", "")
                    file.write(str(line) + '\n')
        print(f"Data written to '{filename}'.")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_from_file(filename):
    data = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                data.append(line.strip())  # Removing leading/trailing whitespaces and newline characters
        print(f"Data read from '{filename}'.")
        return data
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def get_links_from_html(soup, prefix):
    links = []
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        href = a_tag.get('href')
        if href and f'{prefix}/' in href:
            links.append(href)
    return links


def request_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}")


def soupify(html):
    return BeautifulSoup(html, 'html.parser')


def level_1_links():
    lvl_1 = ['moreclasses', 'products', 'Brands']  # Case sensitive
    lvl_1_dict = {
        'moreclasses': 'Class',
        'products': 'product',
        'Brands': 'Brand'
    }

    for lvl in lvl_1:
        page = 1
        all_links = []
        while True:
            url = f"https://140online.com/{lvl}.aspx?page={str(page)}"
            html = soupify(request_url(url))
            links = get_links_from_html(html, lvl_1_dict[lvl])
            if not links:
                print(f"No links found for {lvl_1_dict[lvl]} at page {page}. Leaving...")
                write_to_file(f"{lvl}.txt", all_links)
                break
            else:
                print(f"Links found for {lvl} at page {page}.")
                all_links += links
                if lvl == 'moreclasses':  # This is an outlier page with 1 page only
                    write_to_file(f"{lvl}.txt", all_links)
                    break
            page += 1


def main():
    # level_1_links()
    links = read_from_file('Brands.txt')
    print(len(links))



if __name__ == "__main__":
    main()

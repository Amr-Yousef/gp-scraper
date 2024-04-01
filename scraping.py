from func import write_to_file, read_from_file, request_url
from bs4 import BeautifulSoup
import concurrent.futures


def get_links_from_html(soup, prefix):
    links = []
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        href = a_tag.get('href')
        if href and f'{prefix}/' in href and href not in links:
            links.append(href)
            print(f"Link found: {href}")
    return links


def soupify(html):
    if not html:
        print("Something went horribly wrong and I have no idea what it is")
        return BeautifulSoup("", 'html.parser')
    return BeautifulSoup(html, 'html.parser')


def process_link(link):
    url = f"https://140online.com{link}"
    html = soupify(request_url(url))
    found_links = get_links_from_html(html, "company")
    if not found_links:
        print(f"No links found for {link}.")
        return []
    else:
        print(f"Links found for {link}.")
        return found_links


def level_2_links():
    links = read_from_file('products.txt')  # Brands.txt is done
    all_links = []
    total_links = len(links)
    processed_links = 0

    def update_progress():
        nonlocal processed_links
        processed_links += 1
        print(f"Processed {processed_links}/{total_links} links")

    with concurrent.futures.ThreadPoolExecutor() as executor:  # Multithreading the operation because otherwise I will grow old and die before this finishes.e
        futures = [executor.submit(process_link, link) for link in links]
        for future in concurrent.futures.as_completed(futures):
            found_links = future.result()
            if found_links:
                for e in found_links:
                    if e not in all_links:
                        all_links.append(e)
            update_progress()

    write_to_file(f"Brands_companies.txt", all_links)


def main():
    level_2_links()


if __name__ == "__main__":
    main()

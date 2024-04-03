from func import write_to_file, read_from_file, request_url
from bs4 import BeautifulSoup
from tqdm import tqdm
import re
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from math import ceil


def get_links_from_html(soup, prefix):
    links = []
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        href = a_tag.get('href')
        if href and f'{prefix}/' in href and href not in links:
            links.append(href)
    return links


def get_results_number(soup):
    if not soup:
        return 0
    results = soup.find(class_='rtsTxt').get_text(strip=True)
    number = re.findall(r'\d+', results)
    return number[0] if number else 0


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

    write_to_file(f"oops.txt", all_links)


def level_2_links_classes():
    def classes_process_link(link):
        url = f"https://140online.com/{link}"
        html = soupify(request_url(url))
        results_no = get_results_number(html)
        pages_no = ceil(int(results_no) / 20)
        print(f"Processing {link} with {results_no} results and {pages_no} pages.")
        classes_links_set = set()  # Initialize a set to store unique links
        for page in range(1, pages_no + 1):
            current_url = f"https://140online.com/class/pages/{link[6:]}/{page}"
            current_html = soupify(request_url(current_url))
            found_links = get_links_from_html(current_html, "company")
            if found_links:
                classes_links_set.update(found_links)  # Add unique links to the set
        print(f"Found {len(classes_links_set)} links for {link}. Done.")
        return classes_links_set

    links = read_from_file('moreclasses.txt')
    all_links_set = set()  # Initialize an empty set to store unique links
    with ThreadPoolExecutor() as executor:
        with tqdm(total=len(links), desc="Processing Links") as pbar:
            for found_links_set in executor.map(classes_process_link, links):
                pbar.update(1)  # Update progress bar after processing each link
                all_links_set.update(found_links_set)  # Add unique links from each thread
    return list(all_links_set)  # Convert the set back to a list


def main():
    links = level_2_links_classes()
    print(f"Total links: {len(links)}")
    write_to_file('classes_companies.txt', links)


if __name__ == "__main__":
    main()

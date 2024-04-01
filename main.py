from func import write_to_file, read_from_file, request_url


def main():
    links = read_from_file('products.txt')[0]
    print(links)


if __name__ == "__main__":
    main()

import requests


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


def request_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code}")

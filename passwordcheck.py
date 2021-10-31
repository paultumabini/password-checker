import requests
import hashlib
import sys


def request_api_data(query):
    res = requests.get('https://api.pwnedpasswords.com/range/' + query)
    if res.status_code != 200:
        raise RuntimeError(f'Error Fecthing: {res.status_code}, check the api and try again')
    return res


def split_password_counts(hashes, hash_to_check):
    split_hashes = [h.split(':') for h in hashes.text.splitlines()]
    for hash, count in split_hashes:
        if hash == hash_to_check:
            return count
    return 0


def pwned_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

    first5_char, tail = sha1_password[:5], sha1_password[5:]
    response = request_api_data(first5_char)
    return split_password_counts(response, tail)


def main_func(args):
    for i, arg in enumerate(args):
        res_count = pwned_api_check(arg)
        output = 'Search {}: No Matched found'.format(i + 1) if not res_count else 'Search {}: found {}'.format(i + 1, res_count)
        print(output)

    return 'All done sys run!'


if __name__ == '__main__':
    sys.exit(main_func(sys.argv[1:]))

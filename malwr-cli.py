#! /usr/bin/env python2
from MalwrAPI import MalwrAPI
import argparse
import ConfigParser
import os
import hashlib


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI interface for malwr.com')
    parser.add_argument('-S', '--submit', help='Submit the file')
    parser.add_argument('-s', '--search', help='Search for the string or the file')
    parser.add_argument(
            '-d', '--domains', help='List recent domains',
            action="store_true"
    )
    parser.add_argument(
            '-t', '--tags', help='List public tags',
            action="store_true"
    )
    parser.add_argument(
            '-r', '--recent', help='List recent analyses',
            action="store_true"
    )
    args = parser.parse_args()

    # Read the config file
    authentication = None
    try:
        # FIXME : authenticate only if needed
        config = ConfigParser.RawConfigParser()
        config.read(os.path.expanduser('~/.malwr'))
        apikey = config.get('Malwr', 'apikey')
        user = config.get('Malwr', 'user')
        pwd = config.get('Malwr', 'password')
        authentication = {
                'apikey': apikey,
                'user': user,
                'password': pwd
                }
        api = MalwrAPI(verbose=True, username=user, password=pwd)
    except:
        print('Trouble with ~/.malwr config file, authenticated features unavailable')
        api = MalwrAPI(verbose=True)

    if args.search is not None:
        if os.path.isfile(args.search):
            fhash = md5(args.search)
            print('Search for hash %s (file %s)' % (fhash, args.search))
            res = api.search(fhash)
        else:
            print('Search for %s' % args.search)
            res = api.search(args.search)
        if res is False:
            print('failed login')
        else:
            if res == []:
                print('No results')
            else:
                for d in res:
                    print(
                        '%s\t%s\t%s\thttps://malwr.com%s' % (
                            d['submission_time'], d['file_name'],
                            d['hash'], d['submission_url']
                        )
                    )
    elif args.submit is not None:
        res = api.submit_sample(filepath=args.submit)
        print('File submitted : https://malwr.com%s for %s (hash: %s)' % (res['analysis_link'], res['file'], res['md5']))
    elif args.domains:
        res = api.get_recent_domains()
        print('Recent domains:')
        for d in res:
            print('%s -> https://malwr.com%s' % (d['domain_name'], d['url_analysis']))
    elif args.tags:
        res = api.get_public_tags()
        print('Public tags:')
        for t in res:
            print(t)
    elif args.recent:
        res = api.get_recent_analyses()
        print('Recent analyses:')
        for d in res:
            print('%s -> https://malwr.com%s' % (d['hash'], d['submission_url']))

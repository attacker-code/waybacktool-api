#!/usr/bin/env python
import requests
import sys
import json
import argparse
import warnings
import sys
from urllib.parse import urlparse
import socket
import multiprocessing
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description='Tool for parsing WayBack URLs.')

parser.add_argument('function', help="`pull` or `check`. `pull` will gather the urls from the WayBack API. `check` will ensure the response code is positive (200,301,302,307).")
parser.add_argument('--host', help='The host whose URLs should be retrieved.')
parser.add_argument('--threads', help='The number of threads to use (Default 5)', default=5)
parser.add_argument('--with-subs', help='`yes` or `no`. Retrieve urls from subdomains of the host.', default=True)
parser.add_argument('--loadfile', help='Location of file from which urls should be checked.')
parser.add_argument('--outputfile', help='Location of the file to which checked urls should be reported')

args = parser.parse_args()

session = requests.Session()
retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
adapter = HTTPAdapter(max_retries=retries)
session.mount('http://', adapter)
session.mount('https://', adapter)

def waybackurls(host, with_subs):
    if with_subs:
        url = 'http://web.archive.org/cdx/search/cdx?url=*.%s/*&output=list&fl=original&collapse=urlkey' % host
    else:
        url = 'http://web.archive.org/cdx/search/cdx?url=%s/*&output=list&fl=original&collapse=urlkey' % host
    try:
        r = session.get(url, timeout=(3.05, 27))
    except requests.exceptions.Timeout:
        print("La solicitud ha excedido el tiempo de espera")
    except requests.exceptions.TooManyRedirects:
        print("Demasiadas redirecciones")
    except requests.exceptions.RequestException as e:
        print(f"Ha ocurrido un error: {e}")
    else:
        if args.outputfile:
            j = open(args.outputfile, "w")
            j.write(r.text.strip())
            j.close()
        print(r.text.strip())

# Rest of your functions go here...

# Then, at the bottom of your script:

manager = multiprocessing.Manager()
timeout = manager.list()
writeQueue = manager.Queue()
pool = multiprocessing.Pool(args.threads)
if args.function == "pull":
    if args.host:
        waybackurls(args.host, args.with_subs)
    elif args.loadfile:
        for line in open(args.loadfile).readlines():
            waybackurls(line.strip(), args.with_subs)

# Rest of your script goes here...


elif args.function == "check":
    if args.loadfile:
        try:
            if args.outputfile:
                outputfile = open(args.outputfile, "w", 0)
                p = multiprocessing.Process(target=writer, args=(outputfile,))
                p.start()
            endpoints = checkValidDomain(open(args.loadfile).readlines())
            pool.map(check, endpoints)
            if args.outputfile:
                writeQueue.put(None)
                p.join()
                outputfile.close()
        except IOError as e:
            print("[-] File not found!")
            sys.exit(1)
        except KeyboardInterrupt as e:
            print("[-] Killing processes...")
            pool.terminate()
            sys.exit(1)
        except Exception as e:
            print("[-] Unknown Error: "+str(e))

    elif not sys.stdin.isatty():
        try:
            if args.outputfile:
                outputfile = open(args.outputfile, "w", 0)
                p = multiprocessing.Process(target=writer, args=(outputfile,))
                p.start()
            endpoints = checkValidDomain(sys.stdin.readlines())
            pool.map(check, endpoints)
            if args.outputfile:
                writeQueue.put(None)
                p.join()
                outputfile.close()
        except IOError as e:
            print(e)
            print("[-] File not found!")
            sys.exit(1)
        except KeyboardInterrupt as e:
            print("[-] Killing processes...")
            pool.terminate()
            sys.exit(1)
        except Exception as e:
            print("[-] Unknown Error: "+str(e))
    else:
        print("[-] Please either specify a file using --loadfile or pipe some data in!")
        exit()
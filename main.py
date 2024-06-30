import tls_client
import random
import time
import os
from colorama import Fore, Style
import time
import string
import os
import threading

lc = (Fore.RESET + "[" + Fore.LIGHTMAGENTA_EX + ">" + Fore.RESET + "]")
ld= f"{Fore.RESET}{Fore.LIGHTBLACK_EX}{Style.BRIGHT}[{Fore.LIGHTMAGENTA_EX}N{Style.BRIGHT}{Fore.LIGHTBLACK_EX}]{Fore.RESET}"


class Log:
    @staticmethod
    def err(msg):
        print(f'{Fore.RESET}{Style.BRIGHT}[{Fore.LIGHTRED_EX}-{Fore.RESET}] {msg}')

    @staticmethod
    def succ(msg):
        print(f'{Fore.RESET}{Style.BRIGHT}[{Fore.LIGHTMAGENTA_EX}+{Fore.RESET}] {msg}')

    @staticmethod
    def console(msg):
        print(f'{Fore.RESET}{Style.BRIGHT}[{Fore.LIGHTMAGENTA_EX}-{Fore.RESET}] {msg}')


class DiscordJoinerPY:
    def __init__(self):
        self.joined_tokens_lock = threading.Lock()
        self.client = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )
        self.tokens = []
        self.proxies = []
        self.check()
        self.joined_count = 0
        self.not_joined_count = 0
        self.done_event = threading.Event()

    def write_joined_token(self, token, invite):
        with self.joined_tokens_lock:
            with open("output/" + invite + ".txt", "a") as f:
                f.write(f"{token}\n")

    def headers(self, token: str):
        headers = {
            'authority': 'discord.com',
            'accept': '*/*',
            'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': token,
            'content-type': 'application/json',
            'origin': 'https://discord.com',
            'referer': 'https://discord.com/channels/@me',
            'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'x-context-properties': 'eyJsb2NhdGlvbiI6IkpvaW4gR3VpbGQiLCJsb2NhdGlvbl9ndWlsZF9pZCI6IjExMDQzNzg1NDMwNzg2Mzc1OTEiLCJsb2NhdGlvbl9jaGFubmVsX2lkIjoiMTEwNzI4NDk3MTkwMDYzMzIzMCIsImxvY2F0aW9uX2NoYW5uZWxfdHlwZSI6MH0=',
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-GB',
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6Iml0LUlUIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzExMi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTEyLjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiIiLCJyZWZlcnJpbmdfZG9tYWluIjoiIiwicmVmZXJyZXJfY3VycmVudCI6IiIsInJlZmVycmluZ19kb21haW5fY3VycmVudCI6IiIsInJlbGVhc2VfY2hhbm5lbCI6InN0YWJsZSIsImNsaWVudF9idWlsZF9udW1iZXIiOjE5MzkwNiwiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbCwiZGVzaWduX2lkIjowfQ==',
        }
        return headers
    

    def get_cookies(self):
        cookies = {}
        try:
          response = self.client.get('https://discord.com')
          for cookie in response.cookies:
            if cookie.name.startswith('__') and cookie.name.endswith('uid'):
                cookies[cookie.name] = cookie.value
          return cookies
        
        except Exception as e:
          Log.err('Failed to obtain cookies ({})'.format(e))
          return cookies


    def accept_invite(self, token: str, invite: str, proxy_: str):
        try:
            payload = {
                'session_id': ''.join(random.choice(string.ascii_lowercase) + random.choice(string.digits) for _ in range(16))
            }

            proxy = {
                "http": "http://{}".format(proxy_),
                "https": "https://{}".format(proxy_)

            } if proxy_ else None

            response = self.client.post(
                url='https://discord.com/api/v10/invites/{}'.format(invite),
                headers=self.headers(token=token),
                json=payload,
                cookies=self.get_cookies(),
                proxy=proxy
            )
            response_json = response.json()
            if response.status_code == 200:
                print(f"{ld} {Fore.BLUE}token={Fore.WHITE}{token[:20]}...{Fore.RESET} {Fore.LIGHTGREEN_EX}JOINED -> {Fore.LIGHTBLACK_EX}({response.status_code}) {Fore.LIGHTBLACK_EX}(discord.gg/{invite})")
                self.write_joined_token(token, invite)
                self.joined_count += 1
            elif response.status_code == 401 and response_json['message'] == "401: Unauthorized":
                Log.err(f'{ld} {Fore.BLUE}token={Fore.WHITE}{token[:20]}...{Fore.RESET} {Fore.RED}INVALID -> {Fore.LIGHTBLACK_EX}({response.status_code})')
                self.not_joined_count += 1
            elif response.status_code == 403 and response_json['message'] == "You need to verify your account in order to perform this action.":
                Log.err(f'{ld} {Fore.BLUE}token={Fore.WHITE}{token[:20]}...{Fore.RESET} {Fore.RED}FLAGGED -> {Fore.LIGHTBLACK_EX}({response.status_code})')
                self.not_joined_count += 1
            elif response.status_code == 400 and response_json['captcha_key'] == ['You need to update your app to join this server.']:
                Log.err(f"{ld} {Fore.BLUE}token={Fore.WHITE}{token[:20]}...{Fore.RESET} {Fore.RED}HCAPTCHA -> {Fore.LIGHTBLACK_EX}({response.status_code})")
                self.not_joined_count += 1
            elif response_json['message'] == "404: Not Found":
                Log.err('Unknown invite ({})'.format(invite))
            else:
                Log.err('Invalid response ({})'.format(response_json))
                self.not_joined_count += 1

            if self.joined_count + self.not_joined_count == len(self.tokens):
                self.done_event.set()

        except Exception as e:
            Log.err('Unknown error occurred in accept_invite: {}'.format(e))
            self.not_joined_count += 1
            if self.joined_count + self.not_joined_count == len(self.tokens):
                self.done_event.set()



    def check(self):
        folder_path = "input"
        file_path = os.path.join(folder_path, "tokens.txt")

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if not os.path.exists(file_path):
            for file_name in ['proxies.txt', 'tokens.txt']:
                file_path = os.path.join(folder_path, file_name)
                if not os.path.exists(file_path):
                    with open(file_path, "w") as file:
                        file.write("Delete! proxies: ip:port:host:pass")

        self.load_tokens()


    def load_tokens(self):
          with open("./input/tokens.txt", "r") as file:
           for line in file:
             content = line.replace("\n",  "")
             self.tokens.append(content)

           self.start()

    

    def load_proxies(self):
          with open("./input/proxies.txt", "r") as file:
           for line in file:
             content = line.replace("\n",  "")
             self.proxies.append(content)

    def print_results(self):
        print(f"{Fore.RESET}{Style.BRIGHT}[{Fore.LIGHTGREEN_EX}RESULTS{Fore.RESET}] Joined Tokens: {self.joined_count}, Failed Tokens: {self.not_joined_count}")

    def wait_for_completion(self):
        self.done_event.wait()


    def start(self):
        os.system("title discord.gg/nexustools ")
        self.iterator = iter(self.proxies)
        self.load_proxies()
        os.system("cls")
        print(f"""{Fore.LIGHTMAGENTA_EX}
                    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗   ████████╗ ██████╗  ██████╗ ██╗     ███████╗
                    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝   ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
                    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗█████╗██║   ██║   ██║██║   ██║██║     ███████╗
                    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║╚════╝██║   ██║   ██║██║   ██║██║     ╚════██║
                    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║      ██║   ╚██████╔╝╚██████╔╝███████╗███████║
                    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝      ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
                                                discord.gg/nexus-tools

                                            
                                            
                                            

""")
        invite = input(lc + " Invite Code: ".format(time.strftime("%H:%M:%S")))
        for token in self.tokens:
            if self.proxies == [] or self.proxies[0] == "/// Remove this line":
                proxy = None
            else:
                proxy = next(self.iterator)
                Log.succ('Using ({})'.format(proxy))

            threading.Thread(target=self.accept_invite, args=(token, invite, proxy)).start()

if __name__ == '__main__':
    joiner = DiscordJoinerPY()
    joiner.wait_for_completion()
    joiner.print_results()
    input("")
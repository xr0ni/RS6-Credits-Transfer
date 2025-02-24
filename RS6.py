import threading, ctypes, time, random

from queue import Queue, Empty
from time import sleep
from tls_client import Session
from os import system, _exit, path
from json import loads, dumps
from colorama import Fore
from datetime import datetime
from libs.eazyui import *

class Ubisoft():
    def __init__(self, accounts_normal, accounts_with_credits):
        self.mode = "0"
        self.timeNow = datetime.now().strftime("%H:%M:%S")[:-3]
        self.session = Session(client_identifier="chrome126", random_tls_extension_order=True)
        self.clear_console()
        ctypes.windll.kernel32.SetConsoleTitleW("R6S Marketplace Tool | @rr4r")
        self.initialize_accounts(accounts_normal, accounts_with_credits)
        self.mainFunction()

    def initialize_accounts(self, accounts_normal, accounts_with_credits):
        try:
            self.accounts_normal = self.load_file(accounts_normal)
            self.accounts_normal_bool = True 
            self.accounts_normal_with_tickets = []
            self.log("INFO", f"Normal accounts loaded: {Fore.LIGHTBLUE_EX}{len(self.accounts_normal):,}{Fore.WHITE}")
        except Exception as e:
            self.log("ERROR", f"Failed to load Accounts.txt: {e}")
            input()
            _exit(0)

        try:
            self.accounts_with_credits = self.load_file(accounts_with_credits)
            self.accounts_with_credits_bool = True
            self.accounts_with_credits_with_tickets = []
            self.log("INFO", f"Accounts with credits loaded: {Fore.LIGHTBLUE_EX}{len(self.accounts_with_credits):,}{Fore.WHITE}")
        except:
            self.accounts_with_credits_bool = False

    def log(self, level, *args):
        color_map = {
            "1": (Fore.LIGHTBLUE_EX, "1"),
            "2": (Fore.LIGHTBLUE_EX, "2"),
            "3": (Fore.LIGHTBLUE_EX, "3"),
            "4": (Fore.LIGHTBLUE_EX, "4"),
            "5": (Fore.LIGHTBLUE_EX, "5"),
            "6": (Fore.LIGHTBLUE_EX, "6"),
            "INFO": (Fore.LIGHTBLUE_EX, "*"),
            "INFO2": (Fore.LIGHTBLUE_EX, "^"),
            "INPUT": (Fore.LIGHTYELLOW_EX, "?"),
            "ERROR": (Fore.LIGHTRED_EX, "!"),
            "SUCCESS": (Fore.LIGHTGREEN_EX, "+")
        }
        color, text = color_map.get(level, (Fore.LIGHTWHITE_EX, level))
        time_now = datetime.now().strftime("%H:%M:%S")[:-3]
        base = f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{time_now}{Fore.WHITE}] ({color}{text.upper()}{Fore.WHITE})"
        for arg in args:
            base += f"{Fore.WHITE} {arg}"
        print(base)

    def clear_console(self):
        system("cls")
        print(Colorate.Diagonal(Colors.red_to_purple, Center.XCenter("""
    ____  __________    __  ___           __        __        __                   ______            __
   / __ \/ ___/ ___/   /  |/  /___ ______/ /_____  / /_____  / /___ _________     /_  __/___  ____  / /
  / /_/ / __ \\\__ \   / /|_/ / __ `/ ___/ //_/ _ \/ __/ __ \/ / __ `/ ___/ _ \     / / / __ \/ __ \/ / 
 / _, _/ /_/ /__/ /  / /  / / /_/ / /  / ,< /  __/ /_/ /_/ / / /_/ / /__/  __/    / / / /_/ / /_/ / /  
/_/ |_|\____/____/  /_/  /_/\__,_/_/  /_/|_|\___/\__/ .___/_/\__,_/\___/\___/    /_/  \____/\____/_/   
                                                   /_/                                                 
""") + "\n" + Center.XCenter("By Roni - Instagram @rr4r")))
        print("")
    
    def load_file(self, file_name):
        with open(file_name, "r") as file:
            return [tuple(line.strip().split(':')) for line in file]

    def grabCreditsAmount(self, token, sessionId) -> None:
        try:
            getCredits = self.session.post("https://public-ubiservices.ubi.com/v1/profiles/me/uplay/graphql", headers={
                "Ubi-AppId": "45d80707-deeb-40d6-b5b5-9be96631e90e",
                "Authorization": f"ubi_v1 t={token}",
                "Ubi-Sessionid": sessionId,
                "Accept-Language": "en-US",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
            }, data=dumps([{"operationName":"GetBalance","variables":{"spaceId":"0d2ae42d-4c27-4cb7-af6c-2099062302bb","itemId":"9ef71262-515b-46e8-b9a8-b6b6ad456c67"},"query":"query GetBalance($spaceId: String!, $itemId: String!) {\n  game(spaceId: $spaceId) {\n    id\n    viewer {\n      meta {\n        id\n        secondaryStoreItem(itemId: $itemId) {\n          meta {\n            id\n            quantity\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"}]))
            if 'quantity' in getCredits.text:
                jsonData = loads(getCredits.text)
                creditsCount = jsonData[0]['data']['game']['viewer']['meta']['secondaryStoreItem']['meta']['quantity']
                return creditsCount
            else:
                return "Couldn't Grab Credits"
        except:
            pass

    def itemIsOwned(self, token, sessionId, itemId) -> None:
        try:
            getItemDetails = self.session.post("https://public-ubiservices.ubi.com/v1/profiles/me/uplay/graphql", headers={
                "Ubi-AppId": "80a4a0e8-8797-440f-8f4c-eaba87d0fdda",
                "Authorization": f"ubi_v1 t={token}",
                "Ubi-Sessionid": sessionId,
                "Accept-Language": "en-US",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
            }, data=dumps([{"operationName":"GetItemDetails","variables":{"spaceId":"0d2ae42d-4c27-4cb7-af6c-2099062302bb","itemId":itemId,"tradeId":"","fetchTrade":False},"query":"query GetItemDetails($spaceId: String!, $itemId: String!, $tradeId: String!, $fetchTrade: Boolean!) {\n  game(spaceId: $spaceId) {\n    id\n    marketableItem(itemId: $itemId) {\n      id\n      item {\n        ...SecondaryStoreItemFragment\n        ...SecondaryStoreItemOwnershipFragment\n        __typename\n      }\n      marketData {\n        ...MarketDataFragment\n        __typename\n      }\n      paymentLimitations {\n        id\n        paymentItemId\n        minPrice\n        maxPrice\n        __typename\n      }\n      __typename\n    }\n    viewer {\n      meta {\n        id\n        trades(filterBy: {states: [Created], itemIds: [$itemId]}) {\n          nodes {\n            ...TradeFragment\n            __typename\n          }\n          __typename\n        }\n        trade(tradeId: $tradeId) @include(if: $fetchTrade) {\n          ...TradeFragment\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SecondaryStoreItemFragment on SecondaryStoreItem {\n  id\n  assetUrl\n  itemId\n  name\n  tags\n  type\n  viewer {\n    meta {\n      id\n      isReserved\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SecondaryStoreItemOwnershipFragment on SecondaryStoreItem {\n  viewer {\n    meta {\n      id\n      isOwned\n      quantity\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment MarketDataFragment on MarketableItemMarketData {\n  id\n  sellStats {\n    id\n    paymentItemId\n    lowestPrice\n    highestPrice\n    activeCount\n    __typename\n  }\n  buyStats {\n    id\n    paymentItemId\n    lowestPrice\n    highestPrice\n    activeCount\n    __typename\n  }\n  lastSoldAt {\n    id\n    paymentItemId\n    price\n    performedAt\n    __typename\n  }\n  __typename\n}\n\nfragment TradeFragment on Trade {\n  id\n  tradeId\n  state\n  category\n  createdAt\n  expiresAt\n  lastModifiedAt\n  failures\n  tradeItems {\n    id\n    item {\n      ...SecondaryStoreItemFragment\n      ...SecondaryStoreItemOwnershipFragment\n      __typename\n    }\n    __typename\n  }\n  payment {\n    id\n    item {\n      ...SecondaryStoreItemQuantityFragment\n      __typename\n    }\n    price\n    transactionFee\n    __typename\n  }\n  paymentOptions {\n    id\n    item {\n      ...SecondaryStoreItemQuantityFragment\n      __typename\n    }\n    price\n    transactionFee\n    __typename\n  }\n  paymentProposal {\n    id\n    item {\n      ...SecondaryStoreItemQuantityFragment\n      __typename\n    }\n    price\n    __typename\n  }\n  viewer {\n    meta {\n      id\n      tradesLimitations {\n        ...TradesLimitationsFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SecondaryStoreItemQuantityFragment on SecondaryStoreItem {\n  viewer {\n    meta {\n      id\n      quantity\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TradesLimitationsFragment on UserGameTradesLimitations {\n  id\n  buy {\n    resolvedTransactionCount\n    resolvedTransactionPeriodInMinutes\n    activeTransactionCount\n    __typename\n  }\n  sell {\n    resolvedTransactionCount\n    resolvedTransactionPeriodInMinutes\n    activeTransactionCount\n    resaleLocks {\n      itemId\n      expiresAt\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"}]))
            jsonData = loads(getItemDetails.text)
            isOwned = jsonData[0]["data"]["game"]["marketableItem"]["item"]["viewer"]["meta"]["isOwned"]
            if isOwned == True:
                return True
            else:
                return False
        except:
            pass

    def login(self, email, password, account_list) -> None:
        try:
            self.log("INFO", f"Logging in to: {Fore.LIGHTBLUE_EX}{email}{Fore.WHITE}")
            encoded = self.encodeBase64(f"{email}:{password}")
            firstLoginAttempt = self.session.post("https://public-ubiservices.ubi.com/v3/profiles/sessions", headers={
                "Ubi-AppId": "45d80707-deeb-40d6-b5b5-9be96631e90e",
                "Authorization": f"Basic {encoded}",
                "GenomeId": "de726b45-417f-476f-a3ba-d0c032a9ef2e",
                "Accept-Language": "en-US",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
            }, data=dumps({"rememberMe":True}))
            if 'ticket' in firstLoginAttempt.text:
                jsonData = loads(firstLoginAttempt.text)
                ticket = jsonData['ticket']
                twoFactorAuth = jsonData['twoFactorAuthenticationTicket']
                if ticket != None:
                    sessionId = jsonData['sessionId']
                    username = jsonData['nameOnPlatform']
                    credits = self.grabCreditsAmount(ticket, sessionId)
                    self.log("SUCCESS", f"Success: {Fore.LIGHTGREEN_EX}{email}{Fore.WHITE}")
                    self.log("SUCCESS", f"Username: {Fore.LIGHTGREEN_EX}{username}{Fore.WHITE}")
                    self.log("SUCCESS", f"Credits: {Fore.LIGHTGREEN_EX}{credits}{Fore.WHITE}")
                    self.log("SUCCESS", f"SessionID: {Fore.LIGHTGREEN_EX}{sessionId}{Fore.WHITE}")
                    account_list.append(f"{email}:{username}:{ticket}:{sessionId}:{credits}")
                else:
                    twoFactorCode = input(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{self.timeNow}{Fore.WHITE}] ({Fore.LIGHTYELLOW_EX}?{Fore.WHITE}) Code: {Fore.LIGHTYELLOW_EX}")
                    secondLoginAttempt = self.session.post("https://public-ubiservices.ubi.com/v3/profiles/sessions", headers={
                        "Ubi-AppId": "45d80707-deeb-40d6-b5b5-9be96631e90e",
                        "Authorization": f"ubi_2fa_v1 t={twoFactorAuth}",
                        "ubi-2facode": twoFactorCode,
                        "GenomeId": "de726b45-417f-476f-a3ba-d0c032a9ef2e",
                        "Accept-Language": "en-US",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
                    }, data=dumps({"rememberMe":True}))
                    if 'ticket' in secondLoginAttempt.text:
                        jsonData = loads(secondLoginAttempt.text)
                        ticket = jsonData['ticket']
                        twoFactorAuth = jsonData['twoFactorAuthenticationTicket']
                        if ticket != None:
                            sessionId = jsonData['sessionId']
                            username = jsonData['nameOnPlatform']
                            credits = self.grabCreditsAmount(ticket, sessionId)
                            self.log("SUCCESS", f"Success: {Fore.LIGHTGREEN_EX}{email}{Fore.WHITE}")
                            self.log("SUCCESS", f"Username: {Fore.LIGHTGREEN_EX}{username}{Fore.WHITE}")
                            self.log("SUCCESS", f"Credits: {Fore.LIGHTGREEN_EX}{credits}{Fore.WHITE}")
                            self.log("SUCCESS", f"SessionID: {Fore.LIGHTGREEN_EX}{sessionId}{Fore.WHITE}")
                            account_list.append(f"{email}:{username}:{ticket}:{sessionId}:{credits}")
                        else:
                            self.login(email, password, account_list)
                    else:
                        self.login(email, password, account_list)
            elif 'Invalid credentials' in firstLoginAttempt.text:
                self.log("ERROR", f'{Fore.LIGHTRED_EX}Wrong email or password{Fore.WHITE}')
            else:
                self.log("ERROR", f'Error: {Fore.LIGHTRED_EX}{email}\n{firstLoginAttempt.text}{Fore.WHITE}')
        except:
            pass

    def getItemAllInfo(self):
        def process_accounts(accounts, itemId, pricee):
            accounts_without_item = []
            for account in accounts:
                try:
                    email, username, token, sessionId, credits = account.split(":")[:5]
                    credits = int(credits)
                    if not self.itemIsOwned(token, sessionId, itemId) and credits >= pricee:
                        accounts_without_item.append(account)
                except:
                    continue

            accounts_without_item.sort(key=lambda x: int(x.split(":")[4]))
            return accounts_without_item
        
        try:
            itemId = input(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{self.timeNow}{Fore.WHITE}] ({Fore.LIGHTBLUE_EX}?{Fore.WHITE}) ItemID: {Fore.LIGHTBLUE_EX}")
            numberOfaccsBuying = int(input(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{self.timeNow}{Fore.WHITE}] ({Fore.LIGHTBLUE_EX}?{Fore.WHITE}) Number of accs buying: {Fore.LIGHTBLUE_EX}"))
            
            if numberOfaccsBuying > len(self.accounts_normal_with_tickets):
                self.log("INFO", f"{Fore.LIGHTRED_EX}You can't buy more accs than the number of accs you have{Fore.WHITE}")
                return

            price = int(input(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{self.timeNow}{Fore.WHITE}] ({Fore.LIGHTBLUE_EX}?{Fore.WHITE}) Price to buy: {Fore.LIGHTBLUE_EX}"))
            price_transfer = 0
            if self.mode == "2":
                if self.accounts_with_credits_bool:
                    price_transfer = int(input(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{self.timeNow}{Fore.WHITE}] ({Fore.LIGHTBLUE_EX}?{Fore.WHITE}) Price to transfer: {Fore.LIGHTBLUE_EX}"))

            randomAcc = self.accounts_normal_with_tickets[0]
            token, sessionId = randomAcc.split(":")[2:4]
            
            getItemDetails = self.session.post("https://public-ubiservices.ubi.com/v1/profiles/me/uplay/graphql", 
                headers={
                    "Ubi-AppId": "80a4a0e8-8797-440f-8f4c-eaba87d0fdda",
                    "Authorization": f"ubi_v1 t={token}",
                    "Ubi-Sessionid": sessionId,
                    "Accept-Language": "en-US",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
                }, 
                data=dumps([{"operationName":"GetItemDetails","variables":{"spaceId":"0d2ae42d-4c27-4cb7-af6c-2099062302bb","itemId":itemId,"tradeId":"","fetchTrade":False},"query":"query GetItemDetails($spaceId: String!, $itemId: String!, $tradeId: String!, $fetchTrade: Boolean!) {\n  game(spaceId: $spaceId) {\n    id\n    marketableItem(itemId: $itemId) {\n      id\n      item {\n        ...SecondaryStoreItemFragment\n        ...SecondaryStoreItemOwnershipFragment\n        __typename\n      }\n      marketData {\n        ...MarketDataFragment\n        __typename\n      }\n      paymentLimitations {\n        id\n        paymentItemId\n        minPrice\n        maxPrice\n        __typename\n      }\n      __typename\n    }\n    viewer {\n      meta {\n        id\n        trades(filterBy: {states: [Created], itemIds: [$itemId]}) {\n          nodes {\n            ...TradeFragment\n            __typename\n          }\n          __typename\n        }\n        trade(tradeId: $tradeId) @include(if: $fetchTrade) {\n          ...TradeFragment\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment SecondaryStoreItemFragment on SecondaryStoreItem {\n  id\n  assetUrl\n  itemId\n  name\n  tags\n  type\n  viewer {\n    meta {\n      id\n      isReserved\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SecondaryStoreItemOwnershipFragment on SecondaryStoreItem {\n  viewer {\n    meta {\n      id\n      isOwned\n      quantity\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment MarketDataFragment on MarketableItemMarketData {\n  id\n  sellStats {\n    id\n    paymentItemId\n    lowestPrice\n    highestPrice\n    activeCount\n    __typename\n  }\n  buyStats {\n    id\n    paymentItemId\n    lowestPrice\n    highestPrice\n    activeCount\n    __typename\n  }\n  lastSoldAt {\n    id\n    paymentItemId\n    price\n    performedAt\n    __typename\n  }\n  __typename\n}\n\nfragment TradeFragment on Trade {\n  id\n  tradeId\n  state\n  category\n  createdAt\n  expiresAt\n  lastModifiedAt\n  failures\n  tradeItems {\n    id\n    item {\n      ...SecondaryStoreItemFragment\n      ...SecondaryStoreItemOwnershipFragment\n      __typename\n    }\n    __typename\n  }\n  payment {\n    id\n    item {\n      ...SecondaryStoreItemQuantityFragment\n      __typename\n    }\n    price\n    transactionFee\n    __typename\n  }\n  paymentOptions {\n    id\n    item {\n      ...SecondaryStoreItemQuantityFragment\n      __typename\n    }\n    price\n    transactionFee\n    __typename\n  }\n  paymentProposal {\n    id\n    item {\n      ...SecondaryStoreItemQuantityFragment\n      __typename\n    }\n    price\n    __typename\n  }\n  viewer {\n    meta {\n      id\n      tradesLimitations {\n        ...TradesLimitationsFragment\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment SecondaryStoreItemQuantityFragment on SecondaryStoreItem {\n  viewer {\n    meta {\n      id\n      quantity\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment TradesLimitationsFragment on UserGameTradesLimitations {\n  id\n  buy {\n    resolvedTransactionCount\n    resolvedTransactionPeriodInMinutes\n    activeTransactionCount\n    __typename\n  }\n  sell {\n    resolvedTransactionCount\n    resolvedTransactionPeriodInMinutes\n    activeTransactionCount\n    resaleLocks {\n      itemId\n      expiresAt\n      __typename\n    }\n    __typename\n  }\n  __typename\n}"}])
            )
            
            jsonData = loads(getItemDetails.text)
            if 'sellStats' in jsonData[0]["data"]["game"]["marketableItem"]["marketData"]:
                paymentItemId = jsonData[0]["data"]["game"]["marketableItem"]["marketData"]["sellStats"][0]["paymentItemId"]
                if self.mode == "1":
                    account_list = process_accounts(self.accounts_normal_with_tickets, itemId, price)
                    self.log("INFO", f"Accounts without the item and with sufficient credits: {Fore.LIGHTBLUE_EX}{len(account_list)}{Fore.WHITE}")
                    successful_purchases = self.threaded_buy(numberOfaccsBuying, account_list, price, itemId, paymentItemId)
                elif self.mode == "2":
                    account_list = process_accounts(self.accounts_normal_with_tickets, itemId, price)
                    self.log("INFO", f"Accounts without the item and with sufficient credits: {Fore.LIGHTBLUE_EX}{len(account_list)}{Fore.WHITE}")
                    successful_purchases = self.threaded_buy(numberOfaccsBuying, account_list, price, itemId, paymentItemId)
                    if successful_purchases == numberOfaccsBuying:
                        if self.accounts_with_credits_bool:
                            result = self.buyItem(self.accounts_with_credits_with_tickets[0], price_transfer, itemId, paymentItemId)
                            if result == "Good":
                                self.log("SUCCESS", f"Successfully transferred credits")
                            else:
                                self.log("ERROR", f"Failed to transfer credits")
                        else:
                            self.log("ERROR", f"No account available for the credit transfer")
                    else:
                        self.log("ERROR", f"Failed to complete all {numberOfaccsBuying} initial purchases. Only {successful_purchases} were successful.")
                
                self.accounts_normal_with_tickets.sort(key=lambda x: int(x.split(':')[-1]))
                if self.accounts_with_credits_bool:
                    self.accounts_with_credits_with_tickets.sort(key=lambda x: int(x.split(':')[-1]))
            else:
                self.log("ERROR", "Failed to retrieve item details")
        except Exception as e:
            self.log("ERROR", f"An error occurred: {str(e)}")
        finally:
            while True:
                print("")
                self.log("INFO2", "MAKE SURE TO GO BACK AND USE THE CREDIT CHECKER TOOL")
                back_to_menu = input(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{self.timeNow}{Fore.WHITE}] ({Fore.LIGHTBLUE_EX}?{Fore.WHITE}) Do you want to go back to menu? [y/n]: {Fore.LIGHTBLUE_EX}").lower()
                if back_to_menu == 'y':
                    self.mainMenu()
                    break
                elif back_to_menu == 'n':
                    self.log("INFO", "Exiting the program.")
                    exit(0)
                else:
                    self.log("ERROR", "Invalid input. Please enter 'y' or 'n'.")

    def threaded_buy(self, number_of_accs, account_list, price, itemId, paymentItemId):
        queue = Queue()
        successful_purchases = 0
        lock = threading.Lock()
        stop_flag = threading.Event()
        available_accounts = list(account_list)
        buying_accounts = random.sample(available_accounts, number_of_accs)
        
        for acc in buying_accounts:
            available_accounts.remove(acc)
        for account in buying_accounts:
            queue.put(account)

        def worker():
            nonlocal successful_purchases
            while not stop_flag.is_set():
                try:
                    account = queue.get_nowait()
                except Empty:
                    break

                if stop_flag.is_set():
                    break

                result = self.buyItem(account, price, itemId, paymentItemId)

                with lock:
                    if result == "Good":
                        successful_purchases += 1
                        self.log("INFO", f"Purchase progress: {successful_purchases}/{number_of_accs}")
                        if successful_purchases >= number_of_accs:
                            self.log("SUCCESS", f"Reached target of {number_of_accs} successful purchases!")
                            stop_flag.set()
                    elif result in ["Couldn't Buy", "Error"]:
                        if account in buying_accounts:
                            buying_accounts.remove(account)
                            
                        with lock:
                            if available_accounts:
                                new_account = random.choice(available_accounts)
                                available_accounts.remove(new_account)
                                buying_accounts.append(new_account)
                                queue.put(new_account)
                                self.log("INFO", f"Replacing failed account with new account: {new_account.split(':')[0]}")
                            else:
                                self.log("ERROR", "No more available accounts to try")
                queue.task_done()

        thread_count = number_of_accs
        threads = [threading.Thread(target=worker, daemon=True) for _ in range(thread_count)]
        
        self.log("INFO", f"Starting {thread_count} threads for {number_of_accs} purchases")
        
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.log("INFO", f"Final results: {successful_purchases} successful purchases out of {number_of_accs} requested")
        
        return successful_purchases

    def buyItem(self, account, price, itemId, paymentItemId):
        try:
            username, token, sessionId, credits = account.split(":")[1:5]
            if int(credits) < price:
                self.log("ERROR", f"Insufficient credits for {username}")
                return "Low Credits"

            response = self.session.post(
                "https://public-ubiservices.ubi.com/v1/profiles/me/uplay/graphql",
                headers={
                    "Ubi-AppId": "80a4a0e8-8797-440f-8f4c-eaba87d0fdda",
                    "Authorization": f"ubi_v1 t={token}",
                    "Ubi-Sessionid": sessionId,
                    "Accept-Language": "en-US",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
                },
                data=dumps([{
                    "operationName": "CreateBuyOrder",
                    "variables": {
                        "spaceId": "0d2ae42d-4c27-4cb7-af6c-2099062302bb",
                        "tradeItems": [{"itemId": itemId, "quantity": 1}],
                        "paymentProposal": {"paymentItemId": paymentItemId, "price": price}
                    },
                    "query": "mutation CreateBuyOrder($spaceId: String!, $tradeItems: [TradeOrderItem!]!, $paymentProposal: PaymentItem!) {...}"
                }])
            )

            if any(state in response.text for state in ['"state":"Created",', '"state":"Succeeded"']):
                newCredits = int(credits) - price
                self.log("SUCCESS", f"Success, bought with {Fore.LIGHTGREEN_EX}{username}{Fore.WHITE} [{Fore.LIGHTGREEN_EX}{itemId}{Fore.WHITE} - Credits left: {Fore.LIGHTGREEN_EX}{newCredits}{Fore.WHITE} - Price: {Fore.LIGHTGREEN_EX}{price}{Fore.WHITE}]")
                return "Good"
            
            self.log("ERROR", f"Purchase failed for {username}")
            return "Couldn't Buy"

        except Exception as e:
            self.log("ERROR", f"Error in buyItem for {username}: {str(e)}")
            return "Error"

    def mainMenu(self):
        try:
            self.clear_console()
            total_accs_logged_in = len(self.accounts_normal_with_tickets) + len(self.accounts_with_credits_with_tickets)
            self.log("INFO", f"Logged in to {Fore.LIGHTBLUE_EX}{total_accs_logged_in}{Fore.WHITE} accounts")
            print("")
            self.log("1", "Credits checker")
            self.log("2", "Items checker")
            self.log("3", "Credits Transfer")
            self.log("4", "Credits Transfer (Automatic)")
            self.log("5", "Close tool")
            print("")
            option = input(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{self.timeNow}{Fore.WHITE}] ({Fore.LIGHTBLUE_EX}?{Fore.WHITE}) Option: {Fore.LIGHTBLUE_EX}")
            if option == "1":
                self.clear_console()
                updated_accounts = []

                for account in self.accounts_normal_with_tickets:
                    try:
                        email, username, token, sessionId = account.split(":")[:4]
                        credits = self.grabCreditsAmount(token, sessionId)
                        updated_accounts.append(f"{email}:{username}:{token}:{sessionId}:{credits}")
                    except Exception as e:
                        print(f"Error processing account {email}: {str(e)}")

                updated_accounts.sort(key=lambda x: int(x.split(':')[-1]))

                self.accounts_normal_with_tickets = updated_accounts

                for account in self.accounts_normal_with_tickets:
                    email, username, token, sessionId, credits = account.split(":")
                    self.log("INFO", f"Account (Normal): {Fore.LIGHTBLUE_EX}{email}{Fore.WHITE} - Username: {Fore.LIGHTBLUE_EX}{username}{Fore.WHITE} - Credits: {Fore.LIGHTBLUE_EX}{credits}{Fore.WHITE}")
                
                if self.accounts_with_credits_bool == True:
                    updated_accounts = []

                    for account in self.accounts_with_credits_with_tickets:
                        try:
                            email, username, token, sessionId = account.split(":")[:4]
                            credits = self.grabCreditsAmount(token, sessionId)
                            updated_accounts.append(f"{email}:{username}:{token}:{sessionId}:{credits}")
                        except Exception as e:
                            print(f"Error processing account {email}: {str(e)}")

                    updated_accounts.sort(key=lambda x: int(x.split(':')[-1]))

                    self.accounts_with_credits_with_tickets = updated_accounts

                    for account in self.accounts_with_credits_with_tickets:
                        email, username, token, sessionId, credits = account.split(":")
                        self.log("INFO", f"Account (For Auto): {Fore.LIGHTBLUE_EX}{email}{Fore.WHITE} - Username: {Fore.LIGHTBLUE_EX}{username}{Fore.WHITE} - Credits: {Fore.LIGHTBLUE_EX}{credits}{Fore.WHITE}")
                    
                while True:
                    back_to_menu = input(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{self.timeNow}{Fore.WHITE}] ({Fore.LIGHTBLUE_EX}?{Fore.WHITE}) Do you want to go back to menu? [y/n]: {Fore.LIGHTBLUE_EX}").lower()
                    if back_to_menu == "y":
                        self.mainMenu()
                        break
                    elif back_to_menu == "n":
                        _exit(0)
                    else:
                        self.log("ERROR", "Invalid input. Please enter 'y' or 'n'.")
                        
            elif option == "2":
                self.clear_console()
                itemId = input(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{self.timeNow}{Fore.WHITE}] ({Fore.LIGHTBLUE_EX}?{Fore.WHITE}) ItemID: {Fore.LIGHTBLUE_EX}")

                def process_accounts(accounts, account_type="Normal"):
                    for account in accounts:
                        try:
                            email, username, token, sessionId = account.split(":")[:4]
                            ownership_status = "HAS THE ITEM" if self.itemIsOwned(token, sessionId, itemId) else "DOES NOT HAVE THE ITEM"
                            color = Fore.LIGHTRED_EX if ownership_status == "HAS THE ITEM" else Fore.LIGHTGREEN_EX
                            self.log("INFO", f"Account ({account_type}): {Fore.LIGHTBLUE_EX}{email}{Fore.WHITE} - Username: {Fore.LIGHTBLUE_EX}{username}{Fore.WHITE} - {color}{ownership_status}{Fore.WHITE}")
                        except Exception as e:
                            self.log("ERROR", f"Error processing account: {str(e)}")

                process_accounts(self.accounts_normal_with_tickets)

                if self.accounts_with_credits_bool:
                    process_accounts(self.accounts_with_credits_with_tickets, "With Credits")
                
                while True:
                    back_to_menu = input(f"{Fore.WHITE}[{Fore.LIGHTBLACK_EX}{self.timeNow}{Fore.WHITE}] ({Fore.LIGHTBLUE_EX}?{Fore.WHITE}) Do you want to go back to menu? [y/n]: {Fore.LIGHTBLUE_EX}").lower()
                    if back_to_menu == "y":
                        self.mainMenu()
                        break
                    elif back_to_menu == "n":
                        _exit(0)
                    else:
                        self.log("ERROR", "Invalid input. Please enter 'y' or 'n'.")
                        
            elif option == "3":
                self.mode = "1"
                self.clear_console()
                self.getItemAllInfo()
            elif option == "4":
                self.mode = "2" 
                self.clear_console()
                self.getItemAllInfo()
            elif option == "5":
                _exit(0)
        except Exception as e:
            print(e)

    def mainFunction(self):
        self.clear_console()
        for email, password in self.accounts_normal:
            self.login(email, password, self.accounts_normal_with_tickets)
            print("")
        if self.accounts_with_credits_bool:
            for email, password in self.accounts_with_credits:
                self.login(email, password, self.accounts_with_credits_with_tickets)
                print("")
        if self.accounts_normal_with_tickets:
            self.accounts_normal_with_tickets.sort(key=lambda x: int(x.split(':')[-1]))
            for account in self.accounts_normal_with_tickets:
                credits = account.split(":")[-1]
                self.log("INFO", f"Account (Normal): {Fore.LIGHTBLUE_EX}{account.split(':')[0]}{Fore.WHITE} - Credits: {Fore.LIGHTBLUE_EX}{credits}{Fore.WHITE}")
            if self.accounts_with_credits_bool:
                self.accounts_with_credits_with_tickets.sort(key=lambda x: int(x.split(':')[-1]))
                for account in self.accounts_with_credits_with_tickets:
                    credits = account.split(":")[-1]
                    self.log("INFO", f"Account (For Auto): {Fore.LIGHTBLUE_EX}{account.split(':')[0]}{Fore.WHITE} - Credits: {Fore.LIGHTBLUE_EX}{credits}{Fore.WHITE}")
            time.sleep(1)
            self.mainMenu()
        else:
            self.log("ERROR", "No accounts loaded")
            input("")
            exit(0)

if __name__ == "__main__":
    ubisoft = Ubisoft("Accounts.txt", "AccountWCredits.txt")

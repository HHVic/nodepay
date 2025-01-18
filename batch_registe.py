# import requests
import random
import time
from utils import logger
from termcolor import colored
from captcha import Service2Captcha
from curl_cffi import requests



# 2Captcha API key
api_key = '替换成自己的key'  # Replace with your 2Captcha API key
registration_url = 'https://api.nodepay.org/api/auth/register?'

# Load proxy list
def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.readlines()
    logger.success(f'Found {len(proxies)} proxies')
    return [proxy.strip() for proxy in proxies]

# Load account information
def load_accounts(file_path):
    with open(file_path, 'r') as file:
        accounts = file.readlines()
    logger.success(f'Found {len(accounts)} accounts')
    return [account.strip().split(',') for account in accounts]

def _auth_headers():
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'chrome-extension://lgmpfmgeabnnlemejacfljbmonaomfmm',
        'priority': 'u=1, i',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'none',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }

# Batch register users
def batch_register_users(accounts, proxies):
    with open('token.txt', 'a') as token_file:
        for account in accounts:
            email, username, password = account

            # Randomly select a proxy
            proxy = random.choice(proxies)
            proxies_dict = {
                'http': proxy
            }
            logger.info(f'proxy: {proxies_dict}')

            try:
                # Get Cloudflare Turnstile solution
                captcha_service = Service2Captcha(api_key)
                captcha_token = captcha_service.get_captcha_token()

                # Construct registration data
                registration_data = {
                    "email": email,
                    "username": username,
                    "password": password,
                    "referral_code": "5Hj4Nul9wO3I3XB",  # Replace with actual referral code
                    "recaptcha_token": captcha_token
                }


                # Send registration request
                response = requests.post(registration_url, json=registration_data, headers=_auth_headers(), proxies=proxies_dict, impersonate="chrome110")
                response.raise_for_status()  # Check for HTTP errors

                # Check response content to confirm registration success
                if response.status_code == 200:
                    response_json = response.json()
                    if response_json.get('success'):
                        logger.success(f'{email} | Registered')
                        logger.info(f"{email} | Handled account!")
                        # Extract authorization token
                        auth_token = response.headers.get('authorization')
                        if auth_token:
                            token = auth_token.split(' ')[1]  # Get token after Bearer
                            token_file.write(f'{token}\n')
                    else:
                        logger.error(f'Failed to register user: {username}, Response: {response_json}')
                else:
                    logger.error(f'Failed to register user: {username}, Status code: {response.status_code}')

            except requests.exceptions.RequestException as e:
                logger.error(f'Error registering user {username}: {e}')
            except Exception as e:
                logger.error(f'Error solving captcha for user {username}: {e}')

            # Add delay between requests to avoid being blocked by the server
            time.sleep(1)

def get_choice():
        print("\n" + "="*50)
        print(colored("请选择:"))
        print(colored("1. 批量注册", "cyan"))
        print(colored("2. 批量登录", "cyan"))
        print(colored("3. 退出", "cyan"))
        print("="*50 + "\n")

def batch_register():
    # Load account information
    accounts = load_accounts('account.txt')
    # Load proxy list
    proxies = load_proxies('proxies.txt')
    logger.info("Starting account registration...")
    batch_register_users(accounts=accounts, proxies=proxies)



if __name__ == "__main__":

    get_choice()

    choice = input("Enter your choice: ").strip()
    if choice == '3':
        logger.info("Exiting.")
    elif choice == '1':
        batch_register()
    elif choice == '2':
        logger.warning("功能暂未开发，请等待....")
    else:
        logger.warning("看提示，不要瞎输入")

    # Batch register users
    # batch_register_users(accounts, proxies)

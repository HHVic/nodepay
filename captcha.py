import asyncio
from twocaptcha import TwoCaptcha

CAPTCHA_PARAMS = {
    'website_key': '0x4AAAAAAAx1CyDNL8zOEPe7',
    'website_url': 'https://app.nodepay.ai/login'
}

class Service2Captcha:
    def __init__(self, api_key):
        self.solver = TwoCaptcha(api_key)

    def get_captcha_token(self):
        captcha_token = self.solver.turnstile(sitekey=CAPTCHA_PARAMS['website_key'], url=CAPTCHA_PARAMS['website_url'])

        if 'code' in captcha_token:
            captcha_token = captcha_token['code']

        return captcha_token

    async def get_captcha_token_async(self):
        return await asyncio.to_thread(self.get_captcha_token)

    async def solve_captcha(self):
        return await self.get_captcha_token_async()
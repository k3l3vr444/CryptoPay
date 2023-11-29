import asyncio
import os

from crypto_pay.main import CryptoPay

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    cp = CryptoPay(os.getenv('crypto_pay_live_token'))
    rates = loop.run_until_complete(cp.exchange_rates())

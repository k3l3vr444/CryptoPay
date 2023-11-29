import logging
from _decimal import Decimal

from aiohttp import ClientSession

logger = logging.getLogger(__name__)


class CryptoPay:

    def __init__(self,
                 token: str,
                 test: bool = False):
        self.url = "https://testnet-pay.crypt.bot/" if test else "https://pay.crypt.bot/"
        self.headers: dict[str, str] = {"Crypto-Pay-API-Token": token}

    async def exchange_rate(self, source: str, target: str):
        rates = await self.exchange_rates()
        for item in rates["result"]:
            if item["target"] == target and item["source"] == source:
                return Decimal(item['rate'])
        raise ValueError

    async def exchange_rates(self):
        return await self._post(path="api/getExchangeRates")

    async def auth(self):
        return await self._post(path="api/getMe")

    async def create_invoice(self, currency: str, target: str, amount: int):
        exchange_rate = await self.exchange_rate(currency, target)
        data = {
            'asset': currency,
            'amount': str(amount / exchange_rate)
        }
        page_json = await self._post(path="api/createInvoice", data=data)
        return page_json['result']['pay_url'], page_json['result']['invoice_id']

    async def crypto_pay_check_invoice(self, invoice_id: int):
        data = {'invoice_ids': invoice_id}
        page_json = await self._post(path="api/getInvoices", data=data)
        if page_json['result']['items'][0]['status'] == 'paid':
            return True
        return False

    async def _post(self,
                    path: str,
                    data: dict = None) -> dict:
        async with ClientSession(headers=self.headers) as s:
            response = await s.post(f'{self.url}{path}', data=data)
            return await response.json(encoding="utf-8")

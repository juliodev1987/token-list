import requests
from web3 import Web3
from pycoingecko import CoinGeckoAPI
from constants import COINMARKETCAP_API_URL


class TokenList:
    def __init__(self):
        self.tokens = {}

    def start_get_tokens_from_coinmaketcap(self):
        page = 1
        per_page = 100
        is_end = False
        url = f"{COINMARKETCAP_API_URL}/cryptocurrency/listing"
        params = {
            "start": 1,
            "limit": per_page,
            "sortBy": "rank",
            "sortType": "desc",
            "convert": "USD",
            "cryptoType": "tokens",
            "tagType": "all",
            "audited": "false",
            "aux": "platform",
            # "tagSlugs": "binance-chain",
        }
        headers = {
            "content-type": "application/json",
            "accept": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }
        while not is_end:
            params["start"] = (page - 1) * per_page + 1
            try:
                res = requests.get(url, headers=headers, params=params)
                res_json = res.json()
                if res_json:
                    if 'data' in res_json and res_json['data'] and 'cryptoCurrencyList' in res_json['data'] and res_json['data']['cryptoCurrencyList']:
                        token_list = res_json['data']['cryptoCurrencyList']
                        for token in token_list:
                            if 'platform' in token:
                                platform_symbol = token['platform']['symbol']
                                platform_address = token['platform']['token_address']
                                token_symbol = token["symbol"]
                                market_cap = token["quotes"][0]["marketCap"]
                                if platform_symbol == 'BNB' and len(platform_address) == 42:
                                    print(token_symbol, market_cap, platform_address)
                                    self.tokens[token_symbol] = {
                                        "symbol": token_symbol,
                                        "address": Web3.toChecksumAddress(platform_address)
                                    }
                        page += 1
                    else:
                        is_end = True
            except Exception as e:
                print(f'Get {page} tokens failed', e)

        print(self.tokens)
        print(len(self.tokens))

    def start_get_tokens_from_coingecko(self):
        cg = CoinGeckoAPI()
        coins = cg.get_coins_list()
        for coin in coins:
            # print(coin)
            coin_detail = cg.get_coin_by_id(coin["id"])
            platforms = coin_detail['platforms']
            if 'binance-smart-chain' in platforms:
                token_symbol = coin_detail["symbol"]
                platform_address = platforms["binance-smart-chain"]
                print(platforms["binance-smart-chain"])
                self.tokens[token_symbol] = {
                    "symbol": token_symbol,
                    "address": Web3.toChecksumAddress(platform_address)
                }

        print(self.tokens)
        print(len(self.tokens))


if __name__ == '__main__':
    token_bot = TokenList()
    # token_bot.start_get_tokens_from_coinmaketcap()
    token_bot.start_get_tokens_from_coingecko()

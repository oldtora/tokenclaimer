from web3 import Web3
from dotenv import dotenv_values

# Загрузить переменные из файла .env
config = dotenv_values(".env")

# Установить переменные
PRIVATE_KEY_1 = config["PRIVATE_KEY_1"]
ADDRESS_1 = config["ADDRESS_1"]
PRIVATE_KEY_2 = config["PRIVATE_KEY_2"]
ADDRESS_2 = config["ADDRESS_2"]
TOKEN_ADDRESS = config["TOKEN_ADDRESS"]
TOKEN_ABI = config["TOKEN_ABI"]
GAS_PRICE = config["GAS_PRICE"]
GAS_LIMIT = config["GAS_LIMIT"]

# Создать объект Web3
w3 = Web3(Web3.HTTPProvider(config["WEB3_PROVIDER_URI"]))

# Получить экземпляр контракта токена
token_contract = w3.eth.contract(address=w3.toChecksumAddress(TOKEN_ADDRESS), abi=TOKEN_ABI)

# Функция для получения общего количества токенов на всех кошельках
def get_total_tokens():
    balance_1 = token_contract.functions.balanceOf(w3.toChecksumAddress(ADDRESS_1)).call()
    balance_2 = token_contract.functions.balanceOf(w3.toChecksumAddress(ADDRESS_2)).call()
    total_tokens = balance_1 + balance_2
    return total_tokens

# Установить значение TOTAL_TOKENS равным общему количеству токенов на всех кошельках
TOTAL_TOKENS = get_total_tokens()

# Функция для клейма токенов
def claim_tokens(private_key, address):
    # Получить аккаунт
    account = w3.eth.account.privateKeyToAccount(private_key)

    # Получить nonce
    nonce = w3.eth.getTransactionCount(account.address)

    # Получить значение gas price из конфигурации
    gas_price = int(GAS_PRICE)

    # Получить значение gas limit из конфигурации
    gas_limit = int(GAS_LIMIT)

    # Создать транзакцию
    tx = {
        'nonce': nonce,
        'to': TOKEN_ADDRESS,
        'value': 0,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'data': token_contract.functions.transferFrom(w3.toChecksumAddress(address), account.address, TOTAL_TOKENS).buildTransaction({'from': w3.toChecksumAddress(address)})['data'],
    }

    # Подписать транзакцию
    signed_tx = w3.eth.account.signTransaction(tx, private_key=private_key)

    # Отправить транзакцию
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    # Вывести хеш транзакции
    print(f"Transaction sent: {tx_hash.hex()}")

# Вызвать функцию для клейма токенов на первом кошельке
claim_tokens(PRIVATE_KEY_1, ADDRESS_1)

# Вызвать функцию для клейма токен

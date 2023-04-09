from web3 import Web3
from decimal import Decimal

# Указываем адрес контракта и его ABI
contract_address = "0x1234567890123456789012345678901234567890"
contract_abi = [ ... ]

# Указываем адреса кошельков и их соответствующие приватные ключи
wallet_addresses = ["0x...", "0x...", "0x...", "0x...", "0x..."]
private_keys = ["11..", "22..", "33..", "44..", "55.."]

# Устанавливаем провайдер для работы с блокчейном (в данном случае Infura)
w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/your-infura-project-id'))

# Получаем объект контракта
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Получаем информацию о количестве токенов на каждом кошельке
total_tokens = 0
for i, wallet_address in enumerate(wallet_addresses):
    balance = contract.functions.balanceOf(wallet_address).call()
    total_tokens += balance
    print(f"Wallet {i+1}: {balance} tokens")

# Получаем текущую среднюю стоимость газа
gas_price = w3.eth.gas_price

# Устанавливаем максимальный лимит газа, который мы готовы заплатить
gas_limit = w3.toWei(50, 'gwei')

# Проверяем, достаточно ли токенов на наших кошельках для клейма
if total_tokens < contract.functions.TOTAL_SUPPLY().call():
    print("Not enough tokens to claim")
    exit()

# Вычисляем количество токенов, которые мы можем заклеймить, учитывая максимальный лимит газа
claimable_tokens = 0
for i, wallet_address in enumerate(wallet_addresses):
    balance = contract.functions.balanceOf(wallet_address).call()
    gas_required = contract.functions.claim.estimateGas({'from': wallet_address})
    gas_cost = gas_required * gas_price
    if gas_cost <= gas_limit:
        claimable_tokens += balance
        print(f"Wallet {i+1} can claim {balance} tokens")
    else:
        max_claimable_tokens = int((gas_limit / gas_price) * 0.9)  # учитываем комиссию за транзакцию

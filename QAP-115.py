money = int(input("Введите сумму: "))
per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}

deposit = [int(money * per_cent_value / 100) for per_cent_value in per_cent.values()]

max_deposit = max(deposit)
max_deposit_bank = list(per_cent.keys())[deposit.index(max_deposit)]

print("Накопленные средства в банках:", deposit)
print(f"Максимальная сумма, которую вы можете заработать - {max_deposit} в банке {max_deposit_bank}")

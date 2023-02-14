per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}
money=float(input ("Введите сумму: "))
deposit = []
#формируем список с процентами
for key, value in per_cent.items():
     deposit.append(int(value*money/100))
print ("Максимальная сумма, которую вы можете заработать —", max(deposit))

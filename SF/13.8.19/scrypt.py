b = int(input("Введите количество желаемых билетов: "))
sum = 0
#tickets price
for i in range (b):
    age =  int(input("Введите ваш возраст: "))
    if age > 25:
        sum += 1390
    elif age < 25 and age > 18:
        sum += 990
#discount
if b > 3:
    sum = sum - ((sum / 100) * 10)
print ("Итоговая стоимость: ", int(sum))
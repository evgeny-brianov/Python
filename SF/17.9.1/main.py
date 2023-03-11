lst = []
lst = [int(item) for item in input("Введите список чисел: ").split()]
b = int(input("Введите число: "))

def sortlst(lst):
    lst.sort()
    return lst

lstsorted = sortlst(lst)

def binary_search(x, a):
    lo = 0
    hi = len(a)
    length = len(a)

    # если в списке всего один элемент
    if hi == 1:
        if a[0] < x:
            return 0;
        else:
            return -1;

    # алгоритм бинарного поиска
    while lo < hi:
        mid = (lo + hi) // 2

        # элемент диапазона меньше поискового,а следующий больше или равен - значит результат найден
        if a[mid] < x and (mid+1) < length and a[mid+1] >= x:
            return mid;
        # идем в правую половину диапазона
        elif a[mid] < x:
            lo = mid + 1
        # идем в левую половину диапазона
        elif a[mid] > x:
            hi = mid
        # элемент диапазона больше или равен поискового, а предыдущий меньше -  значит результат найден
        elif a[mid] >= x and a[mid-1] < x:
            return mid-1;
        else:
            return -1;

    return -1

result = binary_search(b, lstsorted)
if result == -1:
    print("Не соответствие условию")
else:
    print(result)





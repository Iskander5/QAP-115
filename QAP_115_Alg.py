def binary_search(array, num):
    left = 0
    right = len(array) - 1
    if left > right:
        return False

    while left <= right:
        middle = (right + left) // 2
        if array[middle] == num:
            return middle
        elif num < array[middle]:
            right = middle - 1
        else:
            left = middle + 1
    return left

def main():
    sequence = input("Введите последовательность чисел через пробел: ")
    sequence = sequence.split()
    try:
        sequence = [int(num) for num in sequence]
    except ValueError:
        print("Некорректный ввод данных")
        return


    num = input("Введите число, которое необходимо найти: ")
    try:
        num = int(num)
    except ValueError:
        print("Некорректный ввод данных")
        return


    sequence.sort()



    index = binary_search(sequence, num)

    if index >= len(sequence) or sequence[index] != num:
        print("Число не найдено в последовательности")
    else:
        print(f"Искомое число находится на позиции {index}")

main()










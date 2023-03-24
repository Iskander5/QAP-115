tickets = int(input("Введите количество билетов:"))
if tickets <= 0:
    print("Количество билетов должно быть больше нуля!")
else:
    price_tickets = 0
    for i in range(tickets):
        age = int(input("Введите возраст посетителя:"))
        if age >= 25:
            price_tickets += 1350
        elif age >= 18:
            price_tickets += 990
        else:
            continue
    if tickets >= 4 and price_tickets > 0:
        print("Полная стоймость билетов с учетом скидки: ", int(price_tickets * 0.9))
    elif tickets < 4 and price_tickets == 0:
        print("Для несовершеннолетних билеты бесплатно!")
    else:
        print("Стоимость без учета скидки: ", price_tickets)



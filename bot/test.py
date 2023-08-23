PAYMENTS = {
    1: [1,]
}

user_id = 1
tour_id = 1
if user_id not in PAYMENTS or tour_id not in PAYMENTS[user_id]:
    print("Вы не оплатили!")
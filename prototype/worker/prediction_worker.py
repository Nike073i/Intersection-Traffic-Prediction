async def prediction_worker(get_messages, predict, ack_message, save_prediction):
    while True:
        try:
            messages = get_messages()
            if messages:
                for message in messages:
                    prediction = predict(message.time, message.crossroad_id)
                    save_prediction(message.prediction_id, message.crossroad_id, message.time, prediction)
                    ack_message(message.id)
            else:
                print("Сообщений нет")

        except Exception as e:
            print(f"Error: {e}")
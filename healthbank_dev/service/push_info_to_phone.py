from pyfcm import FCMNotification

def pytofirebase (tokens, message):
    push_service = FCMNotification(api_key="AAAAbBSI_Jk:APA91bEiwG1Ihi9rqFum10_5njRzlXn6FMz9m57cHP3XJq2IMnegmC9llViv2yF757-kZG4wfKE9hstcSvLMv0KU3_4mA9ChE9J5s0YjplsdDxSPhRWXE1F_EBAXp7mwFy9XH27KBKyc")

    registration_ids = tokens
    message_title = "we are family推播提醒"
    message_body = message
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
    print (result)

if __name__ == "__main__":
    tokens = []
    message = "test"
    pytofirebase(tokens, message)
import vk_api


def auth_handler():
    """ При двухфакторной аутентификации вызывается эта функция. """

    # Код двухфакторной аутентификации,
    # который присылается по смс или уведомлением в мобильное приложение
    key = input("Enter authentication code: ")
    # Если: True - сохранить, False - не сохранять.
    remember_device = True

    return key, remember_device


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(
        login, password,
        # функция для обработки двухфакторной аутентификации
        auth_handler=auth_handler
    )

    try:
        d = {}
        vk_session.auth(token_only=True)
        vk = vk_session.get_api()
        response = vk.friends.get(fields="bdate, city")
        if response['items']:
            for el in response['items']:
                surname = el['last_name']
                birthday = el.get('bdate', 'нет')
                d[surname] = birthday
        for el in sorted(d):
            for s in response['items']:
                if s['last_name'] == el:
                    print(el, s['first_name'], d[el])

    except vk_api.AuthError as error_msg:
        print(error_msg)
        return


if __name__ == '__main__':
    main()

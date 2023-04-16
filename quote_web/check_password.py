def check_password(password):
    digits = '1234567890'
    upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_letters = 'abcdefghijklmnopqrstuvwxyz'
    symbols = '!@#$%^&*()-+'
    acceptable = digits + upper_letters + lower_letters + symbols
    if len(password) > 30:
        return False, 'Максимальная длина пароля - 30'
    passwd = set(password)
    if any(char not in acceptable for char in passwd):
        return False, 'Ошибка. Запрещенный спецсимвол'
    else:
        recommendations = []
        if len(password) < 7:
            recommendations.append(f'увеличить число символов - {7 - len(password)}')
        for what, message in ((digits, 'цифру'),
                              (symbols, 'спецсимвол'),
                              (upper_letters, 'заглавную букву'),
                              (lower_letters, 'строчную букву')):
            if all(char not in what for char in passwd):
                recommendations.append(f'добавить 1 {message}')

        if recommendations:
            return False, "Слабый пароль. Рекомендации: " + ", ".join(recommendations)
        else:
            return True, 'Сильный пароль.'

def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )

    def step2_umbrella():
        print('На поиски зонтика в жилище утки ушло некоторое время,\n'
              'и в бар она пошла позже, чем планировала. Когда она пришла,\n'
              'села за столик, заказала виски с колой, к ней внезапно подсел заяц в шляпе.\n'
              '"Вы же та самая утка-маляр?! Не покрасите мне дом? Я заплачу!" ')

        def step3_paint():
            print('"Хм, какую бы цену ему предложить?"\n'
                  'Введите цену: ')
            price = float(input())  # number input
            if 0 < price <= 1000:
                print('"Да, я согласен на цену в {}", сказал заяц.\n'
                      'Утка покрасила зайцу дом, он был очень доволен работой.\n'
                      'А утка получила возможность и дальше ходить по барам.\n'
                      'FIN '.format(price))
            elif price > 1000:
                print('"Нет, платить {} - для меня многовато. Жаль.\n'
                      'Утка не расстроилась, и вскоре после выпивки отправилась домой.\n'
                      'FIN '.format(price))
            else:
                print('Да не, бред какой-то...')
                return step3_paint()

        def step3_no_paint():
            print('Расстроенный заяц собрался уходить. Он не выглядел обиженным,\n'
                  'скорее, разочарованным. Быть может, утка передумает? ')

            def step4_paint():
                print('"Почему бы и нет", подумала утка? "Дам ему шанс."\n'
                      '"Сколько платишь?"\n'
                      'Введите цену:')
                price = float(input())  # number input
                if 0 <= price <= 500:
                    print('"Мало, извини."\n'
                          'Допив виски, утка отправилась домой, ни о чем не жалея.\n'
                          'FIN ')
                elif 500 < price <= 1000:
                    print('"Хорошо, я согласна."\n'
                          'Однако, утка не выполнила работу так хорошо, как могла бы. Капитализм на дворе!\n'
                          'Но заяц все равно выглядел счастливым.\n'
                          'FIN ')
                elif price > 1000:
                    print('Утка выполнила работу как-будто для себя. Все были довольны.\n'
                          'FIN ')
                else:
                    print("Oh no, oh no, oh no no no no no!")
                    return step4_paint()

            option = ''
            options = {'да': True, 'нет': False}
            while option not in options:
                print('Выберите: {}/{}'.format(*options))
                option = input()

            if options[option]:
                return step4_paint()
            print('Допив виски, и подумав о жизни, утка в приподнятом настроении\n'
                  'вернулась домой, не промокнув.\n'
                  'FIN ')

        option = ''
        options = {'да': True, 'нет': False}
        while option not in options:
            print('Выберите: {}/{}'.format(*options))
            option = input()

        if options[option]:
            return step3_paint()
        return step3_no_paint()

    def step2_no_umbrella():
        print('У барной стойки к утке подсел некий медведь в деловом костюме.\n'
              'Он не представился, а лишь заявил:\n'
              '"Я медведь-волшебник. Сыграем в игру! Если назовешь мне слово-палиндром, я дам тебе подарок!" '
              )

        def step3_palindrom():
            print('"Ого, молодец! Теперь выбери подарок. Назови любое натуральное число от 1 до 4."\n')
            present = int(input())
            if present == 1:
                print('"Твой подарок - зонтик! Удачи!"\n'
                      'Отличный выбор! Утка вернулась домой в хорошем настроении,'
                      'совсем не промокнув.\n'
                      'FIN ')
            elif present == 2:
                print('"Твой подарок - эта куртка с капюшоном. Ни пуха!"\n'
                      'Неплохо! Утка вернулась домой в хорошем настроении,'
                      'совсем не промокнув.\n'
                      'FIN ')
            elif present == 3:
                print('"Твой подарок - новая кружка. Ну как?"\n'
                      'Хм, интересно. Правда, это не помогло утке не намокнуть,'
                      'пока она возвращалась домой...\n'
                      'FIN ')
            elif present == 4:
                print('"Ты получаешь эту шляпу! Хорошо выглядишь!"\n'
                      'Не поможет под дождем, но выглядит и правда неплохо...\n'
                      'FIN ')
            else:
                print('Это не натуральное число от 1 до 4 :(\n'
                      'Давай по новой, все фигня! ')
                return step3_palindrom()

        print('Какое же слово назвать утке?')  # string input
        answer = input()
        if answer[::-1] == answer:
            return step3_palindrom()
        else:
            print('К сожалению, данное слово не является палиндромом. Утка осталась без подарка.\n'
                  'Медведь ушел, а утка решила, что ей нужно больше читать книг, а не ходить по барам.\n'
                  'Домой утка вернулась, вымокнув до нитки.\n'
                  '"Эх, а ведь подарком мог быть зонтик..."\n'
                  'FIN '
                  )

    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()

    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()


if __name__ == '__main__':
    step1()

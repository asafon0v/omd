import csv
import typing as tp


def option_1(data_file: tp.Optional[csv.DictReader] = None) -> tp.Optional[list]:
    # Нормально отображается только с такими пробелами, и то со сдвигом вправо в консоли...
    """        Показывает иерархию команд (отделов) департаментов в понятном виде. На вход
    подается считанный файл, где каждая строка уже преобразована в словарь. На выход
    идет небольшой отчет в виде департаментов и соответствующих им команд (отделов).
    Если на вход не передано ничего, возвращает None.
    """
    if data_file is None:
        return None
    dc_commands = dict()
    for row in data_file:
        if row['Департамент'] not in dc_commands.keys():
            dc_commands[row['Департамент']] = [row['Отдел']]
        elif (row['Департамент'] in dc_commands.keys()) and (row['Отдел'] not in dc_commands[row['Департамент']]):
            dc_commands[row['Департамент']].append(row['Отдел'])
        else:
            continue
    res = []
    for k, v in dc_commands.items():
        if v:
            res.append(f'В департамент "{k}" входят следующие команды(отделы): {", ".join(v)}.')
        else:
            res.append(f'В департаменте "{k}" команд нет!')
    return res


def option_2(data_file: tp.Optional[csv.DictReader] = None) -> tp.Optional[dict]:
    """        Выводит сводный отчет по департаментам в виде набора данных:
    численность; максимальная, минимальная, и средняя зарплаты для каждого департамента.
    Если на вход не передано ничего, возвращает None.
    Если в заполнении зарплаты сотрудника обнаруживается ошибка, сообщает о ней, при этом данный сотрудник
    не учитывается в отчете.
    """
    if data_file is None:
        return None
    dc_deps = dict()
    for row in data_file:
        if row['Оклад'].isdigit():
            zp_curr = int(row['Оклад'])
        else:
            print(f'У работника "{row["ФИО полностью"]}"', '\n'
                  f'департамента "{row["Департамент"]}"', '\n'
                  f'отдела "{row["Отдел"]}"', '\n'
                  f'некорректно задана зарплата!', '\n'
                  f'Он не будет учтен в численности сотрудников!')
            continue
        if row['Департамент'] not in dc_deps.keys():
            dc_deps[row['Департамент']] = {'Численность': 1, 'Минимальная зарплата': zp_curr,
                                           'Максимальная зарплата': zp_curr, 'Средняя зарплата': zp_curr}
        else:
            dc_deps[row['Департамент']]['Численность'] += 1
            dc_deps[row['Департамент']]['Средняя зарплата'] += zp_curr
            if zp_curr < dc_deps[row['Департамент']]['Минимальная зарплата']:
                dc_deps[row['Департамент']]['Минимальная зарплата'] = zp_curr
            if zp_curr > dc_deps[row['Департамент']]['Максимальная зарплата']:
                dc_deps[row['Департамент']]['Максимальная зарплата'] = zp_curr
    for v in dc_deps.values():
        v['Средняя зарплата'] /= v['Численность']
        v['Средняя зарплата'] = round(v['Средняя зарплата'], ndigits=4)
    return dc_deps


def option_3(path: tp.Optional[str] = None, data_file: tp.Optional[csv.DictReader] = None) -> None:
    """        Записывает сводный отчет по департаментам в csv-файл по указанному пути в виде набора данных:
    численность; максимальная, минимальная, и средняя зарплаты для каждого департамента.
    Если на вход не передано ничего, сообщает об этом.
    Если в заполнении зарплаты сотрудника обнаруживается ошибка, сообщает о ней, при этом данный сотрудник
    не учитывается в отчете.
    """
    report = option_2(data_file)
    if report is None or path is None:
        print(f'На вход не передано ничего, нечего сохранять! Также проверьте, что вы ввели путь сохранения файла!')
    else:
        with open(path, mode='w', encoding='utf-8') as w_file:
            names = ['Департамент', 'Численность', 'Минимальная зарплата', 'Максимальная зарплата',
                     'Средняя зарплата']
            file_writer = csv.DictWriter(w_file, delimiter=";",
                                         lineterminator="\r", fieldnames=names)
            file_writer.writeheader()
            for k, v in report.items():
                r_curr = {'Департамент': k}
                r_curr.update([(kn, vn) for kn, vn in v.items()])
                file_writer.writerow(r_curr)


def program_start() -> None:
    """Запускает работу программы с выбором опции и возможностью отменить необходимость выбора."""
    with open('C:\\Data\\Corp_Summary.csv', encoding='utf-8') as r_file:
        reader = csv.DictReader(r_file, delimiter=';')
        print(f'Категорически Вас приветствую! Выберите одну из следующих опций (введите номер):', '\n'
              f'1. Вывести отчет по департаментам и командам, входящим в каждый из них.', '\n'
              f'2. Вывести отчет по департаментам, содержащий информацию о численности персонала', '\n'
              f'и зарплатах каждого департамента.', '\n'
              f'3. Сохранить отчет из пункта 2 по указанному пути в виде csv-файла.', '\n'
              f'4. Отменить выбор и завершить работу программы.')
        chosen_task = input()
        if chosen_task == '1':
            print("\n".join(option_1(data_file=reader)) + "\n")
            program_start()
        elif chosen_task == '2':
            for k, v in option_2(data_file=reader).items():
                print(f'В департаменте "{k}" численность составляет {v["Численность"]} человек,', '\n'
                      f'минимальная зарплата составляет {v["Минимальная зарплата"]} д.е.,', '\n'
                      f'максимальна зарплата составляет {v["Максимальная зарплата"]} д.е.,', '\n'
                      f'средняя зарплата составляет {v["Средняя зарплата"]} д.е.', '\n')
            program_start()
        elif chosen_task == '3':
            print(f'Введите путь к файлу, в который нужно записать отчет:')
            chosen_path = input()
            option_3(path=chosen_path, data_file=reader)
            program_start()
        elif chosen_task == '4':
            print(f'Выбор отменен. Программа завершила работу.')
            return None
        else:
            print(f'Вы ввели кринж! Если хотите отменить необходимость ввода, введите 4.', '\n'
                  f'Программа перезапустится, а вы выберите опцию заново.')
            program_start()


# "C:\\Data\\test_hw2_ex.csv"
if __name__ == '__main__':
    program_start()

from typing import List, Union
from collections import Counter


class CountVectorizer:
    """
    Данный класс позволяет работать со списком строк, строя по нему терм-документную матрицу,
    т.е. матрицу, где для совокупности строк посчитаны количества вхождений уникальных слов в каждую строку,
    независимо от регистра (верхний и нижний регистры идентичны).

    Единственный атрибут класса здесь - список особых знаков, удаляемых из строк, spec_chars.

    Атрибуты экземпляра класса здесь:
    input_strings - список строк, подаваемый на вход;
    clear_split_strings - список входных строк с удаленными особыми знаками, где
    каждая строка разибта на слова по пробелам;
    words_stack - совокупность уникальных слов всей совокупности строк (list);
    td_matrix - терм-документная матрица.
    """
    spec_chars = '''?!@#$%^&*+=()№<>:;'"{}[].,/\|~`'''

    def __init__(self):
        self.input_strings = None
        self.clear_split_strings = None
        self.words_stack = None
        self.td_matrix = None

    def get_feature_names(self) -> List[str]:
        """
        Возвращает список уникальных слов (с удаленными особыми знаками) из совокупности входных строк,
        где слова отсортированы в лексикографическом порядке.

        """
        return self.words_stack

    @classmethod
    def _clearer(cls, string: str) -> List[str]:
        """
        Очищает строку от особых знаков и разбивает ее на слова.
        """
        for char in cls.spec_chars:
            string = string.replace(char, ' ')
        return string.split()

    def fit_transform(self, input_strings: List[str]) -> Union[str, List[List[int]]]:
        """
        Считывает список входных строк, создает по ним терм-документную матрицу,
        а также другие атрибуты (список уникальных слов и др., см. описание класса).
        """
        if input_strings:
            self.input_strings = list(map(lambda w: w.lower(), input_strings))
            self.clear_split_strings = list(map(self._clearer, self.input_strings))
            self.words_stack = set()
            self.words_stack.update(*self.clear_split_strings)
            self.words_stack = list(self.words_stack)
            self.words_stack.sort()
            self.td_matrix = []
            if self.clear_split_strings:
                for l_words in self.clear_split_strings:
                    word_cnter = Counter(l_words)
                    self.td_matrix.append([word_cnter[word] for word in self.words_stack])
            return self.td_matrix
        else:
            return 'Список входных строк пуст.'


if __name__ == '__main__':
    # Test 1
    print('Test 1:')
    input_strings_test_1 = ['hi, my name is', 'my name is', 'my name is', 'chika-chika Slim Shady!']
    obj_test_1 = CountVectorizer()
    matrix_test_1 = obj_test_1.fit_transform(input_strings_test_1)
    words_stack_test_1 = obj_test_1.get_feature_names()
    assert words_stack_test_1 == ['chika-chika', 'hi', 'is', 'my', 'name', 'shady', 'slim']
    assert matrix_test_1 == [[0, 1, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 0, 0], [0, 0, 1, 1, 1, 0, 0], [1, 0, 0, 0, 0, 1, 1]]
    print(f'Список строк - {input_strings_test_1}')
    print(f'Матрица: {matrix_test_1}')
    print(f'Набор слов: {words_stack_test_1}')
    print()

    # Test 2
    print('Test 2:')
    input_strings_test_2 = ['Мой город вне времени (времени)', 'вне территории, племени, рода, империи',
                            ' ', '', ',,,', '!@#', 'Троя, троя, Троя', 'Помпеи, Рим!']
    obj_test_2 = CountVectorizer()
    matrix_test_2 = obj_test_2.fit_transform(input_strings_test_2)
    words_stack_test_2 = obj_test_2.get_feature_names()
    assert words_stack_test_2 == ['вне', 'времени', 'город', 'империи', 'мой', 'племени', 'помпеи',
                                  'рим', 'рода', 'территории', 'троя']
    assert matrix_test_2 == [[1, 2, 1, 0, 1, 0, 0, 0, 0, 0, 0], [1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0]]
    print(f'Список строк - {input_strings_test_2}')
    print(f'Матрица: {matrix_test_2}')
    print(f'Набор слов: {words_stack_test_2}')
    print()

    # Test 3
    print('Test 3:')
    input_strings_test_3 = ["i'm not afraid, ", "i'm not afraid", 'to take a stand', 'take a stand',
                            'everybody, everybody', 'come take my hand, come take my hand!']
    obj_test_3 = CountVectorizer()
    matrix_test_3 = obj_test_3.fit_transform(input_strings_test_3)
    words_stack_test_3 = obj_test_3.get_feature_names()
    assert words_stack_test_3 == ['a', 'afraid', 'come', 'everybody', 'hand', 'i', 'm', 'my', 'not', 'stand', 'take',
                                  'to']
    assert matrix_test_3 == [[0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0], [0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0],
                             [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
                             [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 2, 0, 0, 2, 0, 0, 2, 0]]
    print(f'Список строк - {input_strings_test_3}')
    print(f'Матрица: {matrix_test_3}')
    print(f'Набор слов: {words_stack_test_3}')
    print()

    # Final test
    print('Final test:')
    input_strings_test_4 = []
    obj_test_4 = CountVectorizer()
    matrix_test_4 = obj_test_4.fit_transform(input_strings_test_4)
    words_stack_test_4 = obj_test_4.get_feature_names()
    print(f'Список строк - {input_strings_test_4}')
    print(f'Матрица: {matrix_test_4}')
    print(f'Набор слов: {words_stack_test_4}')

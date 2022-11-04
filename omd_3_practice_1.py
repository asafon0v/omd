from typing import List, Union
from collections import Counter
from math import log


class CountVectorizer:
    """
    Данный класс позволяет работать со списком строк,
    строя по нему терм-документную матрицу,
    т.е. матрицу, где для совокупности строк посчитаны количества
    вхождений уникальных слов в каждую строку,
    независимо от регистра (верхний и нижний регистры идентичны).

    Единственный атрибут класса здесь - список особых знаков,
    удаляемых из строк, spec_chars.

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
        Возвращает список уникальных слов (с удаленными особыми знаками)
        из совокупности входных строк,
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


class TfidfTransformer:
    """
    Содержит операции tf, idf, tf-idf.
    """

    def __init__(self):
        self.tf_idf_matrix = None

    def tf_transform(self, count_matrix: List[List[int]]) -> List[List[float]]:
        """
        Вычисляет tf-матрицу по терм-документной матрице.
        """
        tf_mat = []
        if count_matrix:
            for cm_row in count_matrix:
                tf_mat.append(list(map(lambda w: round(w / sum(cm_row), ndigits=3), cm_row)))
        return tf_mat

    def idf_transform(self, count_matrix: List[List[int]]) -> List[float]:
        """
        Вычисляет idf-матрицу по терм-документной матрице.
        """
        idf_mat = []
        if count_matrix:
            total_documents = len(count_matrix)
            for i in range(len(count_matrix[0])):
                word_doc_count = sum(count_matrix[j][i] > 0 for j in range(total_documents))
                idf_value = log((1 + total_documents) / (1 + word_doc_count)) + 1
                idf_mat.append(round(idf_value, ndigits=3))
        return idf_mat

    def fit_transform(self, count_matrix: List[List[int]]) -> List[List[float]]:
        """
        Вычисляет tf-idf-матрицу по терм-документной матрице.
        """
        tf_idf_mat = []
        if count_matrix:
            tf_mat = self.tf_transform(count_matrix)
            idf_mat = self.idf_transform(count_matrix)
            tf_idf_mat = list(map(lambda w: [round(elm[0] * elm[1], ndigits=3)
                                             for elm in zip(idf_mat, w)], tf_mat))
        return tf_idf_mat


class TfidfVectorizer(CountVectorizer, TfidfTransformer):
    """
    Совмещает в себе методы CountVectorizer и TfidfTransformer
    с помощью наследования от оных.
    Имеет метод вычисления матрицы tf-idf и атрибут с этой матрицей.
    """

    def __init__(self):
        super().__init__()
        self.tf_idf_matrix = None

    def fit_transform(self, text_corpus: List[str]) -> List[List[float]]:
        """
        Вычисляет tf-idf матрицу по имеющемуся корпусу.
        """
        super().fit_transform(text_corpus)
        self.tf_idf_matrix = TfidfTransformer.fit_transform(self, self.td_matrix)
        return self.tf_idf_matrix


if __name__ == '__main__':
    # Тест 1
    corpus = ['Crock Pot Pasta Never boil pasta again',
              'Pasta Pomodoro Fresh ingredients Parmesan to taste']
    print('Входные строки:')
    for st in corpus:
        print(st)
    print()
    tf_idf_obj = TfidfVectorizer()
    tf_idf_matrix = tf_idf_obj.fit_transform(corpus)
    words_stack = tf_idf_obj.get_feature_names()
    assert words_stack == ['again', 'boil', 'crock', 'fresh', 'ingredients',
                           'never', 'parmesan', 'pasta', 'pomodoro', 'pot',
                           'taste', 'to'], \
        'Ошибка в полном наборе слов'
    print('Все слова:')
    print(words_stack)
    print()
    assert tf_idf_matrix == [[0.201, 0.201, 0.201, 0.0, 0.0, 0.201, 0.0,
                              0.286, 0.0, 0.201, 0.0, 0.0],
                             [0.0, 0.0, 0.0, 0.201, 0.201, 0.0, 0.201,
                              0.143, 0.201, 0.0, 0.201, 0.201]], \
        'Ошибка в tf_idf матрице'
    print('Выводим tf_idf матрицу:')
    for st in tf_idf_matrix:
        print(st)

    # Test 2
    corpus2 = []
    tf_idf_obj2 = TfidfVectorizer()
    tf_idf_matrix2 = tf_idf_obj2.fit_transform(corpus2)
    words_stack2 = tf_idf_obj2.get_feature_names()
    assert words_stack2 is None, 'Ошибка в полном наборе слов'
    assert tf_idf_matrix2 == [], 'Ошибка в tf_idf матрице'
    print()
    print('Выводим tf_idf матрицу 2:')
    print(tf_idf_matrix2)

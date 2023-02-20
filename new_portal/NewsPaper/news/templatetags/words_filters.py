from django import template


register = template.Library()


CURSE_WORDS = {
    "америка": "а******", "аэростат": "а*******",
    "задач": "з****", "разлом": "р*****", "сервис": "с*****"
}


try:
    @register.filter()
    def curse(value):
        for i, j in CURSE_WORDS.items():
            value = value.replace(i, j)
        return value
except TypeError:
    print('Исключение TypeError! Фильтр цензурирования применялся только к переменным строкового типа!')
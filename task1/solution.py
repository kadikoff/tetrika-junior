import inspect
from typing import Union, Type, Any
import functools


def strict(func):
    """Декоратор проверяет соответствие типов переданных в вызов функции
    аргументов типам аргументов, объявленным в прототипе функции.

    При несоответствии типов вызывается исключение TypeError.

    Ключевые проверки:
    - проверка типов переданных аргументов;
    - проверка типа возвращаемого значения;
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)  # (a: int, b: int) -> int
        bound_args = signature.bind(*args, **kwargs)  # <BoundArguments (a=1, b=2)>
        # Ввиду того, что аннотации могут поменять на ходу (func.__annotations__ = ...),
        # получаем теперь их из wrapper. Если аннотации не менялись, тогда получаем
        # оригинальные из самой функции func.
        annotations = wrapper.__annotations__ if hasattr(wrapper, '__annotations__') else func.__annotations__

        def _validate_type(name, value, expected_type):
            """Проверка типов переданных данных"""
            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Значение '{name} = {value}' должен быть типа '{expected_type.__name__}', "
                    f"но не '{type(value).__name__}'"
                )

        # Проверка типов переданных аргументов
        for arg_name, arg_value in bound_args.arguments.items():
            expected_type = annotations[arg_name]
            _validate_type(name=arg_name, value=arg_value, expected_type=expected_type)

        # Проверка типа возвращаемого значения
        # В задании не было
        # гарантировано, что тип возвращаемого значения в функции будет указан. Если он не указан - по умолчанию
        # принимаем типы данных, указанных на позиции дефолтных значений в функции get.
        result = func(*args, **kwargs)
        expected_return_type = annotations.get("return", Union[bool, int, float, str])
        _validate_type(name="return", value=result, expected_type=expected_return_type)

        return result

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    print(sum_two(1, 2))  # >>> 3
    print(sum_two(1, 2.4))  # >>> TypeError

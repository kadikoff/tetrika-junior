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
        annotations: dict[str, Type[Any]] = func.__annotations__  # {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}

        # Проверка типов переданных аргументов
        for arg_name, arg_value in bound_args.arguments.items():
            expected_type = annotations[arg_name]
            current_type = type(arg_value)
            if not isinstance(arg_value, expected_type):
                raise TypeError(
                    f"Аргумент '{arg_name} = {arg_value}' должен быть типа '{expected_type.__name__}', "
                    f"но не '{current_type.__name__}'"
                )

        # Проверка типа возвращаемого значения
        # В задании не было
        # гарантировано, что тип возвращаемого значения в функции будет указан. Если он не указан - по умолчанию
        # принимаем типы данных, указанных на позиции дефолтных значений в функции get.
        result = func(*args, **kwargs)
        expected_return_type = annotations.get("return", Union[bool, int, float, str])
        current_return_type = type(result)
        if not isinstance(result, expected_return_type):
            raise TypeError(
                f"Возвращаемый результат '{result}' должен быть типа '{expected_return_type.__name__}', "
                f"но не '{current_return_type.__name__}'"
            )

        return result

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


if __name__ == "__main__":
    print(sum_two(1, 2))  # >>> 3
    print(sum_two(1, 2.4))  # >>> TypeError

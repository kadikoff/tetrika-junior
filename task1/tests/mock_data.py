correct_test_cases = [
    {
        "annotations": {"a": int, "b": int, "return": int},
        "args": (4,),
        "kwargs": {"b": 3},
    },
    {
        "annotations": {"a": float, "b": float, "return": float},
        "args": (4.4,),
        "kwargs": {"b": 3.3},
    },
    {
        "annotations": {"a": bool, "b": bool, "return": int},
        "args": (True,),
        "kwargs": {"b": True},
    },
    {
        "annotations": {"a": str, "b": str, "return": str},
        "args": ("Hello ",),
        "kwargs": {"b": "world!"},
    },
]


incorrect_test_cases = [
    {
        "annotations": {"a": int, "b": float, "return": int},
        "args": (4,),
        "kwargs": {"b": 3},
    },
    {
        "annotations": {"a": str, "b": float, "return": float},
        "args": (4.4,),
        "kwargs": {"b": 3.3},
    },
    {
        "annotations": {"a": bool, "b": float, "return": int},
        "args": (True,),
        "kwargs": {"b": True},
    },
    {
        "annotations": {"a": str, "b": str, "return": int},
        "args": ("Hello ",),
        "kwargs": {"b": "world!"},
    },
]

from dataclasses import dataclass


def function_no_args() -> None:
    ...


def function_with_args(a: str, b: int) -> None:
    ...


class EmptyClass:
    ...


class ClassWithInit:
    def __init__(self, a, b):
        self.a = a
        self.b = b


@dataclass
class DataClass:
    a: str
    b: int

    @property
    def property_(self) -> None:
        ...

    def method(self) -> None:
        ...

    def method_with_args(self, a: str, b: int) -> None:
        ...

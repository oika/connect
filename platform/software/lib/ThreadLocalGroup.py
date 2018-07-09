# -*- coding: utf-8 -*-


class ThreadLocalGroup:

    def __init__(self, *operators):
        self.__operators = tuple(operators)

    @property
    def operators(self):
        return self.__operators
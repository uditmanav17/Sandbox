# class PhoneNumber:
#     def __init__(self, number):
#         self.number = "".join(i for i in number if i.isnumeric())
#         if len(self.number)==11 and self.number[0]=='1':
#             self.number = self.number[1:]
# 
#         if len(self.number) != 10 \
#             or self.number[0] not in '23456789' \
#             or self.number[3] not in '23456789':
#             raise ValueError("wrong number")
#         
#         self.area_code = self.number[:3]
#             
#     def pretty(self):
#         return f"({self.number[:3]}) {self.number[3:6]}-{self.number[6:]}"
# 		
		
import re


class Phone(object):
    _pattern = re.compile(r'''
        ^\+?1?              # optional literal `+` and country code
        (?:[-. ]+)?         # optional separators
        \(?([2-9]\d{2})\)?  # the area code, with or without surrounding parens
        (?:[-. ]+)?         # optional separators
        ([2-9]\d{2})        # the exchange code
        (?:[-. ]+)?         # optional separators
        (\d{4})$            # the subscriber number
    ''', re.VERBOSE)

    def __init__(self, phone_number):
        try:
            self.area_code, self.exchange, self.subscriber = \
                    self._pattern.search(phone_number.strip()).groups()
        except AttributeError:
            raise ValueError('Invalid `phone_number`')

    @property
    def number(self):
        return self.area_code + self.exchange + self.subscriber

    def pretty(self):
        return '({}) {}-{}'.format(self.area_code, self.exchange, self.subscriber)
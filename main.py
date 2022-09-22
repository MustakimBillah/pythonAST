import separate
from custom import process_values


def print_hi(name):
    print(f'Hi, {name},2-3')


def sum_num(num1, num2):
    return num1 + num2


if __name__ == '__main__':
    print_hi('PyCharm testing')
    sum_num(5, 10)
    val = process_values(2, 3, 1)
    res = separate.three_sum(2, 3, 1)
    print("three_sum is :", res)
    print("process_value is :", val)

from Util import test


def transform(subject_number, loop_size):
    value = 1

    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227

    return value


def find_loop_size(target):
    value = 1
    subject_number = 7
    loop_size = 0

    while value != target:
        loop_size += 1
        value *= subject_number
        value %= 20201227

    return loop_size


def decrypt(key_code, door_code):
    loop_size = find_loop_size(door_code)
    return transform(key_code, loop_size)


def run():
    return decrypt(18356117, 5909654)


if __name__ == '__main__':
    test(8, find_loop_size(5764801))
    test(11, find_loop_size(17807724))
    test(14897079, transform(17807724, 8))
    test(14897079, transform(5764801, 11))

    test(14897079, decrypt(5764801, 17807724))
    print(run())

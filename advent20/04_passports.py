from Util import test, from_file
from re import compile


hair_color_pattern = compile("^#[0-9a-f]{6}$")
pid_pattern = compile("^\\d{9}$")


def keys_valid(data):
    expected_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"}
    data["cid"] = "not used"

    return expected_keys == data.keys()


def data_valid(data):
    if not keys_valid(data):
        return False

    try:
        if not (1920 <= int(data['byr']) <= 2002):
            return False

        if not (2010 <= int(data['iyr']) <= 2020):
            return False

        if not (2020 <= int(data['eyr']) <= 2030):
            return False

        height = data['hgt']
        unit = height[-2:]
        height_value = int(height[:-2])

        if unit == 'cm':
            if not (150 <= height_value <= 193):
                return False
        elif unit == 'in':
            if not (59 <= height_value <= 76):
                return False
        else:
            return False

        if not hair_color_pattern.match(data['hcl']):
            return False

        if data['ecl'] not in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}:
            return False

        if not pid_pattern.match(data['pid']):
            return False

    except:
        return False

    return True


def scan(lines, validator):
    count = 0
    keys = {}
    for line in lines:
        if line == '\n':
            if validator(keys):
                count += 1

            keys = {}
            continue

        split_data = line.split(" ")

        for data in split_data:
            key_and_value = data.strip().split(":")
            keys[key_and_value[0]] = key_and_value[1]

    return count


def run():
    return scan(from_file("inputs/04_passports"), data_valid)


if __name__ == '__main__':
    test_data = ["ecl:gry pid:860033327 eyr:2020 hcl:#fffffd\n", "byr:1937 iyr:2017 cid:147 hgt:183cm\n", "\n",
            "iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884\n", "hcl:#cfa07d byr:1929\n", "\n",
            "hcl:#ae17e1 iyr:2013\n", "eyr:2024\n", "ecl:brn pid:760753108 byr:1931\n", "hgt:179cm\n", "\n",
            "hcl:#cfa07d eyr:2025 pid:166559648\n", "iyr:2011 ecl:brn hgt:59in\n", "\n"]

    test_data_bad = ["eyr:1972 cid:100", "hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926", "\n", "iyr:2019", "hcl:#602927 eyr:1967 hgt:170cm", "ecl:grn pid:012533040 byr:1946", "\n", "hcl:dab227 iyr:2012", "ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277", "\n", "hgt:59cm ecl:zzz", "eyr:2038 hcl:74454a iyr:2023", "pid:3556412378 byr:2007", "\n"]
    test_data_good = ["pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980", "hcl:#623a2f", "\n", "eyr:2029 ecl:blu cid:129 byr:1989", "iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm", "\n", "hcl:#888785", "hgt:164cm byr:2001 iyr:2015 cid:88", "pid:545766238 ecl:hzl", "eyr:2022", "\n", "iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719", "\n"]

    # test(2, scan(test_data, keys_valid))
    # test(210, scan(from_file("inputs/04_passports"), keys_valid))
    #
    # test(0, scan(test_data_bad, data_valid))
    # test(4, scan(test_data_good, data_valid))

    # test(1, scan(["iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719", '\n'],  data_valid))

    # test(0, scan(["iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:0123456789", '\n'],  data_valid))
    # test(0, scan(["iyr:2010 hgt:158cm hcl:#b6652a ecl:wat byr:1944 eyr:2021 pid:093154719", '\n'],  data_valid))
    # test(0, scan(["iyr:2010 hgt:158cm hcl:#123abz ecl:blu byr:1944 eyr:2021 pid:093154719", '\n'],  data_valid))
    # test(0, scan(["iyr:2010 hgt:158cm hcl:123abz ecl:blu byr:1944 eyr:2021 pid:093154719", '\n'],  data_valid))
    # test(0, scan(["iyr:2010 hgt:190in hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719", '\n'],  data_valid))
    # test(0, scan(["iyr:2010 hgt:190 hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719", '\n'],  data_valid))
    # test(1, scan(["iyr:2010 hgt:60in hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719", '\n'],  data_valid))
    # test(0, scan(["iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:2003 eyr:2021 pid:093154719", '\n'],  data_valid))
    #
    print(run())

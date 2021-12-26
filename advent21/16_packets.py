from Util import test

input_string = '020D708041258C0B4C683E61F674A1401595CC3DE669AC4FB7BEFEE840182CDF033401296F44367F938371802D2CC9801A980021304609C431007239C2C860400F7C36B005E446A44662A2805925FF96CBCE0033C5736D13D9CFCDC001C89BF57505799C0D1802D2639801A900021105A3A43C1007A1EC368A72D86130057401782F25B9054B94B003013EDF34133218A00D4A6F1985624B331FE359C354F7EB64A8524027D4DEB785CA00D540010D8E9132270803F1CA1D416200FDAC01697DCEB43D9DC5F6B7239CCA7557200986C013912598FF0BE4DFCC012C0091E7EFFA6E44123CE74624FBA01001328C01C8FF06E0A9803D1FA3343E3007A1641684C600B47DE009024ED7DD9564ED7DD940C017A00AF26654F76B5C62C65295B1B4ED8C1804DD979E2B13A97029CFCB3F1F96F28CE43318560F8400E2CAA5D80270FA1C90099D3D41BE00DD00010B893132108002131662342D91AFCA6330001073EA2E0054BC098804B5C00CC667B79727FF646267FA9E3971C96E71E8C00D911A9C738EC401A6CBEA33BC09B8015697BB7CD746E4A9FD4BB5613004BC01598EEE96EF755149B9A049D80480230C0041E514A51467D226E692801F049F73287F7AC29CB453E4B1FDE1F624100203368B3670200C46E93D13CAD11A6673B63A42600C00021119E304271006A30C3B844200E45F8A306C8037C9CA6FF850B004A459672B5C4E66A80090CC4F31E1D80193E60068801EC056498012804C58011BEC0414A00EF46005880162006800A3460073007B620070801E801073002B2C0055CEE9BC801DC9F5B913587D2C90600E4D93CE1A4DB51007E7399B066802339EEC65F519CF7632FAB900A45398C4A45B401AB8803506A2E4300004262AC13866401434D984CA4490ACA81CC0FB008B93764F9A8AE4F7ABED6B293330D46B7969998021C9EEF67C97BAC122822017C1C9FA0745B930D9C480'


def hex_to_bin(c):
    if c == '0':
        return '0000'
    if c == '1':
        return '0001'
    if c == '2':
        return '0010'
    if c == '3':
        return '0011'
    if c == '4':
        return '0100'
    if c == '5':
        return '0101'
    if c == '6':
        return '0110'
    if c == '7':
        return '0111'
    if c == '8':
        return '1000'
    if c == '9':
        return '1001'
    if c == 'A':
        return '1010'
    if c == 'B':
        return '1011'
    if c == 'C':
        return '1100'
    if c == 'D':
        return '1101'
    if c == 'E':
        return '1110'
    if c == 'F':
        return '1111'


def convert_to_binary(line):
    return "".join(map(hex_to_bin, line))


def process_groups(groups, message_type):
    if message_type == 0:
        return sum(groups)
    if message_type == 1:
        acc = 1
        for group in groups:
            acc *= group
        return acc
    if message_type == 2:
        return min(groups)
    if message_type == 3:
        return max(groups)
    if message_type == 5:
        return 1 if groups[0] > groups[1] else 0
    if message_type == 6:
        return 1 if groups[0] < groups[1] else 0
    if message_type == 7:
        return 1 if groups[0] == groups[1] else 0
    return 0


def parse_literal(start, line):
    groups = []

    while True:
        group = line[start: start + 5]
        groups.append(group[1:])
        start += 5
        if group[0] == '0':
            break

    return start, int("".join(groups), 2)


def parse_operator_bits(start, line, version_numbers):
    bits = line[start:start + 15]
    length = int(bits, 2)

    actual_length = 0
    packet_start = start + 15

    groups = []
    while actual_length < length:
        next_pos, value = parse_packet(packet_start, line, version_numbers)
        groups.append(value)

        actual_length += next_pos - packet_start
        packet_start = next_pos

    return packet_start, groups


def parse_operator_length(start, line, version_numbers):
    bits = line[start:start + 11]
    subpackets = int(bits, 2)

    next_packet = start + 11

    groups = []
    for packet in range(subpackets):
        next_packet, value = parse_packet(next_packet, line, version_numbers)
        groups.append(value)

    return next_packet, groups


def parse_operator(start, line, version_numbers, message_type):
    length_type = line[start]

    if length_type == '0':
        next_packet, groups = parse_operator_bits(start + 1, line, version_numbers)
    else:
        next_packet, groups = parse_operator_length(start + 1, line, version_numbers)

    return next_packet, process_groups(groups, message_type)


def parse_packet(start, line, version_numbers):
    version = int(line[start:start + 3], 2)
    version_numbers.append(version)

    message_type = int(line[start + 3: start + 6], 2)

    if message_type == 4:
        return parse_literal(start + 6, line)
    else:
        return parse_operator(start + 6, line, version_numbers, message_type)


def parse_and_count(line):
    versions = []
    parse_packet(0, convert_to_binary(line), versions)

    return sum(versions)


def parse_and_evaluate(line):
    _, value = parse_packet(0, convert_to_binary(line), [])

    return value


def run():
    return parse_and_evaluate(input_string)


def main():
    test("110100101111111000101000", convert_to_binary("D2FE28"))
    test(6, parse_and_count("D2FE28"))

    test(2021, parse_and_evaluate("D2FE28"))

    test(16, parse_and_count("8A004A801A8002F478"))
    test(12, parse_and_count("620080001611562C8802118E34"))
    test(23, parse_and_count("C0015000016115A2E0802F182340"))
    test(31, parse_and_count("A0016C880162017C3686B18A3D4780"))

    test(3, parse_and_evaluate('C200B40A82'))
    test(54, parse_and_evaluate('04005AC33890'))
    test(7, parse_and_evaluate('880086C3E88112'))
    test(9, parse_and_evaluate('CE00C43D881120'))
    test(1, parse_and_evaluate('D8005AC2A8F0'))
    test(0, parse_and_evaluate('F600BC2D8F'))
    test(0, parse_and_evaluate('9C005AC2F8F0'))
    test(1, parse_and_evaluate('9C0141080250320F1802104A08'))

    test(965, parse_and_count(input_string))
    test(116672213160, run())


if __name__ == '__main__':
    main()

class BasePacket:
    def __init__(self, version, type_id) -> None:
        self.version = version
        self.type_id = type_id

    def get_version_sums(self):
        raise NotImplementedError
    
    def evaluate(self):
        raise NotImplementedError


class LiteralValuePacket(BasePacket):
    def __init__(self, version, type_id, value) -> None:
        super().__init__(version, type_id)
        self.value = value
    
    def get_version_sums(self):
        return self.version

    def evaluate(self):
        return self.value


class OperatorPacket(BasePacket):
    def __init__(self, version, type_id) -> None:
        super().__init__(version, type_id)

        self.subpackets = []
    
    def add_subpacket(self, subpkt):
        self.subpackets.append(subpkt)

    def get_version_sums(self):
        return self.version + sum([s.get_version_sums() for s in self.subpackets])
    
    def evaluate(self):
        raise NotImplementedError


class SumPacket(OperatorPacket):
    def evaluate(self):
        return sum([i.evaluate() for i in self.subpackets])


class ProductPacket(OperatorPacket):
    def evaluate(self):
        product = 1
        for s in self.subpackets:
            product = product * s.evaluate()
        return product


class MinPacket(OperatorPacket):
    def evaluate(self):
        return min([i.evaluate() for i in self.subpackets])


class MaxPacket(OperatorPacket):
    def evaluate(self):
        return max([i.evaluate() for i in self.subpackets])


class GtPacket(OperatorPacket):
    def evaluate(self):
        if len(self.subpackets) != 2:
            print("Can't use a gt operator with {0} subpackets!".format(len(self.subpackets)))
        
        first_subpkt = self.subpackets[0].evaluate()
        second_subpkt = self.subpackets[1].evaluate()
        return 1 if first_subpkt > second_subpkt else 0


class LtPacket(OperatorPacket):
    def evaluate(self):
        if len(self.subpackets) != 2:
            print("Can't use an lt operator with {0} subpackets!".format(len(self.subpackets)))
        
        first_subpkt = self.subpackets[0].evaluate()
        second_subpkt = self.subpackets[1].evaluate()
        return 1 if first_subpkt < second_subpkt else 0


class EqPacket(OperatorPacket):
    def evaluate(self):
        if len(self.subpackets) != 2:
            print("Can't use an eq operator with {0} subpackets!".format(len(self.subpackets)))
        
        first_subpkt = self.subpackets[0].evaluate()
        second_subpkt = self.subpackets[1].evaluate()
        return 1 if first_subpkt == second_subpkt else 0


class PacketFactory:
    def __init__(self, bin_str) -> None:
        self.bin_str = bin_str
        self.idx = 0
    
    def advance_index(self, num):
        self.idx = self.idx + num

    def read_version_number(self):
        num_ver_bits = 3
        start_idx = self.idx
        self.advance_index(num_ver_bits)
        end_idx = self.idx
        return int(self.bin_str[start_idx:end_idx], 2)

    def read_type_id(self):
        num_type_id_bits = 3
        start_idx = self.idx
        self.advance_index(num_type_id_bits)
        end_idx = self.idx
        return int(self.bin_str[start_idx:end_idx], 2)

    def get_next_packet(self):
        initial_idx = self.idx
        version_num = self.read_version_number()
        type_id = self.read_type_id()

        if type_id == 4:
            pkt, bits_consumed = self.build_literal_value_packet(version_num, type_id)
        else:
            pkt, bits_consumed = self.build_operator_packet(version_num, type_id)
        
        bits_consumed = self.idx - initial_idx
        return pkt, bits_consumed

    def build_literal_value_packet(self, version_num, type_id):
        data_bits = 4
        number_bin_str = ''
        initial_idx = self.idx
        while True:
            keep_going = self.bin_str[self.idx]
            self.advance_index(1)
            start_idx = self.idx
            self.advance_index(data_bits)
            end_idx = self.idx
            chunk = self.bin_str[start_idx:end_idx]
            number_bin_str = number_bin_str + chunk
            if keep_going == '0':
                break

        bits_consumed = end_idx - initial_idx
        literal_value = int(number_bin_str, 2)
        pkt = LiteralValuePacket(version_num, type_id, literal_value)
        return pkt, bits_consumed

    def build_operator_packet(self, version_num, type_id):
        if type_id == 0:
            pkt = SumPacket(version_num, type_id)
        elif type_id == 1:
            pkt = ProductPacket(version_num, type_id)
        elif type_id == 2:
            pkt = MinPacket(version_num, type_id)
        elif type_id == 3:
            pkt = MaxPacket(version_num, type_id)
        elif type_id == 5:
            pkt = GtPacket(version_num, type_id)
        elif type_id == 6:
            pkt = LtPacket(version_num, type_id)
        elif type_id == 7:
            pkt = EqPacket(version_num, type_id)
        else:
            print('Type {0} is not defined!'.format(type_id))
            raise NotImplementedError

        initial_idx = self.idx
        length_type_id = self.bin_str[self.idx]
        self.advance_index(1)
        if length_type_id == '0':
            # Type 0 indicates that the next 15 bits are the number of bits in the sub-packets
            num_length_bits = 15
            start_idx = self.idx
            self.advance_index(num_length_bits)
            end_idx = self.idx
            length_bin_str = self.bin_str[start_idx:end_idx]
            num_subpacket_bits = int(length_bin_str, 2)
            bits_consumed = 0
            while bits_consumed < num_subpacket_bits:
                subp, sub_bits = self.get_next_packet()
                pkt.add_subpacket(subp)
                bits_consumed = bits_consumed + sub_bits
        else:
            # Type 1 indicates that the next 11 bits are the number of sub-packets
            num_length_bits = 11
            start_idx = self.idx
            self.advance_index(num_length_bits)
            end_idx = self.idx
            length_bin_str = self.bin_str[start_idx:end_idx]
            num_subpackets = int(length_bin_str, 2)

            for _ in range(num_subpackets):
                subp, _ = self.get_next_packet()
                pkt.add_subpacket(subp)
                
        bits_consumed = self.idx - initial_idx
        return pkt, bits_consumed


def hex_to_bin_str(hex_str):
    hex_chars = [i for i in hex_str]
    bin4 = [bin(int(i, 16))[2:].zfill(4) for i in hex_chars]
    return ''.join(bin4)


def read_input(file_path):
    with open(file_path, 'r') as f:
        all_data = f.read()

    hex_str = all_data.strip()
    bin_str = hex_to_bin_str(hex_str)

    f = PacketFactory(bin_str)    
    pkt, bits_consumed = f.get_next_packet()
    return pkt


def main():
    root_pkt = read_input('./input.txt')
    print('Sum of versions in root packet: {0}'.format(root_pkt.get_version_sums()))
    print('Value of root packet: {0}'.format(root_pkt.evaluate()))


if __name__ == '__main__':
    main()

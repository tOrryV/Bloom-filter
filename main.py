import random
import array
from bitarray import bitarray


MAX_STRING_SIZE = 50
FILTER_SIZE = 0xFFFF


def poly_hash(coef, input_string):
    if len(input_string) > MAX_STRING_SIZE:
        print("Error: The size of the input string exceeds the limit...")
        return 0

    arr = array.array('H', [0] * (MAX_STRING_SIZE // 2))

    for i in range(0, len(input_string) - 1, 2):
        arr[i // 2] = ord(input_string[i]) + (ord(input_string[i + 1]) << 8)

    res = 1
    for elem in arr:
        res = res * coef + elem

    return res


def generate_string():
    characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    length = random.randint(10, 49)
    return ''.join(random.choice(characters) for _ in range(length))


class BloomFilter:
    def __init__(self, num):
        self.num_of_hash_func = num
        self.filter = bitarray(FILTER_SIZE)
        self.filter.setall(False)

    def add(self, input_string):
        for i in range(1, self.num_of_hash_func + 1):
            hash_val = poly_hash(i, input_string)
            self.filter[hash_val % FILTER_SIZE] = True

    def possibly_contains(self, input_string):
        for i in range(1, self.num_of_hash_func + 1):
            hash_val = poly_hash(i, input_string)
            if not self.filter[hash_val % FILTER_SIZE]:
                return False
        return True

    def clear(self):
        self.filter.setall(False)


if __name__ == "__main__":
    bloom_filter = BloomFilter(3)

    bloom_filter.add("some")
    bloom_filter.add("random")
    bloom_filter.add("words")
    bloom_filter.add("ddos")

    print("Contains 'random':", bloom_filter.possibly_contains("random"))
    print("Contains 'do not contain':", bloom_filter.possibly_contains("do not contain"))

    #   experiment
    iterations = 10
    average_error = 0

    for filling_factor in range(5, 51, 5):
        filling_factor /= 100
        total_error = 0.0
        bloom_filter = BloomFilter(int(0.69 / filling_factor))

        messages_to_add = int(FILTER_SIZE * filling_factor)

        for _ in range(iterations):

            for _ in range(messages_to_add):
                bloom_filter.add(generate_string())

            generated_messages = 0
            while True:
                generated_messages += 1
                if bloom_filter.possibly_contains(generate_string()):
                    error = 1.0 / generated_messages
                    total_error += error
                    break

            bloom_filter.clear()

        print(f"s:\t{int(0.69 / filling_factor)}")
        print(f"factor: {filling_factor}")
        print(f"error:  {total_error / iterations}\n")

        average_error += total_error

    average_error /= (iterations * 10)
    print(f"Estimated error probability: {average_error}")

"""
Darcy Myring
28769414
"""

from bitarray import bitarray
import sys

"""
DECODER
"""


def elias_decode(bitstring):
    # takes a bitarray with elias omega value at the start and returns both the
    # corresponding integer and the remaining bitstring

    if bitstring[0]:
        return 1, bitstring[1:]

    bitstring = bitstring[1:]

    length = 2

    while not bitstring[0]:  # while bitstring[i] != 1 (ie. while length component)
        bitstring[0] = True
        templength = length
        length = int(bitstring[0:length].to01(), 2) + 1
        bitstring = bitstring[templength:]

    binary_number = bitstring[0:length]
    number = int(binary_number.to01(), 2)

    bitstring = bitstring[length:]

    return number, bitstring


def ascii_retrieve(bitstring):
    # takes in bitarray with ascii character at start and returns both the character and remaining bitarray
    ascii_range = bitstring[0:7]
    value = chr(int(ascii_range.to01(), 2))

    return value, bitstring[7:]


def huffman_retrieve(bitstring):
    # takes in bitarray with huffman length value at the start and returns
    # both the huffman binary rep and the remaining bitarray

    length, new_bitstring = elias_decode(bitstring)
    huffman_val = new_bitstring[0:length]
    return huffman_val, new_bitstring[length:]


def header_retrieve(bitstring):
    # takes in bitstring and returns array of all characters and their huffman representation
    # also returns the remaining bitstring (ie. the data component)

    character_array = []

    unique_characters, bitstring = elias_decode(bitstring)

    for i in range(unique_characters):
        character, bitstring = ascii_retrieve(bitstring)
        huffmanrep, bitstring = huffman_retrieve(bitstring)
        character_array.append([character, huffmanrep])


    return character_array, bitstring


def data_retrieve(bitstring, character_array):
    # takes the results from header_retrieve and finds the original string

    solution_string = ''

    unique_fields, bitstring = elias_decode(bitstring)

    for i in range(unique_fields):

        if bitstring[0] == 1:  # if the field is in format 1
            bitstring = bitstring[1:]
            for j in character_array:
                huffman_length = len(j[1])
                if bitstring[0:huffman_length] == j[1]:
                    solution_string += j[0]
                    bitstring = bitstring[huffman_length:]
                    break

        elif bitstring[0] == 0:
            bitstring = bitstring[1:]
            offset, bitstring = elias_decode(bitstring)
            length, bitstring = elias_decode(bitstring)

            for _ in range(length):
                solution_string += solution_string[-offset]

    return solution_string, bitstring


def solution(bitstring):
    # takes the original bitarray string and returns the original string

    if bitstring[0] and bitstring[10]:  # handles the case where string length is one
        return ascii_retrieve(bitstring[1:])[0]

    character_array, bitstring = header_retrieve(bitstring)
    solution_string, bitstring = data_retrieve(bitstring, character_array)

    return solution_string


def decoder_lzss(bin_doc):
    # takes in a .bin encoded document and writes its corresponding string to a .txt file

    b = bitarray()

    with open(bin_doc, 'rb') as file:
        b.fromfile(file)

    output_string = solution(b)

    file = open('output_decoder_lzss.txt', 'w')
    file.write(output_string)
    file.close()


if __name__ == '__main__':
    bin_doc = sys.argv[1]
    decoder_lzss(bin_doc)


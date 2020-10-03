"""
Darcy Myring
28769414
"""

from bitarray import bitarray
import sys


class CharacterTuple:
    # creates class to represent characters as tuples with their frequency in a string

    def __init__(self, char, freq, leftchild=None, rightchild=None, parent=None):
        self.char = char
        self.freq = freq
        self.leftchild = leftchild
        self.rightchild = rightchild
        self.parent = parent
        self.leaf = False
        if len(self) == 1:
            self.leaf = True
        self.binaryrep = bitarray()
        self.binarylength = len(self.binaryrep)

    def __len__(self):
        return len(self.char)

    def __repr__(self):
        return str([self.char, self.freq, self.binaryrep])

    def __lt__(self, other):
        return self.freq < other.freq

    def __gt__(self, other):
        return self.freq > other.freq

    def __eq__(self, other):
        return self.freq == other.freq



"""
Huffman encoding
"""


def stringsort(string):
    # finds the number of occurances of each character in string and returns an array of charactertuples
    # in ascending order based on the number of occurances

    frequency = []
    characters = []

    for i in string:
        appended = False
        for j in range(len(characters)):
            if i == characters[j]:
                frequency[j] += 1
                appended = True
                break
        if not appended:
            characters.append(i)
            frequency.append(1)

    tuplearray = []
    for i in range(len(frequency)):
        tuplearray.append(CharacterTuple(characters[i], frequency[i]))

    tuplearray.sort()

    return tuplearray


def huffman(string):
    # creates a huffman tree and returns the root node

    tuplearray = stringsort(string)
    parentnode = tuplearray[0]

    while len(tuplearray) > 1:
        leftnode = tuplearray.pop(0)
        rightnode = tuplearray.pop(0)
        parentnode = CharacterTuple(leftnode.char+rightnode.char, leftnode.freq+rightnode.freq,
                                    leftchild=leftnode, rightchild=rightnode)
        tuplearray.append(parentnode)
        tuplearray.sort()

        leftnode.parent = parentnode
        rightnode.parent = parentnode

    return parentnode


def get_leaves(string):
    # finds all of the leaves of the huffman tree of string, returns them in an array

    root = huffman(string)
    non_leaf = []
    leaves = []
    non_leaf.append(root)

    while len(non_leaf) > 0:
        current_node = non_leaf.pop(0)

        if current_node.leaf:
            leaves.append(current_node)

        else:
            if current_node.leftchild is not None:
                current_node.leftchild.binaryrep.extend(current_node.binaryrep)
                current_node.leftchild.binaryrep.append(False)
                non_leaf.append(current_node.leftchild)

            if current_node.rightchild is not None:
                current_node.rightchild.binaryrep.extend(current_node.binaryrep)
                current_node.rightchild.binaryrep.append(True)
                non_leaf.append(current_node.rightchild)


    return leaves




"""
Elias Encoding
"""


def to_binary(integer):  # takes integer (decimal) input and returns bitarray of its binary representation

    binval = bitarray()

    while integer > 1:
        if integer%2 != 1:
            binval.append(False)
        else:
            binval.append(True)
        integer = integer//2

    binval.append(True)
    binval.reverse()

    return binval



def elias_omega(integer):  # takes integer (decimal) input and returns its elias omega representation
    binint = to_binary(integer)
    value = binint
    component_array = []

    while len(value) > 1:
        value = to_binary(len(value) - 1)
        valueaux = value
        valueaux[0] = False
        component_array.append(valueaux)

    component_array.reverse()
    component_array.append(binint)

    result = bitarray()
    for i in component_array:
        result.extend(i)
    return result


"""
Header encoding
"""


def no_of_char(string):  # takes the root of a huffman tree and returns bitarray value of the number of nodes
    leaves = get_leaves(string)
    return elias_omega(len(leaves))


def binary_rep(character):  # takes a character and returns its ascii bitstring
    binstring = bin(ord(character))
    binstring = binstring[2:]
    returnval = bitarray()
    for i in binstring:
        if i == '1':
            returnval.append(True)
        else:
            returnval.append(False)

    if len(returnval) == 6:  # accomodating for a integer values
        buffer_zero = bitarray()
        buffer_zero.append(False)
        buffer_zero.extend(returnval)
        returnval = buffer_zero

    return returnval


def huffman_header(string):
    # takes a string and returns the full encoded header for lzss as a bitarray

    number_of_char = no_of_char(string)
    leaves = get_leaves(string)
    fullbitarray = bitarray()
    fullbitarray.extend(number_of_char)
    for i in leaves:
        fullbitarray.extend(binary_rep(i.char))
        fullbitarray.extend(elias_omega(len(i.binaryrep)))
        fullbitarray.extend(i.binaryrep)

    return fullbitarray


"""
Data encoding
"""


def zalgorithm(text):
    # just your regular run of the mill z-algorithm - takes a string and returns the corresponding z-array

    z_array = [len(text)]

    lval = 0
    rval = 0

    iterated = False

    for j in range(1, len(text)):
        if text[j] == text[j-1]:
            rval += 1
            iterated = True
            if j == len(text) - 1:
                for i in range(1,j+1):
                    z_array.append(j-i+1)
                return z_array
        else:
            for i in range(1, j):
                z_array.append(j-i)
            break

    if iterated:
        lval = 1

    for i in range(len(z_array), len(text)):
        if rval <= i:

            for j in range(i, len(text)):

                if text[j] == text[j-i]:
                    lval = i
                    rval = j

                    if j >= len(text) - 1:
                        z_array.append(j - i + 1)
                        break

                else:
                    z_array.append(j-i)
                    break

        elif z_array[i-lval] < rval - i + 1:
            z_array.append(z_array[i-lval])

        elif z_array[i-lval] > rval - i + 1:
            z_array.append(rval - i)

        elif z_array[i-lval] == rval - i + 1:


            for j in range(rval, len(text)):

                if text[j] == text[j - lval]:
                    rval = j

                    if j >= len(text) - 1:
                        z_array.append(j - i + 1)
                        break

                else:
                    z_array.append(j - i)
                    break

    return z_array


def format_field_iter(string, window, buffer, position):  # computes one iteration of the format field function

    current_pos = position

    if buffer > len(string):  # ensures buffer is not too large as to cause indexing issues
        buffer = len(string)

    if current_pos > window and len(string) >= current_pos+buffer:
        dollar_sign_pos = buffer  # a variable which helps determine how far into the search string the $ appears
        search_string = string[current_pos:current_pos+buffer] + '$' + string[current_pos-window:current_pos+buffer]
    elif current_pos <= window:
        dollar_sign_pos = buffer
        search_string = string[current_pos:current_pos+buffer] + '$' + string[0:current_pos+buffer]
    elif len(string) < current_pos+buffer:
        dollar_sign_pos = len(string)-current_pos
        search_string = string[current_pos:] + '$' + string[current_pos-window:]
    else:
        raise ValueError

    z_array = zalgorithm(search_string)

    maxlength = z_array[dollar_sign_pos]
    maxindex = dollar_sign_pos

    for i in range(dollar_sign_pos, len(z_array)-dollar_sign_pos):
        if z_array[i] > maxlength:  # potentially change this to >=
            maxlength = z_array[i]
            maxindex = i

    offset = len(z_array) - maxindex - dollar_sign_pos

    if maxlength < 3:
        return [1, string[current_pos]]

    else:
        return [0, offset, maxlength]


def format_field(string, window, buffer):
    # takes a string, window and buffer and returns the relevant format field values in an array
    results_list = [[1, string[0]]]
    current_pos = 1

    while current_pos < len(string):
        new_result = format_field_iter(string, window, buffer, current_pos)
        results_list.append(new_result)
        if new_result[0] == 1:
            current_pos += 1
        else:
            current_pos += new_result[2]

    return results_list


def data(string, window, buffer):
    result = bitarray()
    format_field_array = format_field(string, window, buffer)
    length = elias_omega(len(format_field_array))
    result.extend(length)
    leaves = get_leaves(string)

    for field in format_field_array:

        if field[0] == 1:
            field_encoding = bitarray()
            field_encoding.append(True)
            character = field[1]
            for i in leaves:
                # this can be considered a pseudo-constant time operation, since the length of leaves is constant
                if i.char == character:
                    field_encoding.extend(i.binaryrep)
                    break

        else:
            field_encoding = bitarray()
            field_encoding.append(False)
            field_encoding.extend(elias_omega(field[1]))
            field_encoding.extend(elias_omega(field[2]))

        result.extend(field_encoding)

    return result


def encoder_lzz(string, window, buffer):
    # takes in a string, window, and buffer size and writes its fully encoded .bin document to current directory
    # works for strings with any ascii valued characters (newline character is not supported)

    stringcontents = open(string)
    string = stringcontents.read()
    window = int(window)
    buffer = int(buffer)

    if len(string) == 1:  # handles the case where the length is one
        result = bitarray()
        result.append(True)  # add number of unique characters (one)
        result.extend(binary_rep(string))  # add char binary representation
        result.append(True)  # add length of huffman encoding (one)
        result.append(True)  # add trivial huffman encoding (1)

        result.append(True)  # add number of fields (one)
        result.append(True)  # add field type (1)
        result.append(True)  # add huffman encoding (1)

    else:
        result = huffman_header(string) + data(string, window, buffer)
        padding = 8 - len(result)%8
        result += '0'*padding

    with open('output_encoder_lzss.bin', 'wb') as file:
        result.tofile(file)


if __name__ == '__main__':
    string = sys.argv[1]
    window = sys.argv[2]
    buffer = sys.argv[3]
    encoder_lzz(string, window, buffer)

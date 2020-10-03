# AdvancedAlgorithmsWork
Some python work for FIT3155: Advanced Algorithms and Data Structures

encoder_lzss.py is a script which takes any .txt document and writes a .bin file which is its compressed binary representation, based on the LZ77 algorithm (explained in the following
wikipedia article: https://en.wikipedia.org/wiki/LZ77_and_LZ78#LZ77). 

decoder_lzss.py is a script which takes the .bin document created in encoder_lzss.py and retrieves the original string, writing it to a .txt file. 

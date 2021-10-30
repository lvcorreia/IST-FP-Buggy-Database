# Fazer assinaturas para funcoes (O que recebe e devolve e tipos, o que faz), fazer raise ValueError para erros

# PART 1

def corrigir_palavra(word):
    length = len(word)
    count = 0
    while count < length - 1:
        letter1 = word[count]
        letter2 = word[count + 1]
        # Verificar se a letter1 e letter2 sao um surto de letras
        if letter1 != letter2 and (letter1.lower() == letter2 or letter1 == letter2.lower()):
            word = word[:count] + word[count + 2:]
            length -= 2
            # E necessario verificar se a letra antes e depois da reacao sao um surto de letras
            if count != 0:
                count -= 1
        else:
            count += 1
    return word


def eh_anagrama(word1, word2):
    sorted_word1 = sorted(word1.lower())
    sorted_word2 = sorted(word2.lower())
    if sorted_word1 == sorted_word2:
        return True
    return False


# MAIN
# Do validation checks
def corrigir_doc(doc):
    # Check doc is not an empty string, check it is made up of at least one character
    if not (doc != "" and all(chr.isalpha() or chr.isspace() for chr in doc) and doc.isspace() != True):
        raise ValueError("corrigir_doc: argumento invalido")
    doc = corrigir_surtos(doc)
    corrected_doc = remover_anagramas(doc)
    corrected_doc_str = " "
    return corrected_doc_str.join(corrected_doc)


# Compares each word of the doc (the letter outbreaks have been corrected at this point)
# with eachother and checks if they are anagrams
def remover_anagramas(doc):
    length = len(doc)
    count1 = 0
    while count1 < length - 1:
        count2 = count1 + 1
        while count2 < length:
            if eh_anagrama(doc[count1], doc[count2]) and doc[count1] != doc[count2]:
                del doc[count2]
                length -= 1
            else:
                count2 += 1
        count1 += 1
    return doc


def corrigir_surtos(incorrect_doc):
    corrected_doc = []
    length = len(incorrect_doc)
    lower_index = 0
    for upper_index in range(0, length):
        if incorrect_doc[upper_index] == " " or upper_index == length - 1:
            if upper_index == length - 1:
                upper_index += 1
            # Check for two consecutive spaces
            elif incorrect_doc[upper_index + 1] == " ":
                raise ValueError("corrigir_doc: argumento invalido")
            correct_word = corrigir_palavra(incorrect_doc[lower_index:upper_index])
            # CHECK IF THIS IS NEEDED
            # if correct_word == "":
            #     raise ValueError ("corrigir_doc: argumento invalido")
            # Check if word with removed outbreals is empty
            corrected_doc.append(correct_word)
            lower_index = upper_index + 1
    return corrected_doc


# PART 2

def obter_posicao(character, integer):
    if character == "C":
        if integer > 3:
            integer -= 3
    elif character == "B":
        if integer < 7:
            integer += 3
    elif character == "E":
        if integer not in (1, 4, 7):
            integer -= 1
    elif character == "D":
        if integer not in (3, 6, 9):
            integer += 1
    return integer


def obter_digito(characters, integer):
    for element in characters:
        integer = obter_posicao(element, integer)
    return integer


def obter_pin(tup):
    pin_length = len(tup)
    if pin_length < 4 or pin_length > 10:
        raise ValueError("obter_pin: argumento invalido")
    pin = ()
    position = 5
    for count in range(0, pin_length):
        seq_moves = tup[count]
        if type(seq_moves) != str or seq_moves.isalpha() == False:
            raise ValueError("obter_pin: argumento invalido")

        position = obter_digito(seq_moves, position)
        pin += position,
    return pin


# PART 3

def eh_entrada(entry):
    if type(entry) != tuple:
        return False
    if len(entry) != 3:
        return False
    # Check using sub-functions whether elements of entry are valid
    if check_cipher(entry[0]) and \
            check_checksum(entry[1]) and \
            check_security_nums(entry[2]) == True:
        return True
    return False


def check_cipher(cipher):
    prev_char = "dash"
    for element in cipher:
        # Check character is a letter
        if element.isalpha() and element.islower():
            prev_char = "char"
        # Check character is a dash
        elif element == "-" and prev_char != "dash":
            prev_char = "dash"
        else:
            return False
    # Check if last element is a dash
    if prev_char == "dash":
        return False
    return True


def check_checksum(checksum):
    if len(checksum) != 7:
        return False
    if not (checksum[0] == "[" or checksum[6] == "]"):
        return False
    # Check that elements inside [] are lower case characters
    if not (checksum[1:5].isalpha() and checksum[1:5].islower()):
        return False
    return True


def check_security_nums(security_nums):
    if type(security_nums) != tuple:
        return False
    length = len(security_nums)
    if length == 0:
        return False
    for element in security_nums:
        if type(element) != int:
            return False
    return True


def validar_cifra(cipher, checksum):
    letters = {}
    # Adding letters present in cipher to dictionary "letters"
    for character in cipher:
        if character != "-" and character not in letters:
            letters[character] = occurances(cipher, character)
    ordered_letters = ""
    # While there are still letters
    for count in range(5):
        max_occurances = -1
        for key, value in letters.items():
            if value > max_occurances:
                max_occurances, max_letter = value, key
            # Must choose letter which comes first in the alphabet
            elif value == max_occurances:
                if key < max_letter:
                    max_occurances, max_letter = value, key
        ordered_letters += max_letter
        # Remove letter from dictionary
        del letters[max_letter]
    if ordered_letters == checksum[1:-1]:
        return True
    return False


def occurances(cipher, letter):
    count = 0
    for character in cipher:
        if character == letter:
            count += 1
    return count


def filtrar_bdb(unfiltered_list):
    filtered_list = []
    if len(unfiltered_list) == 0:
        raise ValueError("filtrar_bdb: argumento invalido")
    for entry in unfiltered_list:
        if eh_entrada(entry) == False:
            raise ValueError("filtrar_bdb: argumento invalido")
        if validar_cifra(entry[0], entry[1]) == False:
            filtered_list.append(entry)
    return filtered_list


# PART 4

def obter_num_seguranca(numbers):
    min_diff = 10 ** 10
    numbers = sorted(numbers)
    length = len(numbers)
    for count in range(length - 1):
        diff = abs(numbers[count] - numbers[count + 1])
        if diff < min_diff:
            min_diff = diff
    # if min_diff == 10**10:
    #    raise ValueError
    return min_diff


def decifrar_texto(cipher, security_num):
    deciphered_word = ""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    length = len(cipher)
    for i in range(length):
        if cipher[i] == "-":
            deciphered_word += " "
        # Check whether index is even or odd
        elif i % 2 == 0:
            letter_index = alphabet.index(cipher[i]) + security_num + 1
            # Modulus function allows the alphabet string to be "circular" so it doesn't go out of range
            deciphered_word += alphabet[letter_index % 26]
        else:
            letter_index = alphabet.index(cipher[i]) + security_num - 1
            deciphered_word += alphabet[letter_index % 26]
    return deciphered_word


def decifrar_bdb(encrypted_list):
    if type(encrypted_list) != list or len(encrypted_list) == 0:
        raise ValueError("decifrar_bdb: argumento invalido")
    decrypted_list = []
    for entry in encrypted_list:
        if not eh_entrada(entry):
            raise ValueError("decifrar_bdb: argumento invalido")
        decrypted_list.append(decifrar_texto(entry[0], obter_num_seguranca(entry[2])))
    return decrypted_list


# PART 5

# O valor que representa o m´aximo n´umero de vezes que aparece a letra ´e sempre
# maior ou igual que o m´ınimo.
def eh_utilizador(user_dict):
    if type(user_dict) != dict:
        return False
    # Check if keys name, pass and rule exist in user_dict
    if not {"name", "pass", "rule"} <= set(user_dict):
        return False
    if len(user_dict["name"]) == 0 or len(user_dict["pass"]) == 0:
        return False
    if not {"vals", "char"} <= set(user_dict["rule"]):
        return False
    if type(user_dict["rule"]["vals"]) != tuple or len(user_dict["rule"]["vals"]) != 2:
        return False
    if type(user_dict["rule"]["vals"][0]) != int or type(user_dict["rule"]["vals"][1]) != int:
        return False
    if len(user_dict["rule"]["char"]) != 1 or type(user_dict["rule"]["char"]) != str:
        return False
    return True


def eh_senha_valida(password, rule):
    if rule["vals"][0] > rule["vals"][1]:  # Second value in tuple must always be >= the first value
        return False
    count = 0
    prev_char = ""
    consecutive_chars = False
    occurances = 0
    for character in password:
        if character in ("a", "e", "i", "o", "u"):
            count += 1
        if character == prev_char:
            consecutive_chars = True
        prev_char = character
        if character == rule["char"]:
            occurances += 1
    if count < 3 or consecutive_chars == False:
        return False
    if occurances < rule["vals"][0] or occurances > rule["vals"][1]:
        return False
    return True


def filtrar_senhas(unfiltered_list):
    filtered_list = []
    if type(unfiltered_list) != list or len(unfiltered_list) == 0:
        raise ValueError("filtrar_senhas: argumento invalido")
    for dictionary in unfiltered_list:
        if not eh_utilizador(dictionary):
            raise ValueError("filtrar_senhas: argumento invalido")
        if not eh_senha_valida(dictionary["pass"], dictionary["rule"]):
            filtered_list.append(dictionary["name"])
    return sorted(filtered_list)


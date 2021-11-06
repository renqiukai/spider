from hashlib import sha1


def sha1_encoding(encoding_str):
    s1 = sha1()
    s1.update(encoding_str.encode())
    result = s1.hexdigest()
    return result


if __name__ == "__main__":
    s = "Asdf"
    str1 = sha1_encoding(s)
    print(str1)

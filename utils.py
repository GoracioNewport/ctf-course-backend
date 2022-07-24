def stringToList(string):
    return list(map(int, string[1:-1].split(",")))


def listToString(lis):
    return ("[" + ",".join(str(el) for el in lis) + "]")

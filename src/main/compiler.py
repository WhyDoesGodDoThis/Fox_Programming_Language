import error


def parseFile(rawText) -> list:
    parsedText = rawText.split(';')

    for index, line in enumerate(parsedText, 0):
        line = line.strip()
        print(line)
        if line.startswith("/*"):
            line = line.split("*/")[1]
        print(line)
        parsedText[index] = line.split(':')
        for token in parsedText[index]:
            parsedText[index] = token.strip()
    return parsedText





if __name__ == '__main__':
    print(parseFile(open("tests/testFile.txt", "r").read()))
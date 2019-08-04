
host = "localhost"
port = 11237

bufferSize = 8048

def networkDecode(byteText):
    return byteText.decode("utf-8")

def networkEncode(text):
    return text.encode("utf-8")
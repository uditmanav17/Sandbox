import configparser

parser = configparser.ConfigParser()
parser.read("conf.ini")
print(parser)
for sect in parser.sections():
    print("Section:", sect)
    for k, v in parser.items(sect):
        print(f"\t{k} = {v}")
    print()

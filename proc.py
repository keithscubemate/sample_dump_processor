import sys
import json

from datetime import datetime

def main(filename):
    names = ''
    spacings = ''
    lines = []
    with open(filename, 'r') as fin:
        names = fin.readline().strip()[1:]
        spacings = fin.readline().strip()
        lines = [l.strip() for l in fin][0:-2]

    names = names.split()
    spacings = get_spacings(spacings)

    objects = [proc_line(names, spacings, l) for l in lines]

    jobjects = json.dumps(objects)

    print(jobjects)

def get_spacings(spacings):
    rv = []

    last = 0
    final = 0

    for i, c in enumerate(spacings):
        if c == ' ':
            rv.append((last, i))
            last = i
        final = i

    rv.append((last, final))

    return rv

def proc_line(names, spacings, line):
    obj = {}

    field_count = len(names)

    for i in range(field_count):
        name = names[i]
        (start, end) = spacings[i]

        value = line[start:end].strip()

        value = try_parse(value)

        obj[name] = value

    return obj


def try_parse(value):
    types = [datetime, int, float]  # Add more types as needed

    for type_ in types:
        try:
            return type_(value)
        except TypeError:
            pass
        except ValueError:
            pass

    return value


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} [filename]".format(sys.argv[0]))
        exit(1)

    filename = sys.argv[1]
    main(filename)

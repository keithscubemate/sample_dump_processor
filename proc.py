import sys
import json
import base64

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

    for o in objects:
        val = o['IsComplete']
        o['IsComplete'] = bool(val)

    jobjects = json.dumps(objects[:-1])

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

        if "Time" in name:
            continue

        (start, end) = spacings[i]

        value = line[start:end].strip()

        value = try_parse(value)

        obj[name] = value

    return obj


def try_parse(value):
    types = [int, float]  # Add more types as needed

    if "NULL" == value:
        return None

    if '0x' in value:
        return hex_to_byte_array(value)

    for type_ in types:
        try:
            return type_(value)
        except TypeError:
            pass
        except ValueError:
            pass

    return value

def hex_to_byte_array(value):
    value = value[2:]

    rv = []

    for i in range(len(value)//2):
        idx = i * 2
        val = value[idx : idx + 2];

        rv.append(int(val, 16))

    dataStr = json.dumps(rv)

    encoding = base64.b64encode(dataStr.encode('utf-8')).decode('utf-8')

    return str(encoding)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} [filename]".format(sys.argv[0]))
        exit(1)

    filename = sys.argv[1]
    main(filename)

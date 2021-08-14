import json
import os
import sys
from language import Program


def program_from_str(s):
    return Program.create_program([x.rstrip() for x in s.split("\n") if len(x) > 0])


def run_from_disk(path):
    with open(path) as f:
        program = program_from_str(f.read())
    with open(os.path.dirname(path) + "/" + program.variable + ".json", "w") as f:
        f.write(json.dumps(program()))


if __name__ == "__main__":
    run_from_disk(sys.argv[1])
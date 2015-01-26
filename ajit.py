import os
import sys

def do_nothing(machine, code):
    pass

def exit_machine(machine, code):
    machine.terminate_flag = True

def select_storage(machine, code):
    machine.select_storage(code)

def send(machine, code):
    machine.current_storage.send(machine.get_storage(code))

def compare(machine, code):
    storage = machine.current_storage
    if storage.pop() > storage.pop():
        storage.push(0)
    else:
        storage.push(1)

def decide(machine, code):
    if machine.current_storage.pop() == 0:
        machine.cursor.reflect()

def pop(machine, code):
    value = machine.current_storage.pop()
    output = machine.output
    if code == 21:
        output(unicode(str(value)))
    elif code == 27:
        output(unichr(value))

def push(machine, code):
    if code == 21:
        value = machine.number_input()
    elif code == 27:
        value = machine.character_input()
    else:
        value = get_stroke_count(code)
    machine.current_storage.push(value)

def duplicate(machine, code):
    machine.current_storage.duplicate()

def swap(machine, code):
    machine.current_storage.swap()

def arithmetic(func):
    def operation(machine, code):
        storage = machine.current_storage
        right = storage.pop()
        left = storage.pop()
        storage.push(func(left, right))
    return operation

@arithmetic
def add(left, right):
    return left + right

@arithmetic
def subtract(left, right):
    return left - right

@arithmetic
def multiply(left, right):
    return left * right

@arithmetic
def divide(left, right):
    return left // right

@arithmetic
def modulo(left, right):
    return left % right

operation_table = [
    (do_nothing, 0),                    # 0
    (do_nothing, 0),                    # 1
    (divide, 2),                        # 2
    (add, 2),                           # 3
    (multiply, 2),                      # 4
    (modulo, 2),                        # 5
    (pop, 1),                           # 6
    (push, 0),                          # 7
    (duplicate, 1),                     # 8
    (select_storage, 0),                # 9
    (send, 1),                          # 10
    (do_nothing, 0),                    # 11
    (compare, 2),                       # 12
    (do_nothing, 0),                    # 13
    (decide, 1),                        # 14
    (do_nothing, 0),                    # 15
    (subtract, 2),                      # 16
    (swap, 2),                          # 17
    (exit_machine, 0),                  # 18
]

def get_operation(code):
    try:
        if code < 0:
            return do_nothing
        else:
            return operation_table[code][0]
    except IndexError:
        return do_nothing

def get_parameter_required(code):
    try:
        if code < 0:
            return 0
        else:
            return operation_table[code][1]
    except IndexError:
        return 0

stroke_count_table = [
    0, 2, 4, 4, 2,
    5, 5, 3, 5, 7,
    9, 9, 7, 9, 9,
    8, 4, 4, 6, 2,
    4, 1, 3, 4, 3,
    4, 4, 3,
]

def get_stroke_count(code):
    try:
        return stroke_count_table[code]
    except IndexError:
        return 0

class Cursor:
    def __init__(self, codespace, x=0, y=0, dx=0, dy=1):
        self.codespace = codespace
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def line(self):
        try:
            return self.codespace[self.y]
        except IndexError:
            return None

    def code(self):
        line = self.line()
        if line is None:
            return (-1, -1, -1)
        try:
            return line[self.x]
        except IndexError:
            return (-1, -1, -1)

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        line = self.line()
        width = len(line) if line is not None else 0
        height = len(self.codespace)
        if self.x < 0 and self.dx < 0:
            self.x = width - 1
        elif self.x >= width and self.dx > 0:
            self.x = 0
        if self.y < 0 and self.dy < 0:
            self.y = height - 1
        elif self.y >= height and self.dy > 0:
            self.y = 0

    def reflect(self):
        self.dx, self.dy = -self.dx, -self.dy

    def turn(self, code):
        if code == 0:
            self.dx, self.dy = 1, 0
        elif code == 2:
            self.dx, self.dy = 2, 0
        elif code == 4:
            self.dx, self.dy = -1, 0
        elif code == 6:
            self.dx, self.dy = -2, 0
        elif code == 8:
            self.dx, self.dy = 0, -1
        elif code == 12:
            self.dx, self.dy = 0, -2
        elif code == 13:
            self.dx, self.dy = 0, 1
        elif code == 17:
            self.dx, self.dy = 0, 2
        elif code == 18:
            self.dy = -self.dy
        elif code == 19:
            self.reflect()
        elif code == 20:
            self.dx = -self.dx

class Storage:
    def __init__(self):
        self.list = []
    def __len__(self):
        return self.count()
    def count(self):
        return len(self.list)
    def push(self, value):
        self.list.append(value)
    def send(self, to):
        to.push(self.pop())
    def pop(self):
        return 0
    def duplicate(self):
        pass
    def swap(self):
        pass

class Stack(Storage):
    def pop(self):
        try:
            return self.list.pop()
        except IndexError:
            return 0
    def duplicate(self):
        self.list.append(self.list[-1])
    def swap(self):
        self.list[-1], self.list[-2] = self.list[-2], self.list[-1]

class Queue(Storage):
    def pop(self):
        try:
            return self.list.pop(0)
        except IndexError:
            return 0
    def duplicate(self):
        self.list.insert(0, self.list[0])
    def swap(self):
        self.list[0], self.list[1] = self.list[1], self.list[0]

class Machine:
    def __init__(self, codespace):
        self.cursor = Cursor(codespace)
        self.storages = [
            Queue() if x == 21 or x == 27 else Stack()
            for x in range(28)
        ]
        self.select_storage(0)

    def run(self):
        self.terminate_flag = False
        while not self.terminate_flag:
            self.step()
        try:
            raise AheuiExit(self.current_storage.pop())
        except IndexError:
            raise AheuiExit(0)

    def step(self):
        cho, jung, jong = self.cursor.code()
        operation = get_operation(cho)
        self.cursor.turn(jung)
        if self.current_storage.count() < get_parameter_required(cho):
            self.cursor.reflect()
        else:
            operation(self, jong)
        self.cursor.move()

    def get_storage(self, code):
        return self.storages[code]

    def select_storage(self, code):
        self.current_storage = self.get_storage(code)

class AheuiExit(Exception):
    def __init__(self, exit_code):
        self.code = exit_code
    def __str__(self):
        return "Aheui machine terminated with exit code: " + str(self.code)

def extract_index(func):
    def extractor(code):
        if 0xac00 <= code <= 0xd7a3:
            return func(code - 0xac00)
        return -1
    return extractor

@extract_index
def get_cho(syllable_code):
    return syllable_code // 588

@extract_index
def get_jung(syllable_code):
    return (syllable_code // 28) % 21

@extract_index
def get_jong(syllable_code):
    return syllable_code % 28

def parse(code):
    result = []
    line = []
    for char in code:
        if char == u"\r":
            continue
        elif char == u"\n":
            result.append(line)
            line = []
        else:
            charcode = ord(char)
            line.append(
                (get_cho(charcode),
                 get_jung(charcode),
                 get_jong(charcode)))
    result.append(line)
    return result

def read_character():
    bytes = ""
    while True:
        byte = os.read(0, 1)
        if len(byte) == 0:
            break
        bytes = bytes + byte
        try:
            char = bytes.decode("utf-8")[0]
            charcode = ord(char)
            if (len(bytes) != 1 and charcode == 0 or
                ord(byte[0]) != charcode == 0):
                continue
            else:
                return char
        except UnicodeError:
            pass
    return u"\x00"[0]

def aheui_number_input():
    buf = ""
    last = -1
    while True:
        char = read_character()
        charcode = ord(char)
        if (charcode == 0 or charcode == 10 or
            charcode == 13 or charcode == 32):
            return last
        buf = buf + str(char)
        try:
            last = int(buf)
        except ValueError:
            return last

def aheui_character_input():
    return ord(read_character())

def aheui_output(value):
    os.write(1, value.encode("utf-8"))

def entry_point(argv):
    filename = argv[1]
    fp = os.open(filename, os.O_RDONLY, 0777)
    code = ""
    while True:
        read = os.read(fp, 4096)
        if len(read) == 0:
            break
        code += read
    code = code.decode("utf-8")
    machine = Machine(parse(code))
    machine.number_input = aheui_number_input
    machine.character_input = aheui_character_input
    machine.output = aheui_output
    try:
        machine.run()
    except AheuiExit as e:
        return e.code
    return 0

def target(*args):
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)

import sys
import os.path

argvs = sys.argv
argc = len(argvs)

def read_code():
    if argc == 1:
        print("no source file")
        exit()
    if argc > 2:
        print("too many arguments")
        exit()

    filename = argvs[1]

    if not os.path.exists(filename):
        print("no such file:{}".format(filename))
        exit()

    with open(filename, "r") as f:
        sourcecode = f.read()
    return sourcecode

class Starry:
	def __init__(self, sourcecode):
		self.src = sourcecode
		self.reader = 0
		self.stack = []
		self.labels = [0] * 1000
	
	def run(self):
		while self.reader < len(self.src):
			space = 0
			while self.src[self.reader] == ' ':
				space += 1
				self.reader += 1
			c = self.src[self.reader]

			if c == '+':
				if space == 1: self.duplicate()
				if space == 2: self.swap2()
				if space == 3: self.rotate3()
				if space == 4: self.pop()
				if space >= 5: self.push(space - 5)
			if c == '*':
				if space % 5 == 0: self.plus()
				if space % 5 == 1: self.minus()
				if space % 5 == 2: self.prod()
				if space % 5 == 3: self.div()
				if space % 5 == 4: self.mod()
			if c == '.':
				if space % 2 == 0: self.print_num()
				if space % 2 == 1: self.print_chr()
			if c == ',':
				if space % 2 == 0: self.read_num()
				if space % 2 == 1: self.read_chr()
			if c == '`': self.mark_label(space)
			if c == '\'': self.check_label(space)
			self.reader += 1
	
	def duplicate(self):
		self.stack.append(self.stack[-1])

	def swap2(self):
		y = self.stack.pop()
		x = self.stack.pop()
		self.stack.append(y)
		self.stack.append(x)

	def rotate3(self):
		z = self.stack.pop()
		y = self.stack.pop()
		x = self.stack.pop()
		self.stack.append(y)
		self.stack.append(z)
		self.stack.append(x)

	def pop(self):
		self.stack.pop()

	def push(self, n):
		self.stack.append(n)

	def plus(self):
		y = self.stack.pop()
		x = self.stack.pop()
		self.stack.append(x + y)
	
	def minus(self):
		y = self.stack.pop()
		x = self.stack.pop()
		self.stack.append(x - y)
	def prod(self):
		y = self.stack.pop()
		x = self.stack.pop()
		self.stack.append(x * y)

	def div(self):
		y = self.stack.pop()
		x = self.stack.pop()
		self.stack.append(x / y)

	def mod(self):
		y = self.stack.pop()
		x = self.stack.pop()
		self.stack.append(x % y)

	def print_num(self):
		x = self.stack.pop()
		sys.stdout.write(x)

	def print_chr(self):
		x = self.stack.pop()
		sys.stdout.write(chr(int(x)))
	
	def read_num(self):
		x = sys.stdin.read(1)
		self.stack.append(x)

	def read_chr(self):
		x = ord(sys.stdin.read(1))
		self.stack.append(x)

	def mark_label(self, n):
		self.labels[n] = self.reader

	def check_label(self, n):
		x = self.stack.pop()
		if x != 0:
			self.reader = labels[n]

def main():
	sourcecode = read_code()
	starry = Starry(sourcecode)
	starry.run()

if __name__ == "__main__":
	main()
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

class bf:
	def __init__(self, sourcecode):
		self.src = sourcecode
		self.reader = 0
		self.memory = [0] * 1000
		self.pointer = 500

	def run(self):
		while self.reader < len(self.src):
			c = self.src[self.reader]
			if c == '>':self.right()
			if c == '<':self.left()
			if c == '+':self.plus()
			if c == '-':self.minus()
			if c == '.':self.dot()
			if c == ',':self.comma()
			if c == '[':self.bra()
			if c == ']':self.cket()
			self.reader += 1
	
	def right(self):
		self.pointer += 1
	
	def left(self):
		self.pointer -= 1

	def plus(self):
		self.memory[self.pointer] += 1
	
	def minus(self):
		self.memory[self.pointer] -= 1
	
	def dot(self):
		sys.stdout.write(chr(self.memory[self.pointer]))

	def comma(self):
		self.memory[self.pointer] = ord(sys.stdin.read(1))
	
	def bra(self):
		if self.memory[self.pointer] != 0: return
		bracket = 1
		while self.reader < len(self.src) and bracket > 0:
			self.reader += 1
			if self.src[self.reader] == '[':
				bracket += 1
			if self.src[self.reader] == ']':
				bracket -= 1
		if bracket != 0:
			print("bracket is broken")
			exit(0)

	def cket(self):
		if self.memory[self.pointer] == 0: return
		bracket = 1
		while self.reader < len(self.src) and bracket > 0:
			self.reader -= 1
			if self.src[self.reader] == ']':
				bracket += 1
			if self.src[self.reader] == '[':
				bracket -= 1

def main():
	sourcecode = read_code()
	BF = bf(sourcecode)
	BF.run()
	
if __name__ == "__main__":
	main()
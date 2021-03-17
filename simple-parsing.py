DIGITS = "0123456789"
ALPHABETS = "abcdefghijklmnopqrstuvwxyz"
env = {}

def error(message):
	print(message)
	exit(0)

def read_number(string):
	string = string.strip()
	if string == "":error("syntax_error")

	if string[0] in DIGITS:
		return read_constant(string)

	if string[0] in ALPHABETS:
		return read_variable(string)

	error("syntax_error")

def read_constant(string):
	i = 0
	while i < len(string) and string[i] in DIGITS:
		i += 1
	return int(string[:i]), string[i:]


def read_variable(string):
	i = 0
	while i < len(string) and string[i] in ALPHABETS:
		i += 1
	return string[:i], string[i:]

def read_formula(string):
	string = string.strip()
	num, rest = read_number(string)
	if type(num) == str:
		if num not in env:error("no such variable {}".format(num))
		num = env[num]
	if rest == "":
		return num
	rest = rest.strip()

	if rest[0] == '+':
		return num + read_formula(rest[1:])
	if rest[0] == '*':
		return num * read_formula(rest[1:])
	if rest[0] == '-':
		return num - read_formula(rest[1:])
	if rest[0] == '/':
		return num / read_formula(rest[1:])
	error("syntax_error")

def read_substitute(string):
	string.strip()
	var, rest = read_variable(string)
	rest = rest.strip()
	if rest[0] != '=':error("syntax_error")
	env[var] = read_formula(rest[1:])
	return var

def read_command(string):
	if '=' in string:
		var = read_substitute(string)
		print("set {}".format(var))
	else:
		print(read_formula(string))


while True:
	read_command(input())
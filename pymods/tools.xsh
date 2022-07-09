def import_filepath(file_loc, imports=None, return_import=True, print_imports=False):
	import sys, os
	sys.path.append(os.path.dirname(os.path.expanduser(file_loc)))
	import_name = os.path.splitext(os.path.split(file_loc)[-1])[0]
	statement = f"from {import_name} import {', '.join(imports)}" if imports else f"import {import_name}"
	if print_imports:
		print(statement)
	exec(statement, globals())
	if return_import:
		return eval("imports")

def make_faker():
	from string import printable
	from secrets import choice
	from faker import Faker

	dat = Faker().profile()
	dat['password'] = ''.join(choice(printable[:-5]) for i in range(18))
	order = "name,username,password,mail,sex,birthdate,ssn,address".split(',')
	for i in order:
		print(f"{i}: {dat.pop(i)}")
	print()
	print('\n'.join(f"{k}: {v}" for k, v in dat.items()))

def make_uuid(length = 16):
	from random import choice
	from string import ascii_letters, digits
	
	chars = ascii_letters + digits
	return ''.join(choice(chars) for i in range(length))
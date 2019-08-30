from lark import Lark
from lark import exceptions
from lark import Transformer

l0_parser = Lark(r"""
	?term	: term2 | _S* "(" _S* term2 _S* ")" _S*
	
	?term2	: _S* "0" _S*										-> zero
			| _S* "true" _S*									-> true
			| _S* "false" _S*									-> false
			| _S* "succ" term									-> succ
			| _S* "pred" term									-> pred
			| _S* "iszero" _S* term								-> iszero
			| _S* "if" _S* term "then" _S* term "else" _S* term	-> if_t_e

	_S		: " "
			| "\n"
			| "\t"

	""", start='term')

class Transf(Transformer):
	term = tuple
	zero = lambda self, _: '0'
	true = lambda self, _: 'true'
	false = lambda self, _: 'false'
	
	def succ(self, items):
		return ('succ', items[0]) 

	def pred(self, items):
		return ('pred', items[0]) 

	def iszero(self, items):
		return ('iszero', items[0]) 

	def if_t_e(self, items):
		return ('if', items[0], items[1], items[2])	

def parse(sentence='if (true) then (pred (0)) else false'):
	try:
		tree = l0_parser.parse(sentence)
		tree = Transf().transform(tree)
	except:
		print('Parsing went wrong')
		return False
	return tree

if __name__ == '__main__':
	print('This is an L0 parser module made by Artur Waquil Campana')

class Number(object):
	def __init__(self,value):
		self.value=value

	def __str__(self):
		return str(self.value)

	def reducible(self):
		return False

class Boolean(object):
	def __init__(self,value):
		self.value=value

	def __str__(self):
		return str(self.value)

	def __eq__(self,other):
		return self.value==other.value

	def reducible(self):
		return False

class Add(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

	def __str__(self):
		return str(self.left)+'+'+str(self.right)

	def reducible(self):
		return True

	def _reduce(self,environment):
		if self.left.reducible():
			return Add(self.left._reduce(environment),self.right)
		elif self.right.reducible():
			return Add(self.left,self.right._reduce(environment))
		else:
			return Number(self.left.value+self.right.value)

class Multiply(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

	def __str__(self):
		return str(self.left)+'*'+str(self.right)

	def reducible(self):
		return True

	def _reduce(self,environment):
		if self.left.reducible():
			return Multiply(self.left._reduce(environment),self.right)
		elif self.right.reducible():
			return Multiply(self.left,self.right._reduce(environment))
		else:
			return Number(self.left.value*self.right.value)

class Minus(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

	def __str__(self):
		return str(self.left)+'-'+str(self.right)

	def reducible(self):
		return True

	def _reduce(self,environment):
		if self.left.reducible():
			return Minus(self.left._reduce(environment),self.right)
		elif self.right.reducible():
			return Minus(self.left,self.right._reduce(environment))
		else:
			return Number(self.left.value-self.right.value)

class Divide(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

	def __str__(self):
		return str(self.left)+'/'+str(right)

	def reducible(self):
		return True

	def _reduce(self,environment):
		if self.left.reducible():
			return Divide(self.left._reduce(environment),self.right)
		elif self.right.reducible():
			return Divide(self.left,self.right._reduce(environment))
		else:
			return Number(self.left.value/self.right.value)

class LessThan(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

	def __str__(self):
		return str(self.left)+'<'+str(self.right)

	def reducible(self):
		return True

	def _reduce(self,environment):
		if self.left.reducible():
			return LessThan(self.left._reduce(environment),self.right)
		elif self.right.reducible():
			return LessThan(self.left,self.right._reduce(environment))
		else:
			return Boolean(self.left.value<self.right.value)

class Variable(object):
	def __init__(self,name):
		self.name=name

	def __str__(self):
		return str(self.name)

	def reducible(self):
		return True

	def _reduce(self,environment):
		return environment[self.name]

class DoNothing(object):
	def __init__(self):
		self.value='do nothing'

	def __eq__(self,other):
		return isinstance(other,DoNothing)

	def reducible(self):
		return False

class Assign(object):
	def __init__(self,name,expression):
		self.name=name 
		self.expression=expression

	def __str__(self):
		return str(self.name)+'='+str(self.expression)

	def reducible(self):
		return True

	def _reduce(self,environment):
		if self.expression.reducible():
			return Assign(self.name,self.expression._reduce(environment))
		else:
			environment[self.name]=self.expression
			return DoNothing()

class If(object):
	def __init__(self,condition,consequence,alternative):
		self.condition=condition
		self.consequence=consequence
		self.alternative=alternative

	def __str__(self):
		return 'if(%s){%s}else{%s}' %(str(self.condition),str(self.consequence),str(self.alternative))

	def reducible(self):
		return True

	def _reduce(self,environment):
		if self.condition.reducible():
			return If(self.condition._reduce(environment),self.consequence,self.alternative)
		else:
			if self.condition==Boolean(True):
				return self.consequence
			else:
				return self.alternative

class Sequence(object):
	def __init__(self,first,second):
		self.first=first 
		self.second=second 

	def __str__(self):
		return str(self.first)+','+str(self.second)

	def reducible(self):
		return True

	def _reduce(self,environment):
		if self.first==DoNothing():
			return self.second
		elif self.first.reducible():
			return Sequence(self.first._reduce(environment),self.second)
		else:
			return self.second

class While(object):
	def __init__(self,condition,body):
		self.condition=condition
		self.body=body

	def __str__(self):
		return 'while(%s){%s}' %(str(self.condition),str(self.body))

	def reducible(self):
		return True

	def _reduce(self,environment):
		return If(self.condition,Sequence(self.body,self),DoNothing())


class Machine(object):
	def __init__(self,expression,environment):
		self.expression=expression
		self.environment=environment

	def step(self):
		self.expression=self.expression._reduce(self.environment)

	def run(self):
		while self.expression.reducible():
			print self.expression
			self.step()
		print self.expression.value


def main():
	environment=dict()
	environment['x']=Number(2)
	expression=While(LessThan(Variable('x'),Number(5)),Assign('x',Add(Variable('x'),Number(2))))
	#expression=Assign('x',Add(Variable('x'),Number(2)))
	machine=Machine(expression,environment)
	machine.run()
	print environment['x']

if __name__ == '__main__':
	main()


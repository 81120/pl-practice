class Number(object):
	def __init__(self,value):
		self.value=value 

	def reducible(self):
		return False

class Boolean(object):
	def __init__(self,value):
		self.value=value

	def reducible(self):
		return False

class Add(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

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

	def reducible(self):
		return True

	def _reduce(self,environment):
		if self.left.reducible():
			return Multiply(self.left._reduce(environment),self.right)
		elif self.right.reducible():
			return Multiply(self.left,self.right._reduce(environment))
		else:
			return Number(self.left.value*self.right.value)

class LessThan(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

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

	def reducible(self):
		return True

	def _reduce(self,environment):
		return environment[self.name]

class DoNothing(object):
	def __init__(self):
		self.value='do nothing'

	def reducible(self):
		return False

class Assign(object):
	def __init__(self,name,expression):
		self.name=name 
		self.expression=expression

	def reducible(self):
		return True

	def _reduce(self,environment):
		if self.expression.reducible():
			return self.expression._reduce(environment)
		else:
			environment[self.name]=self.expression.value
			return DoNothing()

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
	print 'the initial environment'
	print environment
	expression=list()
	expression.append(Add(Multiply(Number(2),Number(3)),Multiply(Number(1),Number(4))))
	expression.append(Boolean(True))
	expression.append(LessThan(Number(2),Number(3)))
	expression.append(Variable('x'))
	expression.append(Assign(Variable('x'),Number(3)))
	i=1
	for exp in expression:
		print 'the caculation of the %d expression:' % i
		print 'the result:'
		i=i+1
		machine=Machine(exp,environment)
		machine.run()
		print 'the environment:'
		print environment

if __name__ == '__main__':
	main()


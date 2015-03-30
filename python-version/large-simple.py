class Environment(dict):
	def __str__(self):
		result='{'
		for k in self:
			result=result+str(k)+'=>'+str(self[k])+','
		result=result+'}'
		return result

class Number(object):
	def __init__(self,value):
		self.value=value

	def __str__(self):
		return str(self.value)

	def evaluate(self,environment):
		return self

class Boolean(object):
	def __init__(self,value):
		self.value=value

	def __str__(self):
		return str(self.value)

	def evaluate(self,environment):
		return self 

class Add(object):
	def __init__(self,left,right):
		self.left=left 
		self.right=right 

	def __str__(self):
		return str(self.left)+'+'+str(self.right)

	def evaluate(self,environment):
		return Number(self.left.evaluate(environment).value+self.right.evaluate(environment).value)

class LessThan(object):
	def __init__(self,left,right):
		self.left=left 
		self.right=right 

	def __str__(self):
		return str(self.left)+'<'+str(self.right)

	def evaluate(self,environment):
		return Boolean(self.left.evaluate(environment).value<self.right.evaluate(environment).value)

class Variable(object):
	def __init__(self,name):
		self.name=name 

	def __str__(self):
		return self.name 

	def evaluate(self,environment):
		return environment[self.name]

class Assign(object):
	def __init__(self,name,expression):
		self.name=name 
		self.expression=expression

	def __str__(self):
		return self.name+'='+str(self.expression)

	def evaluate(self,environment):
		environment[self.name]=self.expression.evaluate(environment)

class DoNothing(object):
	def __eq__(self,other):
		return isinstance(other,DoNothing)

	def evaluate(self,environment):
		pass

class If(object):
	def __init__(self,condition,consequence,alternative):
		self.condition=condition
		self.consequence=consequence
		self.alternative=alternative

	def __str__(self):
		return 'if('+str(self.condition)+'){'+str(self.consequence)+'}else{'+str(self.alternative)+'}'

	def evaluate(self,environment):
		if self.condition.evaluate(environment).value:
			self.consequence.evaluate(environment)
		else:
			self.alternative.evaluate(environment)

class Sequence(object):
	def __init__(self,first,second):
		self.first=first 
		self.second=second 

	def __str__(self):
		return str(self.first)+','+str(self.second)

	def evaluate(self,environment):
		self.first.evaluate(environment)
		self.second.evaluate(environment)

class While(object):
	def __init__(self,condition,body):
		self.condition=condition
		self.body=body 

	def __str__(self):
		return 'while('+str(self.condition)+'){'+str(self.body)+'}'

	def evaluate(self,environment):
		if self.condition.evaluate(environment).value:
			self.body.evaluate(environment)
			self.evaluate(environment)
		else:
			pass 

def main():
	environment=Environment()
	environment['x']=Number(0)
	print environment
	expression=Sequence(Assign('x',Number(3)),Assign('x',Number(4)))
	expression=While(LessThan(Variable('x'),Number(5)),Assign('x',Add(Variable('x'),Number(2))))
	expression.evaluate(environment)
	print environment

if __name__ == '__main__':
	main()

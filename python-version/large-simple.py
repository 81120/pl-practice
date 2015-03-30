class Environment(dict):
	def __str__(self):
		result='{'
		for k in self:
			result=result+str(k)+'=>'+str(self[k])+','
		result=result+'}'
		return result

class Parameters(list):
	def __str__(self):
		if len(self)==0:
			return '[]'
		else:
			return '['+reduce(lambda u,v:u+','+v,map(str,self))+']'

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

class Lambda(object):
	def __init__(self,parameters,body):
		self.parameters=parameters
		self.body=body

	def __str__(self):
		return 'lambda '+str(self.parameters)+'{'+str(self.body)+'}'

	def evaluate(self,environment):
		environment[str(self)]=self

class Call(object):
	def __init__(self,function,values):
		self.function=function 
		self.values=values 

	def __str__(self):
		return 'call '+str(self.function)+' with '+str(values)

	def evaluate(self,environment):
		local_environment=Environment()
		for i in range(len(self.function.parameters)):
			local_environment[self.function.parameters[i]]=self.values[i].evaluate(environment)
		return self.function.body.evaluate(local_environment)

def main():
	environment=Environment()
	environment['x']=Number(0)
	print environment
	expression=Sequence(Assign('x',Number(3)),Assign('x',Number(4)))
	expression=While(LessThan(Variable('x'),Number(5)),Assign('x',Add(Variable('x'),Number(2))))
	expression.evaluate(environment)
	print environment
	x=Parameters()
	print x
	x.append('x')
	x.append('y')
	print x

	print 'test lambda'
	expression=Call(Lambda(Parameters(['x']),Add(Variable('x'),Number(1))),Parameters([Number(1)]))
	print expression.evaluate(environment)
	print environment

if __name__ == '__main__':
	main()

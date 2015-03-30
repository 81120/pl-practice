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

class Minus(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right

	def __str__(self):
		return str(self.left)+'-'+str(self.right)

	def evaluate(self,environment):
		return Number(self.left.evaluate(environment).value-self.right.evaluate(environment).value)

class Times(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

	def __str__(self):
		return str(self.left)+'*'+str(self.right)

	def evaluate(self,environment):
		return Number(self.left.evaluate(environment).value*self.right.evaluate(environment).value)

class Divide(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

	def __str__(self):
		return str(self.left)+'/'+str(self.right)

	def evaluate(self,environment):
		return Number(self.left.evaluate(environment).value/self.right.evaluate(environment).value)

class LessThan(object):
	def __init__(self,left,right):
		self.left=left 
		self.right=right 

	def __str__(self):
		return '('+str(self.left)+'<'+str(self.right)+')'

	def evaluate(self,environment):
		return Boolean(self.left.evaluate(environment).value<self.right.evaluate(environment).value)

class GreaterThan(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

	def __str__(self):
		return '('+str(self.left)+'>'+str(self.right)+')'

	def evaluate(self,environment):
		return Boolean(self.left.evaluate(environment).value>self.right.evaluate(environment).value)

class Equal(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

	def __str__(self):
		return '('+str(self.left)+'='+str(self.right)+')'

	def evaluate(self,environment):
		return Boolean(self.left.evaluate(environment).value==self.right.evaluate(environment).value)

class And(object):
	def __init__(self,left,right):
		self.left=left 
		self.right=right 

	def __str__(self):
		return '('+str(self.left)+'&&'+str(self.right)+')'

	def evaluate(self,environment):
		return Boolean(self.left.evaluate(environment).value and self.right.evaluate(environment).value)

class Or(object):
	def __init__(self,left,right):
		self.left=left
		self.right=right 

	def __str__(self):
		return '('+str(self.left)+'||'+str(self.right)+')'

	def evaluate(self,environment):
		return Boolean(self.left.evaluate(environment).value or self.right.evaluate(environment).value)

class Not(object):
	def __init__(self,item):
		self.item=item 

	def __str__(self):
		return 'not('+str(self.item)+')'

	def evaluate(self,environment):
		return Boolean(not self.item.evaluate(environment).value)

class Variable(object):
	def __init__(self,name):
		self.name=name 

	def __str__(self):
		return self.name 

	def evaluate(self,environment):
		return environment[self.name]

class If(object):
	def __init__(self,condition,consequence,alternative):
		self.condition=condition
		self.consequence=consequence
		self.alternative=alternative

	def __str__(self):
		return 'if('+str(self.condition)+'){'+str(self.consequence)+'}else{'+str(self.alternative)+'}'

	def evaluate(self,environment):
		if self.condition.evaluate(environment).value:
			return self.consequence.evaluate(environment)
		else:
			return self.alternative.evaluate(environment)

class Assign(object):
	def __init__(self,name,expression):
		self.name=name 
		self.expression=expression

	def __str__(self):
		return str(self.name)+'='+str(self.expression)

	def evaluate(self,environment):
		environment[self.name]=self.expression.evaluate(environment)

class Block(object):
	def __init__(self,items):
		self.items=items 

	def __str__(self):
		return 'block:['+reduce(lambda u,v:u+','+v,map(str,self.items))+']'

	def evaluate(self,environment):
		for i in range(len(self.items)-1):
			self.items[i].evaluate(environment)
		return self.items[len(self.items)-1].evaluate(environment)


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

class Lambda(object):
	def __init__(self,parameters,body):
		self.parameters=parameters
		self.body=body

	def __str__(self):
		return 'lambda'+str(self.parameters)+'{'+str(self.body)+'}'

	def evaluate(self,environment):
		return self

class Call(object):
	def __init__(self,function,values):
		self.function=function 
		self.values=values 

	def __str__(self):
		return 'call '+str(self.function)+' with '+str(self.values)

	def evaluate(self,environment):
		local_environment=Environment()
		for i in range(len(self.function.parameters)):
			local_environment[self.function.parameters[i]]=self.values[i].evaluate(environment)
		return self.function.body.evaluate(local_environment)

def main():
	environment=Environment()
	print environment
	environment['x']=Number(1)
	expression=Call(Lambda(Parameters(['x']),If(LessThan(Variable('x'),Number(1)),Number(1),Number(2))),Parameters([Number(0)]))
	#expression=Minus(Number(5),Number(1))
	expression=Not(Or(LessThan(Number(2),Number(3)),GreaterThan(Number(2),Number(3))))
	function=Lambda(Parameters([]),Block([Assign('y',Number(0)),While(LessThan(Variable('y'),Number(5)),Assign('y',Add(Variable('y'),Number(2)))),Times(Variable('y'),Number(2))]))
	expression=Call(function,Parameters())
	print expression
	print expression.evaluate(environment)
	print environment

if __name__ == '__main__':
	main()
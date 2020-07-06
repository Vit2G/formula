# нахождение обратной формулы
# система уровнений на исходных данных
# константы - {"l":11,"h":12,"g":13}									l=11,h=12,g=13
# генератор значений {"x":[0,"rnd",[["l","*",["h","*","g"]],"-",1]]} 	x=rnd(0,l*h*g-1)
# система уравнений {"xl":["x","%","l"],								xl=x%l
#                    "xh":["x","%","h"],								xh=x%h
#                    "xg":["x","%","g"]}								xg=x%g
# найти f(l,h,g,xl,xh,xg) = x

import random
import json
import sys

# вычисление
add=lambda a,b: a+b
sub=lambda a,b: a-b
mul=lambda a,b: a*b
div=lambda a,b: a/b
mod=lambda a,b: a%b
pow=lambda a,b: a**b
rnd=lambda a,b: random.randint(a,b)


fun={"+":add,"-":sub,"*":mul,"/":div,"^":pow,"%":mod,"rnd":rnd}

def calcOps(ops,src):
	tops=type(ops)
	if tops==int:	# вычисленное значение
		return ops	# возвращаем значение
	
	if tops==str:	# мнемоника
		if type(src[ops])==int:	# мнемоника вычисленна - 
			return src[ops]		# возвращаем значение мнемоники
		else:					# мнемока может быть только формулой
			return calc(src[ops],src)	# возвращаем значение вычисленной формулы
		
	if tops == list:			# значение формула
		return calc(ops,src)	# возвращаем значение вычисленной формулы
	
	

def calc(formula,src):
	
	if type(formula)==int:
		return formula
		
	op1,op,op2 = formula
	
	op1 = calcOps(op1,src)
	op2 = calcOps(op2,src)
	
	return fun[op](op1,op2)

# генерация значений переменных и верного результата

def genData(data):
	res=data.copy()
	
	for d in res:
		res[d]=calc(res[d],res)
	return res
	
def genFormula(srs,ops,level=5):
	lsrs=len(srs)
	if level==0:
		return srs[random.randint(0,lsrs-1)],1
	
	while True:	
		op1=random.randint(0,lsrs+lsrs)
		op2=random.randint(0,lsrs+lsrs)
		op=random.randint(0,len(ops)-1)
		
		if op1==op2 and op1<lsrs and ops[op] in ["-","%"]:
			continue
		
		break
	
	if op1<lsrs:
		op1=srs[op1]
		steps1=1
	else:
		op1,steps1=genFormula(srs,ops,level-1)
		
	if op2<lsrs:
		op2=srs[op2]
		steps2=1
	else:
		op2,steps2=genFormula(srs,ops,level-1)
		
	return [op1,ops[op],op2],steps1+steps2


data={"l":14,"h":15,
		"x":[1,"rnd",[["l","*","h"],"-",1]],	
		"xl":["x","%","l"],
		"xh":["x","%","h"]
	}
	
# список переменных
srs=["l","h","xl","xh"]
# список допустимых операция
ops=["+","-","*","%"]
log=open("formula.log","wb")
m=0
while True:
	
	formula,steps = genFormula(srs,ops,7)
	if steps<5:	
		continue
		
	lres=[]
	for i in range(100):
		resault=0
		while resault==0:
			values=genData(data)
			resault=values["x"]
			
		try:
			res=calc(formula,values)
		except:
			break
		
		if res==resault:
			lres.append(res)
			continue
			
		break
	
	if len(lres)>m or len(lres)==100:
		m=len(lres)
		sformula=json.dumps(formula).replace('[','(').replace(']',')').replace(' ',' ').replace(',','').replace('"','')
		print m,lres,sformula
		log.write(sformula+"\n")
		log.write(json.dumps(lres)+"\n")
		log.flush()
	
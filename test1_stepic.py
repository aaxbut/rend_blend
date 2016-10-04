import math


def s_tri(a,b,c):
		p = (a+b+c)/2
		return math.sqrt(p*(p-a)*(p-b)*(p-c))
if __name__ == '__main__':
	a = int(input('enter a :'))
	b = int(input('enter b :'))
	c = int(input('enter c :'))
	print(s_tri(a,b,c))

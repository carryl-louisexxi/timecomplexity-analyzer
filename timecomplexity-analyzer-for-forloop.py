from abc import ABC, abstractmethod
import re
import math 
from fractions import Fraction



class Iterable:
    def __init__(self, mi, isn, islog, i, n, log, simp, many, one):
        self.mi = mi
        self.isn = isn 
        self.islog = islog 
        self.i = i 
        self.n = n 
        self.log = log 
        self.simp = simp 
        self.many = many 
        self.one = one 
        self.values = []

    def digit(self): 
        if self.islog:  return self.log_digit() 
        else:   return self.real_digit()

    def log_digit(self): 
        pass
    
    def real_digit(self): 
        pass 

    def alpha(self): 
        if self.islog:  return self.log_alpha()
        else:   return self.real_alpha()

    def log_alpha(self):
        x , y = self.many 

        x = '{} log({}){}'.format(x, self.log, self.n)
        y = '{} log({}){}'.format(y, self.log, self.n)
        
        return x, y, self.one

    def i_summation(self, num, n):
        x = '{}{}^2/2'.format(num, n)
        y = '{}{}/2'.format(eval(num), n)
        self.values.append(x)
        self.values.append(y)
        return 0

    def real_alpha(self): 
        for i, x in enumerate(list(self.many)):

            if type(x) == str:
                num = x[:x.find(next(filter(str.isalpha, x)))]
                iden = x[x.find(next(filter(str.isalpha, x))):]
                if self.n == iden:
                    val = '{}{}^2'.format(num, self.n)
                elif self.mi == iden: 
                    val = self.i_summation(num, self.n)
                else:
                    val = '{}{}{}'.format(num, self.n, iden)

            elif type(x) == int:
                val = '{}{}'.format(x, self.n)

            self.values.append(val)

        return tuple(self.values) + (self.one, )

    def calculate(self): 
        if type(self.n) == int:   return self.digit()
        else:    return self.alpha()

class NotIterable:
    def __init__(self, mi, isn, islog, i, n, log, simp, many, one):
        self.mi = mi
        self.isn = isn 
        self.islog = islog 
        self.i = i 
        self.n = n 
        self.log = log 
        self.simp = simp 
        self.many = many 
        self.one = one 

    def digit(self): 
        if self.islog:  return self.log_digit() 
        else:   return self.real_digit()

    def log_digit(self): 
        if self.isn:
            return (self.many * int(math.log(self.n, self.log))) + (self.one)
        else:
            return (self.many * int(math.log(self.n - 1, self.log))) + (self.one)
    
    def real_digit(self): 
        if self.isn:
            return ((self.many) * (self.n - 0 - self.i + 1)) + (self.one)
        else:
            return ((self.many) * (self.n - 1 - self.i + 1)) + (self.one)

    def alpha(self): 
        if self.islog:  return self.log_alpha()
        else:   return self.real_alpha()

    def log_alpha(self):
        if self.isn:
            return '{} log({}){}'.format(self.many, self.log, self.n), (self.one) 
        else:
            return '{} log({}){}'.format(self.many, self.log, self.n), ((self.many * -1) + (self.one))

    def real_alpha(self): 
        if '/' in self.n:
            pos = self.n.find(next(filter(str.isdigit, self.n)))
            denom =  Fraction('1/'+ self.n[pos:])   
            if self.isn:
                if (-self.i + 1) == 0: 
                    return  '{}{}'.format(self.many, self.n), math.floor(self.one * denom)
                else: 
                    return '{}{}'.format(self.many, self.n), (self.many * (-self.i + 1)) + (self.one)
            else: #n/2 - 1
                pass
        else:
            if self.isn:
                if type(self.i) == str: #ex. 3n - 3i + 5
                    return '{}{}'.format(self.many, self.n), '{}{}'.format(-self.many, self.i), (self.many + self.one)
                elif (-self.i+1) == 0: #ex. 3n + 2
                    return  '{}{}'.format(self.many, self.n), (self.one)
                else: #ex.3(n-1) + 2 = 3n-1 + 2 
                    return '{}{}'.format(self.many, self.n), ((self.many) * (-self.i + 1)) + (self.one)
            else: #ex.3(n-2-1+1) = 3(n-2) = 3n-6 + 2
                return '{}{}'.format(self.many, self.n), (self.many * -self.i) + (self.one)

    def calculate(self): 
        if type(self.n) == int:   return self.digit()
        else:    return self.alpha()

class Time(ABC):
    @abstractmethod
    def calculate(self): pass 

class TimeCalculator:
    def __init__(self, string, many, iter, one): 
        self.mi = string[0]
        self.isn = string[1]
        self.islog = string[2]
        self.i = string[3]
        self.n = string[4]
        self.log = string[5]
        self.simp = string[6]
        self.many = many
        self.iter = iter 
        self.one = one 

    def time(self, time):
        return time.calculate()

    def complexity(self):
        if self.iter:
            return self.time(Iterable(self.mi, self.isn, self.islog, self.i, self.n, self.log, self.simp, self.many, self.one))
        else: 
            return self.time(NotIterable(self.mi, self.isn, self.islog, self.i, self.n, self.log, self.simp, self.many, self.one))



class Initializer:
    def __init__(self, values):
       self.vals = [values[0], values[1], values[3], values[4], values[6], values[7]]
       self.o1 = values[2]
       self.o2 = values[5]
       self.o3 = values[8]
       self.mi = self.i = self.n = self.log = ''
       self.isn = self.islog = False 
       self.simple = 0

    def remove_space(self, string):
        return string.replace(' ', '')

    def revise(self, string):
        string = self.remove_space(string)
        if string.isdigit(): return int(string)
        else: return string 

    def is_complex(self, string):
        string = [1 for x in string if x in ['+', '-', '*', '/']]
        if not string: return False
        else: return True

    def pre_sum_vals(self):
        self.mi = self.vals[0]
        self.i = self.vals[1]
        self.n = self.vals[3]
        self.log = self.vals[5]

    def init_i_and_n(self):
        if type(self.n) == int and type(self.i) == int:
            if self.i > self.n:
                nn = self.n
                self.n = self.i
                self.i = nn 
            else: pass # if complex do it here 

    def init_i_cond(self):
        if self.i == self.vals[0]:
                self.i = 1

    def init_opers(self):
        if self.o2 == '>=' or self.o2 == '<=': self.isn = True 
        else:  self.isn = False 
        if self.o3 == '*=' or self.o3 == '/=': self.islog = True 
        else: self.islog = False 

    def initialize_summation(self):
        self.pre_sum_vals()
        self.init_i_and_n()
        self.init_i_cond()
        self.init_opers()
        return self.summation_values()

    def summation_values(self):
        return self.mi, self.isn, self.islog, self.i, self.n, self.log, self.simple

    def evaluate(self):
        for x, val in enumerate(self.vals):
            self.vals[x] = self.revise(val)
            if self.is_complex(val):
                try:
                    self.vals[x] = eval(val)
                except: pass 
        return self.initialize_summation()
        
class Splitter:
    def __init__(self, string):
        self.string = string 
        self.current = 0
        self.values = []
        self.token = self.char = self.left = self.right = self.op = ''

    def presplit(self): 
        self.string = re.split('[(;)]', self.string)
        self.string = [x for x in self.string if x] 
    
    def getNextToken(self):
        try:
            self.char = self.strings[self.current]
            self.current += 1 
        except:
            self.char = '$'

    def appendLeft(self):
        self.left += self.char 
        self.getNextToken()

    def appendRight(self, opers):
        if self.char not in opers:
            self.right += self.char 
        else:
            self.op += self.char 
        self.getNextToken()

    def getRightVals(self, opers):
        while self.char !=  '$':
            self.appendRight(opers)  

    def getLeftVals(self, opers):
        while self.char not in opers:
            self.appendLeft()
        self.getRightVals(opers)

    def reset(self):
        self.strings = self.char = self.left = self.right = self.op = ''
        self.current = 0  

    def evaluate(self, string, opers):
        self.reset()
        self.strings = string 
        self.getNextToken()
        self.getLeftVals(opers)
        return self.left, self.right, self.op

    def add_values(self, values):
        for x in values:
            self.values.append(x)

    def preinitialize(self):
        self.add_values(self.evaluate(self.string[1], ['=']))# initializer
        self.add_values(self.evaluate(self.string[2], ['=', '<', '>'])) # continuer
        self.add_values(self.evaluate(self.string[3], ['=', '+', '-', '*', '/'])) # updater

    def initializer(self):
        return Initializer(self.values)

    def splitting(self):
        self.presplit()
        self.preinitialize()
        return self.initializer().evaluate()

class Expression(ABC):
    @abstractmethod
    def calculate(self): pass 

class Loop(Expression):
    def __init__(self, string, result):
        self.string = string
        self.result = result 
        self.one = 0
        self.many = 0
        self.iter = False 

    def splitter(self): 
        return Splitter(self.string)  

    def time(self):
        return TimeCalculator(self.string, self.many, self.iter, self.one)

    def unpack(self): 
        self.one = 2 
        if type(self.result) == tuple:
            self.many = list(self.result)
            self.many[-1] += 2 
            self.iter = True 
        elif type(self.result) == int:
            self.many = self.result + 2 
            self.iter = False 
        
    def initialize(self):
        self.string = self.splitter().splitting()
        self.unpack()

    def calculate(self):
        self.initialize()
        x = self.time().complexity() # return something
        return x

class Simple(Expression):
    def __init__(self, string): 
        self.string = string

    def calculate(self): 
        tokens = re.split('\t|[0-9a-z();]| |<|"', self.string)
        tokens = [1 for x in tokens if x]

        if not tokens: return 1 
        else: return sum(tokens)

class ExpressionCalculator:
    def __init__(self): pass 

    def calculating(self, expression):
        return expression.calculate()



class Generator:
    def __init__(self, strings):
        self.expression = ExpressionCalculator()
        self.strings = strings
        self.queue = self.results = []
        self.string = ''
        self.current = 0

    def current_string(self): 
        try:
            self.string = self.strings[self.current]
            self.current += 1
        except:
            self.string = '$'

    def next_string(self):
        return self.strings[self.current]

    def the_string(self):
        string = self.queue[-1]
        self.queue.pop()
        return string

    def next(self): 
        if not self.next_string()[0].isspace():
            return self.expression.calculating(Simple(self.string)) # simple: return digits like 1

        self.queue.append(self.string)
        return self.expression.calculating(Loop(self.the_string(), self.generating())) # string and return simple value : value liek 3n + 4

    def root(self): 
        self.queue.append(self.string)
        self.results.append(self.expression.calculating(Loop(self.the_string(), self.generating()))) # string and return value 3n + 4 : value like the finish product, append to result list

    def generating(self): 
        self.current_string()
        if self.string == '$':
            return self.results
        elif self.string[0].isspace():
            return self.next()
        else:
            self.root()
            return self.generating()



class Converter: # sort of lexical analyzer
    def __init__(self, strings): 
        self.strings = strings
        self.token = ''
        self.current = 0
        self.values = ''

    def splitter(self):
        if '/' in self.token:
            copypos = len(self.token) - self.token.find('/')
            self.current += copypos

    def getNextToken(self):
        try:
            self.token = self.strings[self.current]
            self.current += 1 
            self.splitter()
        except: self.token = '$'

    def digit(self): 
        while self.token.isdigit():
            self.getNextToken()
        self.values += 'd'

        if self.token.isalpha():   self.aplha()
        else:   self.others()

    def aplha(self):
        i = self.current - 1
        if self.token == 'l' and self.strings[i+1] == 'o' and self.strings[i+2] == 'g' and self.strings[i+4].isdigit():
            self.current += 5
            self.values += 'log'
        else:   self.values += self.token
    
    def others(self):
        if self.token == ' ':
            self.values += ' '
        elif self.token == '^':
            self.values += '^'

    def evaluate(self): 
        self.getNextToken()

        if self.token == '$':
            return 
        elif self.token.isdigit():
            self.digit() 
        elif self.token.isalpha():
            self.aplha()
        else:
            self.others()
        self.evaluate()

    def converting(self):
        self.evaluate()
        return self.values

class PolyCalculator: # calculating polynomial values given by the generator
    def __init__(self, values):
        self.values = values 
        self.converted = [] 
        self.copy = []
        self.fraciden = ''
        self.normiden = ''

    def convert(self, value): 
        pos = value.find(next(filter(str.isalpha, value)))
        self.normiden = value[pos:]
        up = int(value[:pos])
        down = 1

        if '/' in value:
            self.fraciden = value[pos:]
            pos = value.find('/')
            down = int(value[pos+1:])

        return up, down

    def digit(self, copy, string):

        xup, xdw = self.convert(copy)
        yup, ydw = self.convert(string)

        m = str(xup) + '/' + str(xdw)
        n = str(yup) + '/' + str(ydw)

        mn = Fraction(eval(m + '+' + n))

        if self.fraciden:
            mn = str(mn)

            pos = mn.find('/')
            mn = mn[:pos]
            return mn + self.fraciden
        else:
            return str(mn) + self.normiden

    
    def split(self, x):
        return re.split('[ ]', x)

    def add(self, copy, string, converted):
        token = ''
        copy = self.split(copy)
        string = self.split(string)
        converted = self.split(converted)

        for cop, st, conv in zip(copy, string, converted):
            if 'd' in conv:
                if 'n' in conv:
                    token = self.digit(cop, st) 
                else:
                    token = str(eval(cop + '+' + st))
            else: 
                token += ' ' + st 
        return token

    def isSimilar(self, valsconverted, string): 
        for i, vals in enumerate(self.converted):
            if vals == valsconverted:
                self.copy[i] = self.add(self.copy[i], string, valsconverted)
                return True 
        return False

    def similarity(self, valsconverted, string): 
        if not self.isSimilar(valsconverted, string):
            self.converted.append(valsconverted)
            self.copy.append(string)

    def converter(self, string):
        return Converter(string)

    def evaluate(self):
        timecomplexity = ''
        for i in self.copy:
            timecomplexity += i + ' + '

        return 'T(n) = ' + timecomplexity[:-3]
        
    def arrange(self):
        arr = ['dn^d', 'dn', 'dn logn', 'd logn', 'd']
        carr = ['' for x in arr] 

        for i, x in enumerate(arr):
            for j, y in enumerate(self.converted):
                if x == y:
                    carr[i] = self.copy[j]

        self.copy = [x for x in carr if x]
        
    def calculate(self):
        for vals in self.values:
            if type(vals) == tuple:
                for string in vals:
                    string = str(string)
                    valsconverted = self.converter(string).converting()   
                    self.similarity(valsconverted, string)
            else:
                vals = str(vals)
                valsconverted = self.converter(vals).converting()
                self.similarity(valsconverted, vals)

        self.arrange()
        return self.evaluate()



class MainSystem: # class: asking input 
    def __init__(self):
        self.strings = []
        self.generator = Generator(self.strings)

    def main(self):
        choice = int(input(':'))

        for x in range(choice):
            string = input(':')
            self.strings.append(string)
        self.strings.append('$')

        value = self.generator.generating()
        value = PolyCalculator(value)
        print(value.calculate())


system = MainSystem()
system.main()

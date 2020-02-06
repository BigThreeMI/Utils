#!/usr/bin/env python
# coding: utf-8

# ## Closures and Decoratros in Python

# ### Reza Bagheri

# #### Scope of variables

# In[1]:


x = 1 # x is a global variable  
y = 5 # y is a global variable 
def f():
    global y 
    x = 2   # x is a local variable
    y += 1  # Reassigning the global variable y
    z = 10   # z is a local variable
    print("Local variable x =", x)
    print("Global variable y =", y)
    print("Local variable z =", z)
f()
print("Global variable  x =", x)
print("Global variable y =", y)


# In[2]:


a = [1, 2, 3]
b = 5
def func(x, y):
    x.append(4)
    y = y + 1

func(a, b)
print("a=", a)  
print("b=", b)  


# In[3]:


def f(x):
    y = 5
    z = 10
    t = 10
    def g():
        nonlocal y
        y += 1
        z = 20
        print("Nonlocal variable x =", x)
        print("Local variable z =", z) 
    print("Local variable t =", t)    
    g()
    print("Nonlocal variable x =", x)
    print("Nonlocal variable y =", y)
    print("Local variable z =", z)
f(5)
# This does not work:
# g()


# #### Closures

# In[4]:


def f():
    x = 5
    y = 10
    return x
h=f()


# In[5]:


def f(x):
    def g(y):
        return y
    return g
a = 5
b = 1
h=f(a)
h(b)  


# In[6]:


h.__name__


# In[7]:


def f(x):
    def g(y):
        return y
    return g(y)
a = 5
b = 1
h=f(a) 
# This does not work:
# h(b)


# In[8]:


def f(x):
    def g(y):
        return y
    return g
a = 5
b = 1
f(a)(b)  


# In[9]:


def f(x):
    def g(y):
        def h(z):
            return z
        return h
    return g
a = 5
b = 2
c = 1
f(a)(b)(c)  


# In[10]:


def f(x):
    z = 2
    def g(y):
        return z*x + y
    return g
a = 5
b = 1
h = f(a)
h(b)  


# In[11]:


h.__code__.co_freevars


# In[12]:


print(h.__code__.co_freevars[0], "=", h.__closure__[0].cell_contents) 
print(h.__code__.co_freevars[1], "=", h.__closure__[1].cell_contents)


# In[13]:


def f(x):
    z = 2
    def g(y):
        return y
    return g
a = 5
b = 1
h = f(a)
h(b)  


# In[14]:


h.__code__.co_freevars


# In[15]:


def f(x):
    z = 2
    t = 3
    def g(y):
        nonlocal t
        return y
    return g
a = 5
b = 1
h = f(a)
h(b)  
h.__code__.co_freevars  


# In[16]:


def f(x):
    def g(y = x):
        return y
    return g
a = 5
b = 1
h = f(a)
h()  


# In[17]:


def f(x):
    def g(y):
        def h(z):
            return x * y * z
        return h
    return g
a = 5
b = 2
c = 1
f(a)(b)(c)  


# In[18]:


f(a)(b).__code__.co_freevars


# In[19]:


f(a).__code__.co_freevars  


# In[20]:


def f(x):
    def g(y):
        def h(z):
            return y * z
        return h
    return g
a = 5
b = 2
c = 1
f(a).__code__.co_freevars  


# In[21]:


def f(x):
    z = 2
    return lambda y: z*x+y
a = 5
b = 1
f(a)(b)  


# In[22]:


class NthRoot:
    def __init__(self, n=2):
        self.n = n
    def set_root(n):
        self.n = n
    def calc(self, x):
        return x ** (1/self.n)
    
thirdRoot = NthRoot(3)
print(thirdRoot.calc(27))  
def nth_root(n=2):
    def calc(x):
        return x ** (1/n)
    return calc
third_root = nth_root(3)
print(third_root(27))  


# #### Composition

# In[23]:


def compose(g, f):
    def h(*args, **kwargs):
        return g(f(*args, **kwargs))
    return h


# In[24]:


inch_to_foot= lambda x: x/12
foot_meter= lambda x: x * 0.3048
inch_to_meter = compose(foot_meter, inch_to_foot)
inch_to_meter(12)   


# #### Partial application

# In[25]:


def partial(f, *f_args, **f_keywords):
    def g(*args, **keywords):
        new_keywords = f_keywords.copy()
        new_keywords.update(keywords)
        return f(*(f_args + args), **new_keywords)
    return g


# In[26]:


func = lambda x,y,z: x**2 + 2*y + z
pfunc = partial(func, 1)
pfunc(2, 3)  


# #### Currying

# In[27]:


def curry(f):
    argc = f.__code__.co_argcount
    f_args = []
    f_kwargs = {}
    def g(*args, **kwargs):
        nonlocal f_args, f_kwargs
        f_args += args
        f_kwargs.update(kwargs)
        if len(f_args)+len(f_kwargs) == argc:
            return f(*f_args, **f_kwargs)
        else:
            return g          
    return g


# In[28]:


cfunc = curry(func)
cfunc(1)(2)


# In[29]:


cfunc(3)


# In[30]:


cfunc = curry(func)
cfunc(1, 2)
cfunc(3)


# #### Decoration and decorators

# In[31]:


def f():
    return("f definition")
def g():
    return("g definition")
print("f is referring to ", f())
print("g is referring to ", g())
print("Swapping f and g")
temp = f
f = g
g = temp
print("f is referring to ", f())
print("g is referring to ", g())


# In[32]:


def deco(f):
    def g(*args, **kwargs):
        return f(*args, **kwargs)
    return g
def func(x):
     return 2*x
func = deco(func)
func(2)  


# In[33]:


func.__name__


# In[34]:


def deco(f):
    def g(*args, **kwargs):
        print("Calling ", f.__name__)
        return f(*args, **kwargs)
    return g
def func(x):
    return 2*x
func = deco(func)
func(2)


# #### Memoization

# In[35]:


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
for i in range(6):
    print(fib(i), end=" ")


# In[36]:


def memoize(f):
    memo = {}
    def memoized_func(n):
        if n not in memo:            
            memo[n] = f(n)
        return memo[n]
    return memoized_func


# In[37]:


fib = memoize(fib)
fib(30)


# #### Tracing recursive functions

# In[38]:


def trace(f):
    level = 1
    def helper(*arg):
        nonlocal level
        print((level-1)*"  │",  "  ┌",  f.__name__, "(", ",".join(map(str, arg)), ")", sep="")
        level += 1
        result = f(*arg)
        level -= 1
        print((level-1)*"  │", "  └",  result, sep="")
        return result
    return helper


# In[39]:


def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
fib = trace(fib)
fib(4)


# #### Syntactic sugar

# In[40]:


def deco(f):
    def g(*args, **kwargs):
        print("Calling ", f.__name__)
        return f(*args, **kwargs)
    return g
@deco
def func(x):
    return 2*x
func(2)


# #### Stacked decorators

# In[41]:


def deco1(f):
    def g1(*args, **kwargs):
        print("Calling ", f.__name__, "using deco1")
        return f(*args, **kwargs)
    return g1
def deco2(f):
    def g2(*args, **kwargs):
        print("Calling ", f.__name__, "using deco2")
        return f(*args, **kwargs)
    return g2
def func(x):
    return 2*x
func = deco2(deco1(func))
func(2)


# In[42]:


def deco1(f):
    def g1(*args, **kwargs):
        print("Calling ", f.__name__, "using deco1")
        return f(*args, **kwargs)
    return g1
def deco2(f):
    def g2(*args, **kwargs):
        print("Calling ", f.__name__, "using deco2")
        return f(*args, **kwargs)
    return g2
@deco2
@deco1
def func(x):
    return 2*x
func(2)


# In[43]:


def deco1(f):
    def g1(*args, **kwargs):
        print("Calling ", f.__name__, "using deco1")
        return f(*args, **kwargs)
    return g1
def deco2(f):
    def g2(*args, **kwargs):
        print("Calling ", f.__name__, "using deco2")
        return f(*args, **kwargs)
    return g2
deco = compose(deco2, deco1) 
@deco
def func(x):
    return 2*x
func(2)


# #### Tracing with memoization

# In[44]:


@trace
@memoize
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
fib(5)


# In[45]:


fib(6)


# #### Decorators with additional parameters

# In[46]:


def deco(msg_before, msg_after):
    def original_deco(f):
        def g(*args, **kwargs):
            print(msg_before + " " + f.__name__)
            result =  f(*args, **kwargs)
            print(msg_after + " " + f.__name__)
            return result
        return g
    return original_deco
def func(x):
    return 2*x
func = deco("Starting", "Finished")(func)
func(2)


# In[47]:


def deco(msg_before, msg_after):
    def original_deco(f):
        def g(*args, **kwargs):
            print(msg_before + " " + f.__name__)
            result =  f(*args, **kwargs)
            print(msg_after + " " + f.__name__)
            return result
        return g
    return original_deco
@deco("Starting", "Finished")
def func(x):
    return 2*x
func(2)


# In[48]:


def deco(msg_before, msg_after, f):
    def g(*args, **kwargs):
        print(msg_before + " " + f.__name__)
        result =  f(*args, **kwargs)
        print(msg_after + " " + f.__name__)
        return result
    return g
    
def func(x):
    return 2*x
func = deco("Starting", "Finished", func)
func(2)


# In[49]:


# This does not work:
#@deco("Starting", "Finished")
def func(x):
    return 2*x
func(2)


# In[50]:


@curry
def deco(msg_before, msg_after, f):
    def g(*args, **kwargs):
        print(msg_before + " " + f.__name__)
        result =  f(*args, **kwargs)
        print(msg_after + " " + f.__name__)
        return result
    return g
    
@deco("Starting", "Finished")
def func(x):
    return 2*x
func(2)


# #### Wrapping

# In[51]:


def wraps(f):
    def decorator(g):
        def helper(*args, **kwargs):
            return g(*args, **kwargs)
        attributes = ('__module__', '__name__', '__qualname__',
                      '__doc__', '__annotations__')         
        for attr in attributes:
            try:
                value = getattr(f, attr)
            except AttributeError:
                pass
            else:
                setattr(helper, attr, value)
        return helper
    return decorator


# In[52]:


def memoize(f):
    memo = {}
    @wraps(f)
    def memoized_func(n):
        if n not in memo:            
            memo[n] = f(n)
        return memo[n]
    return memoized_func


# In[53]:


@trace
@memoize
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
fib(5)


# In[54]:


fib(6)


# In[ ]:





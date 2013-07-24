import traceback

# assert that var is of vartype
def t(vartype, var):
    #assert(type(var) == vartype)
    if not type(var) == vartype:
        raise Exception('variable "' + str(var) + '" is of type ' + 
            str(type(var)) + ', not of type ' + str(vartype))
    return var

# use as a function decorator.  asserts function returns type vartype
# example: @returns(int)
#          def add_one(x):
#              return int(x+1)
def returns(vartype):
    def wrapper(f):
        def wrapped(*args, **kwargs):
            output = f(*args, **kwargs)
            if not type(output) == vartype:
                raise Exception('function "'+f.__name__+'" should return type '
                                +str(vartype)+' but returned type '
                                +str(type(output))+' with value: '
                                +str(output))
            return t(vartype, output)
        return wrapped
    return wrapper


# use as a function decorator.  asserts parapeters of specified length & type
# (does not require you specify all kwarg types)
# example: @takes(int,str,x=int,y=int)
#          def f(a,b,x=0,y=0,z=0):
def takes(*args_types, **kwargs_types):
    def wrapper(f):
        def wrapped(*args, **kwargs):
            error = False
            errormsg = ''
            if not len(args) == len(args_types):
                error = True
                errormsg += ('"takes()" expected function "'+f.__name__
                            +'" to receive '+str(len(args_types))
                            +' arguments, but '+str(len(args))+' were given.\n')
            for i in range(min(len(args),len(args_types))):
                if not type(args[i]) == args_types[i]:
                    error = True
                    errormsg += ('"takes()" expected parameter #'+str(i+1)
                                +' of function "'+f.__name__+'" to be type '
                                +str(args_types[i])+' but it received  type '
                                +str(type(args[i]))+' with value: '
                                +str(args[i])+'\n')
            for argname in kwargs_types:
                if argname in kwargs:
                    if not type(kwargs[argname]) == kwargs_types[argname]:
                        error = True
                        errormsg += ('takes() expected kwarg "'+str(argname)
                                    +'" of "'+f.__name__+'" to have type '
                                    +str(kwargs_types[argname])
                                    +' but received type '
                                    +str(type(kwargs[argname]))+' with value: '
                                    +str(kwargs[argname]))
            if error:
                raise Exception(errormsg)
            return f(*args, **kwargs)
        return wrapped
    return wrapper


# acts like print, but also prints code context it was called from
# usage: dprint(x+2): <'dprint: file file.py, function f, line 0:\n 'x+2' --> 5>
def dprint(var):
    stack = traceback.extract_stack()
    filename, lineno, function_name, code = stack[-2]
    print('dprint: file "'+filename+'", function "'+function_name
            +'", line #'+str(lineno)+':')
    l_index = code.index('dprint(')+7
    r_index = code.rindex(')')
    print('\t"'+code[l_index : r_index]+'" --> '+str(var))

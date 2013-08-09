import traceback
import pdb


def returns(vartype):
    """ use as a function decorator.  asserts function returns type vartype
        example: @returns(int)
                 def add_one(x):
                     return int(x+1)
    """
    def wrapper(f):
        def wrapped(*args, **kwargs):
            output = f(*args, **kwargs)
            if not type(output) == vartype:
                raise Exception('function "'+f.__name__+'" should return type '
                                +str(vartype)+' but returned type '
                                +str(type(output))+' with value: '
                                +str(output))
            return output
        return wrapped
    return wrapper


def takes(*args_types, **kwargs_types):
    """ Use as a function decorator. asserts params of specified length & type
    (does not require you specify all kwarg types)
    example: @takes(int,str,x=int,y=int)
             def f(a,b,x=0,y=0,z=0):
    """
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


def print_enter_exit(print_vars=True):
    """ use as a function decorator. Prints when the function is called and
    when it returns.  if print_vars == True, then prints arguments, and result
    """
    def wrapper(f):
        def wrapped(*args, **kwargs):
            filename, lineno, _, _ = traceback.extract_stack()[-2]
            print('%s called from file %s line #%s' % (str(f), filename, lineno))
            if print_vars:
                for i in range(len(args)):
                    print('| argument#%s->%s' % (str(i), str(args[i])))
                for key in kwargs:
                    print('| kwarg %s -> %s' % (str(key), str(kwargs[key])))
            output = f(*args, **kwargs)
            print('exited %s (called from file %s line #%s)' % (str(f), filename, lineno))
            if print_vars:
                print('| returned: %s' % str(output))
            return output
        return wrapped
    return wrapper


def dprint(var):
    """ acts like print, but also prints code context it was called from
    usage: dprint(x+2): <'dprint: file file.py, function f, line 0:\n 'x+2'-->5>
    """
    stack = traceback.extract_stack()
    filename, lineno, function_name, code = stack[-2]
    print('dprint: file "'+filename+'", function "'+function_name
                                        +'", line #'+str(lineno)+':')
    if code == None: # if being executed from python shell
        print('\t"'+str(var)+'"')
    else: # if executed from file
        l_index = code.index('dprint(')+7
        r_index = code.rindex(')')
        print('\t"'+code[l_index : r_index]+'" --> '+str(var))


def assertd(exp):
    """ assert that exp is of type bool.  If exp is false, then print code
    context it was called from, then start pdb.
    """
    assert(isinstance(exp, bool))
    if not exp:
        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-2]
        print('assertd failed: file "'+filename+'" function "'
                +function_name+'", line #'+str(lineno)+': ')
        if code != None: # if not running from python shell
            l_index = code.index('assertd(')+8
            r_index = code.rindex(')')
            print('\t"'+code[l_index : r_index])
        print('starting pdb...')
        pdb.set_trace()


class StaticTypeHolder(object):
    """ Creates an object with method typeof(key, keytype). Once it is 
    called, the instance asserts that type of self.key is always keytype
    """
    def __init__(self):
        object.__setattr__(self, 'keytypes', {})

    def typeof(self, key, keytype):
        assert(isinstance(key, str))
        assert(isinstance(keytype, type))
        if hasattr(self, key):
            if not isinstance(eval('self.'+key), keytype):
                raise Exception(('self.'+key+' already exists and is of type '
                                                +str(type(eval('self.'+key)))))
        self.keytypes[key] = keytype

    def remove_typeof(self, key):
        assert(isinstance(key, str))
        if key in self.keytypes:
            del self.keytypes[key]
        else:
            raise Exception(key+' does not have a specified type.')

    def __setattr__(self, key, val):
        if key in self.keytypes:
            if not isinstance(val, self.keytypes[key]):
                raise Exception('self.'+key+' specified as type '
                      +str(self.keytypes[key])+' but attempted to assign type '
                                       +str(type(val))+' with value: '+str(val))
        object.__setattr__(self, key, val)

    def __getattribute__(self, key):
        val = object.__getattribute__(self, key)
        if key in object.__getattribute__(self, 'keytypes'):
            if not isinstance(val, self.keytypes[key]):
                raise Exception('self.'+key+' specified as type '+
                                str(self.keytypes[key])+' but holds type '+
                                     +str(type(val))+' with value: '+str(val))
            assert(isinstance(val, self.keytypes[key]))
        return val

    def __delattr__(self, key):
        if key in self.keytypes:
            del self.keytypes[key]
        object.__delattr__(self, key)

    def __str__(self):
        string = "StaticTypeHolder:"
        for key in self.keytypes:
            string += '\nself.'+key+' specified as type '+str(self.keytypes[key])
            if hasattr(self, key):
                string += '\n\tself.'+key+' = '+str(eval('self.'+key))
        return string



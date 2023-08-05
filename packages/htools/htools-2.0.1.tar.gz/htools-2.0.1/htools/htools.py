from abc import ABC, abstractmethod
from bz2 import BZ2File
from collections import namedtuple
from contextlib import contextmanager
from email.mime.text import MIMEText
from functools import wraps, partial
import inspect
from itertools import chain
import json
import os
import pickle
import re
import signal
import smtplib
import sys
import time
import warnings

from htools.config import get_credentials, get_default_user


class AutoInit:
    """Mixin class where child class has a long list of init arguments where 
    the parameter name and the class attribute will be the same. Note that 
    *args are not supported in the init method because each attribute that is
    defined in the resulting object must have a name. A variable length list
    of args can still be passed in as a single argument, of course, without the
    use of star unpacking.

    This updated version of AutoInit is slightly more user friendly than in V1
    (no more passing locals() to super()) but also slower and probably requires 
    more testing (all because of the frame hack in the init method). Note that 
    usage differs from the AutoInit present in htools<=2.0.0, so this is a  
    breaking change.

    Examples
    --------
    Without AutoInit:

    class Child:
        def __init__(self, name, age, sex, hair, height, weight, grade, eyes):
            self.name = name
            self.age = age
            self.sex = sex
            self.hair = hair
            self.height = height
            self.weight = weight
            self.grade = grade
            self.eyes = eyes
        def __repr__(self):
            return f'Child(name={self.name}, age={self.age}, sex={self.sex}, '\
                   f'hair={self.hair}, weight={self.weight}, '\
                   f'grade={self.grade}, eyes={self.eyes})'

    With AutoInit:

    class Child(AutoInit):
        def __init__(self, name, age, sex, hair, height, weight, grade, eyes):
            super().__init__()

    Note that we could also use the following method, though this is less
    informative when constructing instances of the child class and does not
    have the built in __repr__ that comes with AutoInit:

    class Child:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    """

    def __init__(self):
        # Calculate how many frames to go back to get child class.
        frame_idx = type(self).__mro__.index(AutoInit)
        attrs = {k: v for k, v in sys._getframe(frame_idx).f_locals.items()
                  if not k.startswith('__')}
        attrs.pop('self')
        bound = inspect.signature(self.__class__.__init__)\
                       .bind_partial(**attrs)
        
        # Flatten dict so kwargs are not listed as their own argument.
        bound.arguments.update(
            bound.arguments.pop('kwargs', {}).get('kwargs', {})
        )
        self._init_keys = set(bound.arguments.keys())
        for k, v in bound.arguments.items():
            setattr(self, k, v)

    def __repr__(self):
        """Returns string representation of child class including variables
        used in init method. For the example in the class docstring, this would
        return:

        child = Child('Henry', 8, 'm', 'brown', 52, 70, 3, 'green')
        Child(name='Henry', age=8, sex='m', hair='brown', height=52, 
              weight=70, grade=3, eyes='green')
        
        Returns
        -------
        str
        """
        fstrs = (f'{k}={repr(getattr(self, k))}' for k in self._init_keys)            
        return f'{self.__class__.__name__}({", ".join(fstrs)})'


def Args(**kwargs):
    """Wrapper to easily create a named tuple of arguments. Functions sometimes
    return multiple values, and we have a few options to handle this: we can
    return them as a regular tuple, but it is often convenient to be able to
    reference items by name rather than position. If we want the output to be
    mutable, we can return a dictionary, but this still requires more space
    than a tuple and bracket notation is arguably less convenient than dot
    notation. We can create a new namedtuple inside the function, but this
    kind of seems like overkill to create a new type of namedtuple for each
    function.

    Instead, this lets us create a namedtuple of Args on the fly just as easily
    as making a dictionary.

    Parameters
    ----------

    Examples
    --------
    def math_summary(x, y):
        sum_ = x + y
        prod = x * y
        diff = x - y
        quotient = x / y
        return Args(sum=sum_,
                    product=prod,
                    difference=diff,
                    quotient=quotient)

    >>> results = math_summary(4, 2)
    >>> results.product

    8

    >>> results.quotient

    2

    >>> results

    Args(sum=6, product=8, difference=2, quotient=2)
    """
    args = namedtuple('Args', kwargs.keys())
    return args(*kwargs.values())


@contextmanager
def assert_raises(error):
    """Context manager to assert that an error is raised. This can be nice
    if we don't want to clutter up a notebook with error messages.

    Parameters
    ----------
    error: class inheriting from Exception or BaseException
        The type of error to catch, e.g. ValueError.

    Examples
    --------
    # First example does not throw an error.
    >>> with assert_raises(TypeError) as ar:
    >>>     a = 'b' + 6

    # Second example throws an error.
    >>> with assert_raises(ValueError) as ar:
    >>>     a = 'b' + 6

    AssertionError: Wrong error raised. Expected PermissionError, got 
    TypeError(can only concatenate str (not "int") to str)

    # Third example throws an error because the code inside the context manager
    # completed successfully.
    >>> with assert_raises(ValueError) as ar:
    >>>     a = 'b' + '6'

    AssertionError: No error raised, expected PermissionError.
    """
    try:
        yield
    except error as e:
        print(f'As expected, got {error.__name__}({e}).')
    except Exception as e:
        raise AssertionError(f'Wrong error raised. Expected {error.__name__},'
                             f' got {type(e).__name__}({e}).') from None
    else:
        raise AssertionError(f'No error raised, expected {error.__name__}.')


class InvalidArgumentError(Exception):
    pass


class TimeExceededError(Exception):
    pass


def timebox_handler(time, frame):
    raise TimeExceededError('Time limit exceeded.')


@contextmanager
def timebox(time, strict=True):
    """Try to execute code for specified amount of time before throwing error.
    If you don't want to throw an error, use with a try/except block.

    Parameters
    ----------
    time: int
        Max number of seconds before throwing error.
    strict: bool
        If True, timeout will cause an error to be raised, halting execution of
        the entire program. If False, a warning message will be printed and 
        the timeboxed operation will end, letting the program proceed to the
        next step.

    Examples
    --------
    with time_box(5) as tb:
        x = computationally_expensive_code()

    More permissive version:
    x = step_1()
    with timebox(5) as tb:
        try:
            x = slow_step_2()
        except TimeExceededError:
            pass
    """
    try:
        signal.signal(signal.SIGALRM, timebox_handler)
        signal.alarm(time)
        yield
    except TimeExceededError as e:
        if strict: raise
        warnings.warn(e.args[0])
    finally:
        signal.alarm(0)


def timeboxed(time, strict=True):
    """Decorator version of timebox. Try to execute decorated function for
    `time` seconds before throwing exception.

    Parameters
    ----------
    time: int
        Max number of seconds before throwing error.
    strict: bool
        If True, timeout will cause an error to be raised, halting execution of
        the entire program. If False, a warning message will be printed and 
        the timeboxed operation will end, letting the program proceed to the
        next step.

    Examples
    --------
    @timeboxed(5)
    def func(x, y):
        # If function does not complete within 5 seconds, will throw error.
    """
    def intermediate_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with timebox(time, strict) as tb:
                return func(*args, **kwargs)
        return wrapper
    return intermediate_wrapper


class cached_property:
    """Decorator for computationally expensive methods that should only be
    computed once (i.e. they take zero arguments aside from self and are slow
    to execute). Lowercase name is used for consistency with more decorators.
    Heavily influenced by example in `Python Cookbook` by David Beazley and
    Brian K. Jones. Note that, as with the @property decorator, no parentheses
    are used when calling the decorated method.

    Examples
    --------
    class Vocab:

        def __init__(self, tokens):
            self.tokens = tokens

        @cached_property
        def embedding_matrix(self):
            print('Building matrix...')
            # Slow computation to build and return a matrix of word embeddings.
            return matrix

    # First call is slow.
    >>> v = Vocab(tokens)
    >>> v.embedding_matrix

    Building matrix...
    [[.03, .5, .22, .01],
     [.4, .13, .06, .55]
     [.77, .14, .05, .9]]

    # Second call accesses attribute without re-computing 
    # (notice no "Building matrix" message).
    >>> v = Vocab(tokens)
    >>> v.embedding_matrix

    [[.03, .5, .22, .01],
     [.4, .13, .06, .55]
     [.77, .14, .05, .9]]
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        """This method is called when the variable being accessed is not in the
        instance's state dict. The next time the attribute is accessed, the 
        computed value will be in the state dict so this method (and the method
        in the instance itself) is not called again unless the attribute is 
        deleted.
        """
        # When attribute accessed as class method, instance is None.
        if instance is None:
            return self

        # When accessed as instance method, call method on instance as usual.
        # Then set instance attribute and return value.
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val


class ReadOnly:
    """Descriptor to make an attribute read-only. This means that once a value
    has been set, the user cannot change or delete it. Note that read-only 
    attributes must first be created as class variables (see example below). 
    To allow more flexibility, we do allow the user to manually manipulate the 
    instance dictionary.

    Examples
    --------
    class Dog:
        breed = ReadOnly('breed')
        def __init__(self, breed, age):
            # Once breed is set in the line below, it cannot be changed.
            self.breed = breed
            self.age = age

    >>> d = Dog('dalmatian', 'Arnold')
    >>> d.breed

    'dalmatian'

    >>> d.breed = 'labrador'

    PermissionError: Attribute is read-only.

    >>> del d.breed
    
    PermissionError: Attribute is read-only.
    """

    def __init__(self, name):
        self.name = name
        self.initialized = set()

    def __get__(self, instance, cls):
        if instance is None:
            return self
        elif instance not in self.initialized:
            warnings.warn(
                f'Read-only attribute {self.name} has not been initialized.'
            )
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if instance not in self.initialized:
            instance.__dict__[self.name] = value
            self.initialized.add(instance)
        else:
            raise PermissionError('Attribute is read-only.')

    def __delete__(self, instance):
        raise PermissionError('Attribute is read-only.')


def validating_property(func, allow_del=False):
    """Factory that makes properties that perform some user-specified 
    validation when setting values. The returned function must be used as a
    descriptor to create a class variable before setting the instance 
    attribute.
    
    Parameters
    ----------
    func: function
        Function or lambda that accepts a single parameter. This will be used
        when attempting to set a value for the managed attribute. It should 
        return True if the value is acceptable, False otherwise.
    allow_del: bool
        If True, allow the attribute to be deleted.
        
    Returns
    -------
    function: A property with validation when setting values. Note that this 
        will be used as a descriptor, so it must create a class variable as
        shown below. In the example, also notice that the name passed to
        LengthyInt mustt match the name of the variable it is assigned to.
    
    Examples
    --------
    LengthyInt = validating_property(
        lambda x: isinstance(x, int) and len(str(int)) > 4
    )
    
    class Foo:
        long = LengthyInt('long')
        def __init__(self, a, long):
            self.a = a
            self.long = long
            
    >>> foo = Foo(3, 4)
    
    ValueError: Invalid value 4 for argument long.
   
    # No error on instantiation because the argument is a valid LengthyInt. 
    >>> foo = Foo(3, 543210)
    >>> foo.long

    543210
   
    >>> foo = Foo(3, 'abc')
    ValueError: Invalid value 'abc' for argument long.
    """
    def prop(name):
        @property
        def method(instance):
            return instance.__dict__[name]
        
        @method.setter
        def method(instance, val):
            if func(val):
                instance.__dict__[name] = val
            else:
                raise ValueError(f'Invalid value {val} for argument {name}.')
       
        if allow_del:
            @method.deleter
            def method(instance):
                del instance.__dict__[name]
        return method
    return prop


class Callback(ABC):
    """Abstract base class for callback objects to be passed to @callbacks
    decorator. Children must implement a __call__ method that accepts function
    inputs and outputs.
    """

    @abstractmethod
    def __call__(self, inputs, output=None):
        """
        Parameters
        -------------
        inputs: dict
            Dictionary of bound arguments passed to the function being 
            decorated.
        output: any
            Callbacks to be executed after the function call can pass the 
            function output to the callback. The default None value will remain
            for callbacks that execute before the function.
        """
        pass


def callbacks(*, on_begin=None, on_end=None):
    """Decorator that attaches callbacks to a function. Callbacks should be
    defined as classes inheriting from abstract base class Callback that 
    implement a __call__ method. This allows us to store states
    rather than just printing outputs or relying on global vars.

    Parameters
    ----------
    on_begin: list
        Callbacks to be executed before the decorated function.
    on_end: list
        Callbacks to be executed after the decorated function.

    Examples
    --------
    @callbacks(on_begin=[print_hyperparameters],
               on_end=[plot_activation_hist, activation_means, print_output])
    def train(**kwargs):
        # Train model and return loss.
    """
    on_begin = on_begin or []
    on_end = on_end or []
    def decorator(func):
        def wrapper(*args, **kwargs):
            bound = inspect.signature(func).bind_partial(*args, **kwargs)
            bound.apply_defaults()
            for cb in on_begin:
                cb(bound.arguments, None)
            out = func(*args, **kwargs)
            for cb in on_end:
                cb(bound.arguments, out)
            return out
        return wrapper
    return decorator


def typecheck(func_=None, **types):
    """Decorator to enforce type checking for a function or method. There are 
    two ways to call this: either explicitly passing argument types to the
    decorator, or letting it infer them using type annotations in the function
    that will be decorated. We allow multiple both usage methods since older
    versions of Python lack type annotations, and also because I feel the 
    annotation syntax can hurt readability.
    

    Parameters
    ----------
    func_: function
        The function to decorate. When using decorator with 
        manually-specified types, this is None. Underscore is used so that
        `func` can still be used as a valid keyword argument for the wrapped 
        function.
    types: type
        Optional way to specify variable types. Use standard types rather than
        importing from the typing library, as subscripted generics are not 
        supported (e.g. typing.List[str] will not work; typing.List will but at
        that point there is no benefit over the standard `list`). 
        
    Examples
    --------
    In the first example, we specify types directly in the decorator. Notice
    that they can be single types or tuples of types. You can choose to 
    specify types for all arguments or just a subset.
    
    @typecheck(x=float, y=(int, float), iters=int, verbose=bool)
    def process(x, y, z, iters=5, verbose=True):
        print(f'z = {z}')
        for i in range(iters):
            if verbose: print(f'Iteration {i}...')
            x *= y
        return x
    
    >>> process(3.1, 4.5, 0, 2.0)
    TypeError: iters must be <class 'int'>, not <class 'float'>.
    
    >>> process(3.1, 4, 'a', 1, False)
    z = a
    12.4
    
    Alternatively, you can let the decorator infer types using annotations
    in the function that is to be decorated. The example below behaves 
    equivalently to the explicit example shown above. Note that annotations
    regarding the returned value are ignored.
    
    @typecheck
    def process(x:float, y:(int, float), z, iters:int=5, verbose:bool=True):
        print(f'z = {z}')
        for i in range(iters):
            if verbose: print(f'Iteration {i}...')
            x *= y
        return x
        
    >>> process(3.1, 4.5, 0, 2.0)
    TypeError: iters must be <class 'int'>, not <class 'float'>.
    
    >>> process(3.1, 4, 'a', 1, False)
    z = a
    12.4
    """
    # Case 1: Pass keyword args to decorator specifying types.
    if not func_:
        return partial(typecheck, **types)
    # Case 2: Infer types from annotations. Skip if Case 1 already occurred.
    elif not types:
        types = {k: v.annotation 
                 for k, v in inspect.signature(func_).parameters.items()
                 if not v.annotation == inspect._empty}
    
    @wraps(func_)
    def wrapper(*args, **kwargs):
        fargs = inspect.signature(wrapper).bind(*args, **kwargs).arguments
        for k, v in types.items():
            if k in fargs and not isinstance(fargs[k], v):
                raise TypeError(
                    f'{k} must be {str(v)}, not {type(fargs[k])}.'
                )
        return func_(*args, **kwargs)
    return wrapper


def debug_call(func):
    """Decorator to help debug function calls. In general, this is not meant to
    permanently decorate a function, but rather to be used temporarily when
    debugging a function call. Note that a wrapped function that accepts *args
    will display a signature including an 'args' parameter even though it isn't
    a named parameter, because the goal here is to explicitly show which values
    are being passed to which parameters. This does mean that the printed 
    string won't be executable code in this case, but that shouldn't be
    necessary anyway since it would contain the same call that was just used.

    Parameters
    ----------
    func: function
        Function being decorated.
    
    Examples
    --------
    Occasionally, you might pass arguments to different parameters than you 
    intended. Throwing a debug_call decorator on the function helps you check
    that the arguments are matching up as expected. For example, the parameter
    names in the function below have an unexpected order, so you could easily
    make the following call and expect to get 8. The debug decorator helps
    catch that the third argument is being passed in as the x parameter.

    @debug_call
    def f(a, b, x=0, y=None, z=4, c=2):
        return a + b + c

    >>> f(3, 4, 1)
    f(a=3, b=4, x=1, y=None, z=4, c=9)
    9
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = inspect.signature(wrapper).bind_partial(*args, **kwargs)
        sig.apply_defaults()
        sig.arguments.update(sig.arguments.pop('kwargs', {}))
        arg_strs = (f'{k}={repr(v)}' for k, v in sig.arguments.items())
        print(f'{wrapper.__name__}({", ".join(arg_strs)})')
        return func(*args, **kwargs)
    return wrapper


class LambdaDict(dict):
    """Create a default dict where the default function can accept parameters.
    Whereas the defaultdict in Collections can set the default as int or list,
    here we can pass in any function where the key is the parameter.
    """

    def __init__(self, default_function):
        """
        Parameters
        ----------
        default_function: function
            When referencing a key in a LambdaDict object that has not been
            added yet, the value will be the output of this function called
            with the key passed in as an argument.
        """
        super().__init__()
        self.f = default_function

    def __missing__(self, key):
        self[key] = self.f(key)
        return self[key]


def hdir(obj, magics=False, internals=False):
    """Print object methods and attributes, by default excluding magic methods.

    Parameters
    -----------
    obj: any type
        The object to print methods and attributes for.
    magics: bool
        Specifies whether to include magic methods (e.g. __name__, __hash__).
        Default False.
    internals: bool
        Specifies whether to include internal methods (e.g. _dfs, _name).
        Default False.

    Returns
    --------
    dict
        Keys are method/attribute names, values are strings specifying whether
        the corresponding key is a 'method' or an 'attr'.
    """
    output = dict()
    for attr in dir(obj):
        # Exclude magics or internals if specified.
        if (not magics and attr.startswith('__')) or \
           (not internals and re.match('_[^_]', attr)):
            continue

        # Handle rare case where attr can't be invoked (e.g. df.sparse on a
        # non-sparse Pandas dataframe).
        try:
            is_method = callable(getattr(obj, attr))
        except Exception:
            continue

        # Update output to specify whether attr is callable.
        if is_method:
            output[attr] = 'method'
        else:
            output[attr] = 'attribute'
    return output


def tdir(obj, **kwargs):
    """A variation of the built in `dir` function that shows the
    attribute names as well as their types. Methods are excluded as they can
    change the object's state.

    Parameters
    ----------
    obj: any type
        The object to examine.
    kwargs: bool
        Additional arguments to be passed to hdir. Options are `magics` and
        `internals`. See hdir documentation for more information.

    Returns
    -------
    dict[str, type]: Dictionary mapping the name of the object's attributes to
    the corresponding types of those attributes.
    """
    return {k: type(getattr(obj, k)) 
            for k, v in hdir(obj, **kwargs).items() if v == 'attribute'}


def hmail(subject, message, to_email, from_email=None):
    """Send an email.

    Parameters
    -----------
    from_email: str
        Gmail address being used to send email.
    to_email: str
        Recipient's email.
    subject: str
        Subject line of email.
    message: str
        Body of email.

    Returns
    --------
    None
    """
    # Load source email address.
    from_email = from_email or get_default_user()
    if not from_email:
        return None

    # Load email password.
    password = get_credentials(from_email)
    if not password:
        return None

    # Create message instance.
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    # Access server and send email.
    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.starttls()
    server.login(user=from_email, password=password)
    server.send_message(msg)
    print(f'Email sent to {to_email}.')


def htimer(func):
    """Provide conservative time estimate for a function to run. Behavior may
    not be interpretable for recursive functions.

    Parameters
    -----------
    func: function
        The function to time.

    Examples
    ---------
    import time

    @htimer
    def count_to(x):
        for i in range(x):
            time.sleep(0.5)

    >>> count_to(10)
    [TIMER]: count_to executed in approximately 5.0365 seconds.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        output = func(*args, **kwargs)
        duration = time.perf_counter() - start
        print(f'\n[TIMER]: {func.__name__} executed in approximately '
              f'{duration:.3f} seconds.\n')
        return output
    return wrapper


@contextmanager
def block_timer():
    """Context manager to time a block of code. This works similarly to htimer
    but can be used on code outside of functions.

    Examples
    --------
    with block_timer() as bt:
        # Code inside the context manager will be timed.
        arr = [str(i) for i in range(25_000_000)]
        first = None
        while first != '100':
            arr.pop(0)
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        duration = time.perf_counter() - start
        print(f'[TIMER]: Block executed in {duration:.3f} seconds.')


def hsplit(text, sep, group=True, attach=True):
    """Flexible string splitting that retains the delimiter rather, unlike
    the built-in str.split() method.

    Parameters
    -----------
    text: str
        The input text to be split.
    sep: str
        The delimiter to be split on.
    group: bool
        Specifies whether to group consecutive delimiters together (True),
        or to separate them (False).
    attach: bool
        Specifies whether to attach the delimiter to the string that preceeds
        it (True), or to detach it so it appears in the output list as its own
        item (False).

    Returns
    --------
    list[str]

    Examples
    ---------
    text = "Score -- Giants win 6-5"
    sep = '-'

    # Case 0.1: Delimiters are grouped together and attached to the preceding
    word.
    >> hsplit(text, sep, group=True, attach=True)
    >> ['Score --', ' Giants win 6-', '5']

    # Case 0.2: Delimiters are grouped together but are detached from the
    preceding word, instead appearing as their own item in the output list.
    >> hsplit(text, sep, group=True, attach=False)
    >> ['Score ', '--', ' Giants win 6', '-', '5']

    Case 1.1: Delimiters are retained and attached to the preceding string.
    If the delimiter occurs multiple times consecutively, only the first
    occurrence is attached, and the rest appear as individual items in the
    output list.
    >> hsplit(text, sep, group=False, attach=True)
    >> ['Score -', '-', ' Giants win 6-', '5']

    # Case 1.2: Delimiters are retained but are detached from the preceding
    string. Each instance appears as its own item in the output list.
    >> hsplit(text, sep, group=False, attach=False)
    >> ['Score ', '-', '-', ' Giants win 6', '-', '5']
    """
    sep_re = re.escape(sep)
    regex = f'[^{sep_re}]*{sep_re}*'

    ##########################################################################
    # Case 0: Consecutive delimiters are grouped together.
    ##########################################################################
    if group:
        # Subcase 0.1
        if attach:
            return [word for word in re.findall(regex, text)][:-1]

        # Subcase 0.2
        else:
            return [word for word in re.split(f'({sep_re}+)', text) if word]

    ##########################################################################
    # Case 1: Consecutive delimiters are NOT grouped together.
    ##########################################################################
    words = text.split(sep)

    # Subcase 1.1
    if attach:
        return [word for word in re.findall(regex[:-1]+'?', text) if word]

    # Subcase 1.2
    return [word for word in chain(*zip(words, [sep]*len(words))) if word][:-1]


def print_object_sizes(space, limit=None, exclude_underscore=True):
    """Print the object names and sizes of the currently defined objects.

    Parameters
    -----------
    space: dict
        locals(), globals(), or vars()
    limit: int or None
        Optionally limit the number of objects displayed (default None for no
        limit).
    exclude_underscore: bool
        Determine whether to exclude objects whose names start with an
        underscore (default True).
    """
    var_size = [(var, sys.getsizeof(obj)) for var, obj in space.items()]
    for var, size in sorted(var_size, key=lambda x: -x[1])[:limit]:
        if not var.startswith('_') or not exclude_underscore:
            print(var, size)


def eprint(arr, indent=2, spacing=1):
    """Enumerated print. Prints an iterable with one item per line accompanied
    by a number specifying its index in the iterable.

    Parameters
    -----------
    arr: iterable
        The object to be iterated over.
    indent: int
        Width to assign to column of integer indices. Default is 2, meaning
        columns will line up as long as <100 items are being printed, which is
        the expected use case.
    spacing: int
        Line spacing. Default of 1 will print each item on a new line with no
        blank lines in between. Spacing of 2 will double space output, and so
        on for larger values.

    Returns
    --------
    None
    """
    for i, x in enumerate(arr):
        print(f'{i:>{indent}}: {x}', end='\n'*spacing)


def _read_write_args(path, mode):
    """Helper for `save` and `load` functions.
    
    Parameters
    ----------
    path: str
        Path to read/write object from/to.
    mode: str
        'w' for writing files (as in `save`), 'r' for reading files 
        (as in `load`).
    
    Returns
    -------
    tuple: Function to open file, mode to open file with (str), object to open
        file with.
    """
    ext = path.rpartition('.')[-1]
    if ext not in {'json', 'pkl', 'zip'}:
        raise InvalidArgumentError(
            'Invalid extension. Make sure your filename ends with .json, '
            '.pkl, or .zip.'
        )
        
    # Store in dict to make it easier to add additional formats in future.
    ext2data = {'pkl': (open, 'b', pickle), 
                'zip': (BZ2File, '', pickle), 
                'json': (open, '', json)}
    opener, mode_suffix, saver = ext2data[ext]
    return opener, mode + mode_suffix, saver

def save(obj, path, verbose=True):
    """Wrapper to save data as pickle (optionally zipped) or json.

    Parameters
    -----------
    obj: any
        Object to pickle.
    path: str
        File name to save pickled object to. Should end with .pkl, .zip, or 
        .json depending on desired output format. If .zip is used, object will
        be zipped and then pickled.
    verbose: bool
        If True, print a message confirming that the data was pickled, along
        with its path.

    Returns
    -------
    None
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    opener, mode, saver = _read_write_args(path, 'w')
    with opener(path, mode) as f:
        saver.dump(obj, f)
    if verbose: print(f'Data written to {path}.')


def load(path, verbose=True):
    """Wrapper to load pickled (optionally zipped) or json data.
    
    Parameters
    ----------
    path : str
        File to load. File type will be inferred from extension.
    verbose : bool, optional
        If True, will print message stating where object was loaded from.
    
    Returns
    -------
    object: The Python object that was pickled to the specified file.
    """
    opener, mode, saver = _read_write_args(path, 'r')
    with opener(path, mode) as f:
        data = saver.load(f)
    if verbose: print(f'Object loaded from {path}.')
    return data


def dict_sum(*args):
    """Given two or more dictionaries with numeric values, combine them into a
     single dictionary. For keys that appear in multiple dictionaries, their
     corresponding values are added to produce the new value.

     This differs from combining two dictionaries in the following manner:

     {**d1, **d2}

     The method shown above will combine the keys but will retain the value
     from d2, rather than adding the values from d1 and d2.

    Parameters
    -----------
    *args: dicts
        2 or more dictionaries with numeric values.

    Returns
    --------
    dict: Contains all keys which appear in any of the dictionaries that are
          passed in. The corresponding values from each dictionary containing a
          given key are summed to produce the new value.

    Examples
    ---------
    >>> d1 = {'a': 1, 'b': 2, 'c': 3}
    >>> d2 = {'a': 10, 'c': -20, 'd': 30}
    >>> d3 = {'c': 10, 'd': 5, 'e': 0}
    >>> dict_sum(d1, d2)

    {'a': 11, 'b': 2, 'c': -7, 'd': 35, 'e': 0}
    """
    keys = {key for d in args for key in d.keys()}
    return {key: sum(d.get(key, 0) for d in args)
            for key in keys}


def differences(obj1, obj2, methods=False, **kwargs):
    """Find the differences between two objects of the same type. This is a
    way to get more detail beyond whether two objects are equal or not.

    Parameters
    -----------
    obj1: any type
        An object.
    obj2: same type as obj1
        An object.
    methods: bool
        If True, include methods in the comparison. If False, only attributes
        will be compared. Note that the output may not be particularly
        interpretable when using method=True; for instance when comparing two
        strings consisting of different characters, we get a lot of output
        that looks like this:

        {'islower': (<function str.islower()>, <function str.islower()>),
        'isupper': (<function str.isupper()>, <function str.isupper()>),...
        'istitle': (<function str.istitle()>, <function str.istitle()>)}

        These attributes all reflect the same difference: if obj1 is 'abc'
        and obj2 is 'def', then
        'abc' != 'def' and
        'ABC' != 'DEF' abd
        'Abc' != 'Def'.

        When method=False, we ignore all of these, such that
        differences('a', 'b') returns {}. Therefore, it is important to
        carefully consider what differences you care about identifying.

    **kwargs: bool
        Can pass args to hdir to include magics or internals.

    Returns
    --------
    dict[str, tuple]: Maps attribute name to a tuple of values, where the
        first is the corresponding value for obj1 and the second is the
        corresponding value for obj2.
    """
    if obj1 == obj2:
        return {}

    assert type(obj1) == type(obj2), 'Objects must be the same type.'
    attr1, attr2 = hdir(obj1, **kwargs), hdir(obj2, **kwargs)
    assert attr1.keys() == attr2.keys(), 'Objects must have same attributes.'

    diffs = {}
    for (k1, v1), (k2, v2) in zip(attr1.items(), attr2.items()):
        # Only compare non-callable attributes.
        if not (methods or v1 == 'attribute'):
            continue

        # Comparisons work differently for numpy arrays.
        val1, val2 = getattr(obj1, k1), getattr(obj2, k2)
        try:
            equal = (val1 == val2).all()
        except AttributeError:
            equal = val1 == val2

        # Store values that are different for obj1 and obj2.
        if not equal:
            diffs[k1] = (val1, val2)

    return diffs


def catch(func, *args, verbose=False):
    """Error handling for list comprehensions. In practice, it's recommended
    to use the higher-level robust_comp() function which uses catch() under the
    hood.

    Parameters
    -----------
    func: function
    *args: any type
        Arguments to be passed to func.
    verbose: bool
        If True, print the error message should one occur.

    Returns
    --------
    any type: If the function executes successfully, its output is returned.
        Otherwise, return None.

    Examples
    ---------
    [catch(lambda x: 1 / x, i) for i in range(3)]
    >>> [None, 1.0, 0.5]

    # Note that the filtering method shown below also removes zeros which is
    # okay in this case.
    list(filter(None, [catch(lambda x: 1 / x, i) for i in range(3)]))
    >>> [1.0, 0.5]
    """
    try:
        return func(*args)
    except Exception as e:
        if verbose: print(e)
        return


def robust_comp(func, gen):
    """List comprehension with error handling. Note that values of None will be
    removed from the resulting list.

    Parameters
    ----------
    func: function
        Function to apply to each 
    gen: generator
        The sequence to iterate over. This could also be a list, set, etc.

    Returns
    -------
    list

    Examples
    --------
    # Notice that 
    >>> robust_comp(lambda x: x/(x-2), range(4))
    [-0.0, -1.0, 3.0]
    """
    return list(
        filter(lambda x: x is not None, (catch(func, obj) for obj in gen))
    )


def flatten(nested):
    """Flatten a nested sequence where the sub-items can be sequences or 
    primitives. This differs slightly from itertools chain methods because
    those require all sub-items to be sequences. This also returns a list 
    rather than a generator.

    Parameters
    ----------
    nested: sequence (list, tuple, set)
        Sequence where some or all of the items are also sequences.

    Returns
    -------
    list: Flattened version of `nested`.
    """
    def _walk(nested):
        for group in nested:
            try:
                yield from group
            except TypeError:
                yield group
    return list(_walk(nested))


SENTINEL = object()

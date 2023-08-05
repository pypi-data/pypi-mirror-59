"""

Python bindings for HFST finite-state transducer library written in C++.

FUNCTIONS:

    compile_lexc_file
    compile_lexc_files
    compile_lexc_script
    compile_pmatch_expression
    compile_pmatch_file
    compile_xfst_file
    compile_xfst_script
    concatenate
    disjunct
    empty_fst
    epsilon_fst
    fsa
    fst
    fst_type_to_string
    get_default_fst_type
    intersect
    is_diacritic
    read_att_input
    read_att_string
    read_att_transducer
    read_prolog_transducer
    regex
    set_default_fst_type
    start_xfst
    tokenized_fst

CLASSES:

    AttReader
    HfstIterableTransducer
    HfstTransition
    HfstInputStream
    HfstOutputStream
    HfstTokenizer
    HfstTransducer
    ImplementationType
    LexcCompiler
    PmatchContainer
    PrologReader
    XfstCompiler
    XreCompiler

"""

__version__ = "3.15.0.1"

import hfst_dev.exceptions
import hfst_dev.sfst_rules
import hfst_dev.xerox_rules
from libhfst_dev import is_diacritic, compile_pmatch_expression, HfstTransducer, HfstOutputStream, HfstInputStream, \
HfstTokenizer, HfstIterableTransducer, HfstTransition, XreCompiler, LexcCompiler, \
XfstCompiler, set_default_fst_type, get_default_fst_type, fst_type_to_string, PmatchContainer, Location
import libhfst_dev

from sys import version
if int(version[0]) > 2:
    def unicode(s, c):
        return s

EPSILON='@_EPSILON_SYMBOL_@'
UNKNOWN='@_UNKNOWN_SYMBOL_@'
IDENTITY='@_IDENTITY_SYMBOL_@'

def start_xfst(**kwargs):
    """
    Start interactive xfst compiler.

    Parameters
    ----------
    * `kwargs` :
        Arguments recognized are: type, quit_on_fail.
    * `quit_on_fail` :
        Whether the compiler exits on any error, defaults to False.
    * `type` :
        Implementation type of the compiler, defaults to
        hfst_dev.get_default_fst_type().
    """
    type = get_default_fst_type()
    quit_on_fail = 'OFF'
    for k,v in kwargs.items():
      if k == 'type':
        type = v
      elif k == 'quit_on_fail':
        if v == True:
          quit_on_fail='ON'
      else:
        print('Warning: ignoring unknown argument %s.' % (k))

    comp = XfstCompiler(type)
    comp.setReadInteractiveTextFromStdin(True) # ?
    comp.setReadline(False) # do not mix python and c++ readline
    comp.set('quit-on-fail', quit_on_fail)

    rl_length_1 = 0
    rl_found = False
    try:
      import readline
      rl_found = True
      rl_length_1 = readline.get_current_history_length()
    except ImportError:
      pass

    expression=""
    while True:
        expression += input(comp.get_prompt()).rstrip().lstrip()
        if len(expression) == 0:
           continue
        if expression[-1] == '\\':
           expression = expression[:-2] + '\n'
           continue
        retval = -1
        if True:
            if (expression == "apply down" or expression == "apply up" or expression == "inspect" or expression == "inspect net"):
               stdout.write('interactive command \'' + expression + '\' not supported\n')
               retval = 0
            # Viewing must be handled in python
            elif (expression == "view" or expression == "view net"):
               tr = comp.top(True) # silent mode
               if tr == None:
                  stdout.write('Empty stack.\n')
                  if comp.get("quit-on-fail") == "ON":
                     return
               else:
                  from IPython.core.display import display, SVG
                  display(SVG(tr.view()._repr_svg_()))
               retval = 0
            else:
               retval = comp.parse_line(expression);
        # at the moment, interactive commands are not supported
        else:
            # interactive command
            if (expression == "apply down" or expression == "apply up"):
               rl_length_2=0
               if rl_found:
                  rl_length_2 = readline.get_current_history_length()
               while True:
                  try:
                     line = input().rstrip().lstrip()
                  except EOFError:
                     break
                  if expression == "apply down":
                     comp.apply_down(line)
                  elif expression == "apply up":
                     comp.apply_up(line)
               if rl_found:
                  for foo in range(readline.get_current_history_length() - rl_length_2):
                     readline.remove_history_item(rl_length_2)
               retval = 0
            elif expression == "inspect" or expression == "inspect net":
               print('inspect net not supported')
               retval = 0
            else:
               retval = comp.parse_line(expression + "\n")
        if retval != 0:
           stdout.write("expression '%s' could not be parsed\n" % expression)
           if comp.get("quit-on-fail") == "ON":
              return
        if comp.quit_requested():
           break
        expression = ""

    if rl_found:
      for foo in range(readline.get_current_history_length() - rl_length_1):
         readline.remove_history_item(rl_length_1)

from sys import stdout

def regex(re, **kwargs):
    """
    Get a transducer as defined by regular expression *re*.

    Parameters
    ----------
    * `re` :
        The regular expression defined with Xerox transducer notation.
    * `kwargs` :
        Arguments recognized are: 'output' and 'definitions'.
    * `output` :
        Where warnings and errors are printed. Possible values are sys.stderr
        (the default), a StringIO or None, indicating a quiet mode.
    * `definitions` :
        A dictionary mapping variable names into transducers.


    Regular expression operators:

    ~   complement
    \   term complement
    &   intersection
    -   minus

    $.  contains once
    $?  contains optionally
    $   contains once or more
    ( ) optionality

    +   Kleene plus
    *   Kleene star

    ./. ignore internally (not yet implemented)
    /   ignoring

    |   union

    <>  shuffle
    <   before
    >   after

    .o.   composition
    .O.   lenient composition
    .m>.  merge right
    .<m.  merge left
    .x.   cross product
    .P.   input priority union
    .p.   output priority union
    .-u.  input minus
    .-l.  output minus
    `[ ]  substitute

    ^n,k  catenate from n to k times, inclusive
    ^>n   catenate more than n times
    ^>n   catenate less than n times
    ^n    catenate n times

    .r   reverse
    .i   invert
    .u   input side
    .l   output side

    \\\\\\  left quotient

    Two-level rules:

     \<=   left restriction
     <=>   left and right arrow
     <=    left arrow
     =>    right arrow

    Replace rules:

     ->    replace right
     (->)  optionally replace right
     <-    replace left
     (<-)  optionally replace left
     <->   replace left and right
     (<->) optionally replace left and right
     @->   left-to-right longest match
     @>    left-to-right shortest match
     ->@   right-to-left longest match
     >@    right-to-left shortest match

    Rule contexts, markers and separators:

     ||   match contexts on input sides
     //   match left context on output side and right context on input side
     \\   match left context on input side and right context on output side
     \/   match contexts on output sides
     _    center marker
     ...  markup marker
     ,,   rule separator in parallel rules
     ,    context separator
     [. .]  match epsilons only once

    Read from file:

     @bin" "  read binary transducer
     @txt" "  read transducer in att text format
     @stxt" " read spaced text
     @pl" "   read transducer in prolog text format
     @re" "   read regular expression

    Symbols:

     .#.  word boundary symbol in replacements, restrictions
     0    the epsilon
     ?    any token
     %    escape character
     { }  concatenate symbols
     " "  quote symbol

    :    pair separator
    ::   weight

    ;   end of expression
    !   starts a comment until end of line
    #   starts a comment until end of line    
    """
    type_ = get_default_fst_type()
    defs=None
    import sys
    output=sys.stderr

    for k,v in kwargs.items():
      if k == 'output':
          output=v;
      elif k == 'definitions':
          defs=v;
      else:
        print('Warning: ignoring unknown argument %s.' % (k))

    comp = XreCompiler(type_)
    if not defs == None:
        for k,v in defs.items():
            vtype = str(type(v))
            if "HfstTransducer" in vtype:
                comp.define_transducer(k,v)
                # print('defining transducer')
            else:
                pass

    comp.set_verbosity((output != None))
    if 'StringIO' in str(type(output)):
        retval = comp.compile_iostream(re)
        output.write(retval[1])
        return retval[0]
    else:
        return comp.compile(re)

def _replace_symbols(symbol, epsilonstr=EPSILON):
    if symbol == epsilonstr:
       return EPSILON
    if symbol == "@0@":
       return EPSILON
    symbol = symbol.replace("@_SPACE_@", " ")
    symbol = symbol.replace("@_TAB_@", "\t")
    symbol = symbol.replace("@_COLON_@", ":")
    return symbol

def _parse_att_line(line, fsm, epsilonstr=EPSILON):
    # get rid of extra whitespace
    line = line.replace('\t',' ')
    line = " ".join(line.split())
    fields = line.split(' ')
    try:
        if len(fields) == 1:
           if fields[0] == '': # empty transducer...
               return True
           fsm.add_state(int(fields[0]))
           fsm.set_final_weight(int(fields[0]), 0)
        elif len(fields) == 2:
           fsm.add_state(int(fields[0]))
           fsm.set_final_weight(int(fields[0]), float(fields[1]))
        elif len(fields) == 4:
           fsm.add_transition(int(fields[0]), int(fields[1]), _replace_symbols(fields[2]), _replace_symbols(fields[3]), 0)
        elif len(fields) == 5:
           fsm.add_transition(int(fields[0]), int(fields[1]), _replace_symbols(fields[2]), _replace_symbols(fields[3]), float(fields[4]))
        else:
           return False
    except ValueError as e:
        return False
    return True

def read_att_string(att):
    """
    Create a transducer as defined in AT&T format in *att*.
    """
    linecount = 0
    fsm = HfstIterableTransducer()
    lines = att.split('\n')
    for line in lines:
        linecount = linecount + 1
        if not _parse_att_line(line, fsm):
           raise hfst_dev.exceptions.NotValidAttFormatException(line, "", linecount)
    return HfstTransducer(fsm, get_default_fst_type())

def read_att_input():
    """
    Create a transducer as defined in AT&T format in user input.
    An empty line signals the end of input.
    """
    linecount = 0
    fsm = HfstIterableTransducer()
    while True:
        line = input().rstrip()
        if line == "":
           break
        linecount = linecount + 1
        if not _parse_att_line(line, fsm):
           raise hfst_dev.exceptions.NotValidAttFormatException(line, "", linecount)
    return HfstTransducer(fsm, get_default_fst_type())

def read_att_transducer(f, epsilonstr=EPSILON, linecount=[0]):
    """
    Create a transducer as defined in AT&T format in file *f*. *epsilonstr*
    defines how epsilons are represented. *linecount* keeps track of the current
    line in the file.
    """
    linecount_ = 0
    fsm = HfstIterableTransducer()
    while True:
        line = f.readline()
        if line == "":
           if linecount_ == 0:
              raise hfst_dev.exceptions.EndOfStreamException("","",0)
           else:
              linecount_ = linecount_ + 1
              break
        linecount_ = linecount_ + 1
        if line[0] == '-':
           break
        if not _parse_att_line(line, fsm, epsilonstr):
           raise hfst_dev.exceptions.NotValidAttFormatException(line, "", linecount[0] + linecount_)
    linecount[0] = linecount[0] + linecount_
    return HfstTransducer(fsm, get_default_fst_type())

class AttReader:
      """
      A class for reading input in AT&T text format and converting it into
      transducer(s).

      An example that reads AT&T input from file 'testfile.att' where epsilon is
      represented as \"<eps>\" and creates the corresponding transducers and prints
      them. If the input cannot be parsed, a message showing the invalid line in AT&T
      input is printed and reading is stopped.

      with open('testfile.att', 'r') as f:
           try:
                r = hfst_dev.AttReader(f, \"<eps>\")
                for tr in r:
                    print(tr)
           except hfst_dev.exceptions.NotValidAttFormatException as e:
                print(e.what())
      """
      def __init__(self, f, epsilonstr=EPSILON):
          """
          Create an AttReader that reads input from file *f* where the epsilon is
          represented as *epsilonstr*.

          Parameters
          ----------
          * `f` :
              A python file.
          * `epsilonstr` :
              How epsilon is represented in the file. By default, \"@_EPSILON_SYMBOL_@\"
              and \"@0@\" are both recognized.
          """
          self.file = f
          self.epsilonstr = epsilonstr
          self.linecount = [0]

      def read(self):
          """
          Read next transducer.

          Read next transducer description in AT&T format and return a corresponding
          transducer.

          Exceptions
          ----------
          * `hfst_dev.exceptions.NotValidAttFormatException` :
          * `hfst_dev.exceptions.EndOfStreamException` :
          """
          return read_att_transducer(self.file, self.epsilonstr, self.linecount)

      def __iter__(self):
          """
          An iterator to the reader.

          Needed for 'for ... in' statement.

          for transducer in att_reader:
              print(transducer)
          """
          return self

      def next(self):
          """
          Return next element (for python version 3).

          Needed for 'for ... in' statement.

          for transducer in att_reader:
              print(transducer)

          Exceptions
          ----------
          * `StopIteration` :
          """
          try:
             return self.read()
          except hfst_dev.exceptions.EndOfStreamException as e:
             raise StopIteration

      def __next__(self):
          """
          Return next element (for python version 2).

          Needed for 'for ... in' statement.

          for transducer in att_reader:
              print(transducer)

          Exceptions
          ----------
          * `StopIteration` :
          """
          return self.next()

def read_prolog_transducer(f, linecount=[0]):
    """
    Create a transducer as defined in prolog format in file *f*. *linecount*
    keeps track of the current line in the file.
    """
    linecount_ = 0
    fsm = HfstIterableTransducer()
    
    line = ""
    while(True):
        line = f.readline()
        linecount_ = linecount_ + 1
        if line == "":
            raise hfst_dev.exceptions.EndOfStreamException("","",linecount[0] + linecount_)
        line = line.rstrip()
        if line == "":
            pass # allow extra prolog separator(s)
        if line[0] == '#':
            pass # comment line
        else:
            break

    if not libhfst_dev.parse_prolog_network_line(line, fsm):
        raise hfst_dev.exceptions.NotValidPrologFormatException(line,"",linecount[0] + linecount_)

    while(True):
        line = f.readline()
        if (line == ""):
            retval = HfstTransducer(fsm, get_default_fst_type())
            retval.set_name(fsm.name)
            linecount[0] = linecount[0] + linecount_
            return retval
        line = line.rstrip()
        linecount_ = linecount_ + 1
        if line == "":  # prolog separator
            retval = HfstTransducer(fsm, get_default_fst_type())
            retval.set_name(fsm.name)
            linecount[0] = linecount[0] + linecount_
            return retval
        if libhfst_dev.parse_prolog_arc_line(line, fsm):
            pass
        elif libhfst_dev.parse_prolog_final_line(line, fsm):
            pass
        elif libhfst_dev.parse_prolog_symbol_line(line, fsm):
            pass
        else:
            raise hfst_dev.exceptions.NotValidPrologFormatException(line,"",linecount[0] + linecount_)

class PrologReader:
      """
      A class for reading input in prolog text format and converting it into
      transducer(s).

      An example that reads prolog input from file 'testfile.prolog' and creates the
      corresponding transducers and prints them. If the input cannot be parsed, a
      message showing the invalid line in prolog input is printed and reading is
      stopped.

          with open('testfile.prolog', 'r') as f:
              try:
                 r = hfst_dev.PrologReader(f)
                 for tr in r:
                     print(tr)
              except hfst_dev.exceptions.NotValidPrologFormatException as e:
                  print(e.what())
      """
      def __init__(self, f):
          """
          Create a PrologReader that reads input from file *f*.

          Parameters
          ----------
          * `f` :
              A python file.
          """
          self.file = f
          self.linecount = [0]

      def read(self):
          """

          Read next transducer.

          Read next transducer description in prolog format and return a corresponding
          transducer.

          Exceptions
          ----------
          * `hfst_dev.exceptions.NotValidPrologFormatException` :
          * `hfst_dev.exceptions.EndOfStreamException` :
          """
          return read_prolog_transducer(self.file, self.linecount)

      def __iter__(self):
          """
          An iterator to the reader.

          Needed for 'for ... in' statement.

          for transducer in prolog_reader:
              print(transducer)
          """
          return self

      def next(self):
          """
          Return next element (for python version 2).

          Needed for 'for ... in' statement.

          for transducer in prolog_reader:
              print(transducer)

          Exceptions
          ----------
          * `StopIteration` :
          """
          try:
             return self.read()
          except hfst_dev.exceptions.EndOfStreamException as e:
             raise StopIteration

      def __next__(self):
          """
          Return next element (for python version 2).

          Needed for 'for ... in' statement.

          for transducer in prolog_reader:
              print(transducer)

          Exceptions
          ----------
          * `StopIteration` :
          """
          return self.next()

def compile_xfst_file(filename, **kwargs):
    """
    Compile (run) xfst.

    Parameters
    ----------
    * `filename` :
        The name of the xfst file.
    * `kwargs` :
        Arguments recognized are: verbosity, quit_on_fail, output, type.
    * `verbosity` :
        The verbosity of the compiler, defaults to 0 (silent). Possible values are:
        0, 1, 2.
    * `quit_on_fail` :
        Whether the script is exited on any error, defaults to True.
    * `output` :
        Where output is printed. Possible values are sys.stdout, sys.stderr, a
        StringIO, sys.stdout being the default.
    * `type` :
        Implementation type of the compiler, defaults to
        hfst_dev.get_default_fst_type().

    Returns
    -------
    On success 0, else an integer greater than 0.
    """
    return _compile_xfst(filename=filename, **kwargs)

def compile_xfst_script(script, **kwargs):
    """
    Compile (run) xfst.

    Parameters
    ----------
    * `script` :
        The xfst script to be compiled (a string).
    * `kwargs` :
        Arguments recognized are: verbosity, quit_on_fail, output, type.
    * `verbosity` :
        The verbosity of the compiler, defaults to 0 (silent). Possible values are:
        0, 1, 2.
    * `quit_on_fail` :
        Whether the script is exited on any error, defaults to True.
    * `output` :
        Where output is printed. Possible values are sys.stdout, sys.stderr, a
        StringIO, sys.stdout being the default.
    * `type` :
        Implementation type of the compiler, defaults to
        hfst_dev.get_default_fst_type().

    Returns
    -------
    On success 0, else an integer greater than 0.
    """
    return _compile_xfst(script=script, **kwargs)

def _compile_xfst(**kwargs):
    """
    Compile (run) xfst.

    Parameters
    ----------
    * `kwargs` :
        Arguments recognized are: filename, data, verbosity, quit_on_fail, output, type.
    * `filename` :
        The name of the xfst file.
    * `script` :
        The xfst script to be compiled (a string).
    * `verbosity` :
        The verbosity of the compiler, defaults to 0 (silent). Possible values are:
        0, 1, 2.
    * `quit_on_fail` :
        Whether the script is exited on any error, defaults to True.
    * `output` :
        Where output is printed. Possible values are sys.stdout, sys.stderr, a
        StringIO, sys.stdout being the default.
    * `type` :
        Implementation type of the compiler, defaults to
        hfst_dev.get_default_fst_type().

    Returns
    -------
    On success 0, else an integer greater than 0.
    """
    if int(version[0]) > 2:
      pass
    else:
      raise RuntimeError('hfst_dev.compile_xfst_file not supported for python version 2')
    verbosity=0
    quit_on_fail='ON'
    type = get_default_fst_type()
    import sys
    output=sys.stdout
    filename=None
    script=None

    for k,v in kwargs.items():
      if k == 'verbosity':
        verbosity=v
      elif k == 'quit_on_fail':
        if v == False:
          quit_on_fail='OFF'
      elif k == 'output':
          output=v
      elif k == 'filename':
          filename=v
      elif k == 'script':
          script=v
      else:
        print('Warning: ignoring unknown argument %s.' % (k))

    if verbosity > 1:
      output.write('Compiling with %s implementation...' % fst_type_to_string(type))
    xfstcomp = XfstCompiler(type)
    xfstcomp.setVerbosity(verbosity > 0)
    xfstcomp.setInspectNetSupported(False)
    xfstcomp.set('quit-on-fail', quit_on_fail)
    if filename == None:
      data = script
    else:
      if verbosity > 1:
        output.write('Opening xfst file %s...' % filename)
      f = open(filename, 'r', encoding='utf-8')
      data = f.read()
      f.close()
      if verbosity > 1:
        output.write('File closed...')

    retval = xfstcomp.parse_line(data);
    #retval=-1
    #retval = libhfst_dev.hfst_compile_xfst_to_string_one(xfstcomp, data)
    #output.write(unicode(libhfst_dev.get_hfst_xfst_string_one(), 'utf-8'))

    if verbosity > 1:
      output.write('Parsed file with return value %i (0 indicating succesful parsing).' % retval)
    return retval

def compile_twolc_file(filename, **kwargs):
    """
    Compile twolc file *filename* and return the result.

    Parameters
    ----------
    * `filename` :
        The name of the twolc input file.
    * `kwargs` :
        Arguments recognized are: silent, verbose, resolve_right_conflicts, resolve_left_conflicts, type.
    * `silent` :
        Whether compilation is performed in silent mode, defaults to False.
    * `verbose` :
        Whether compilation is performed in verbose mode, defaults to False.
    * `resolve_right_conflicts` :
        Whether right arrow conflicts are resolved, defaults to True.
    * `resolve_left_conflicts` :
        Whether left arrow conflicts are resolved, defaults to False.
    * `type` :
        Implementation type of the compiler, defaults to hfst_dev.get_default_fst_type().

    Returns
    -------
    The compiled rules.
    """
    return _compile_twolc(filename=filename, **kwargs)

def compile_twolc_script(script, **kwargs):
    """
    Compile twolc script *script* and return the result.

    Parameters
    ----------
    * `script` :
        The twolc script.
    * `kwargs` :
        Arguments recognized are: silent, verbose, resolve_right_conflicts, resolve_left_conflicts, type.
    * `silent` :
        Whether compilation is performed in silent mode, defaults to False.
    * `verbose` :
        Whether compilation is performed in verbose mode, defaults to False.
    * `resolve_right_conflicts` :
        Whether right arrow conflicts are resolved, defaults to True.
    * `resolve_left_conflicts` :
        Whether left arrow conflicts are resolved, defaults to False.
    * `type` :
        Implementation type of the compiler, defaults to hfst_dev.get_default_fst_type().

    Returns
    -------
    A tuple containing the compiled rules.
    """
    return _compile_twolc(script=script, **kwargs)

def _compile_twolc(**kwargs):
    """
    Compile twolc script *script* and return the result.

    Parameters
    ----------
    * `kwargs` :
        Arguments recognized are: script, inputfilename, silent, verbose, resolve_right_conflicts, resolve_left_conflicts, type.
    * `script` :
        The twolc script.
    * `filename` :
        The name of the twolc input file.
    * `silent` :
        Whether compilation is performed in silent mode, defaults to False.
    * `verbose` :
        Whether compilation is performed in verbose mode, defaults to False.
    * `resolve_right_conflicts` :
        Whether right arrow conflicts are resolved, defaults to True.
    * `resolve_left_conflicts` :
        Whether left arrow conflicts are resolved, defaults to False.
    * `type` :
        Implementation type of the compiler, defaults to hfst_dev.get_default_fst_type().

    Returns
    -------
    A tuple containing the compiled rules.
    """
    script=None
    filename=None
    silent=False
    verbose=False
    resolve_right_conflicts=True
    resolve_left_conflicts=False
    implementation_type=get_default_fst_type()

    for k,v in kwargs.items():
        if k == 'script':
            script = v
        elif k == 'filename':
            filename = v
        elif k == 'type':
            implementation_type = v
        elif k == 'silent':
            silent=v
        elif k == 'verbose':
            verbose=v
        elif k == 'resolve_right_conflicts':
            resolve_right_conflicts=v
        elif k == 'resolve_left_conflicts':
            resolve_left_conflicts=v
        else:
            print('Warning: ignoring unknown argument %s.' % (k))

    if filename == None:
        retval = libhfst_dev.TwolcCompiler.compile_script_and_get_storable_rules(script, silent, verbose,
                                                    resolve_right_conflicts, resolve_left_conflicts,
                                                    implementation_type)
    else:
        retval = libhfst_dev.TwolcCompiler.compile_file_and_get_storable_rules(filename, silent, verbose,
                                                    resolve_right_conflicts, resolve_left_conflicts,
                                                    implementation_type)
    return retval

def compile_pmatch_file(filename):
    """
    Compile pmatch expressions as defined in *filename* and return a tuple of
    transducers.

    An example:

    If we have a file named streets.txt that contains:

    define CapWord UppercaseAlpha Alpha* ; define StreetWordFr [{avenue} |
    {boulevard} | {rue}] ; define DeFr [ [{de} | {du} | {des} | {de la}] Whitespace
    ] | [{d'} | {l'}] ; define StreetFr StreetWordFr (Whitespace DeFr) CapWord+ ;
    regex StreetFr EndTag(FrenchStreetName) ;

    we can run:

    defs = hfst_dev.compile_pmatch_file('streets.txt')
    const = hfst_dev.PmatchContainer(defs)
    assert cont.match("Je marche seul dans l'avenue desTernes.") ==
      "Je marche seul dans l'<FrenchStreetName>avenue des Ternes</FrenchStreetName>."
    """
    with open(filename, 'r') as myfile:
      data=myfile.read()
      myfile.close()
    defs = compile_pmatch_expression(data)
    return defs

def compile_sfst_file(filename, **kwargs):
    """
    Compile sfst file *filename* into a transducer.

    Parameters
    ----------
    * `filename` :
        The name of the sfst file.
    * `kwargs` :
        Arguments recognized are: verbose, output.
    * `verbose` :
        Whether sfst file is processed in verbose mode, defaults to False.
    * `output` :
        Where output is printed. Possible values are sys.stdout, sys.stderr, a
        StringI0, sys.stderr being the default. TODO

    Returns
    -------
    On success the resulting transducer, else None.
    """
    verbosity=False
    type = get_default_fst_type()
    output=None

    for k,v in kwargs.items():
      if k == 'verbose':
        verbosity=v
      elif k == 'output':
          output=v
      else:
        print('Warning: ignoring unknown argument %s.' % (k))

    retval=None
    import sys
    if output == None:
       retval = libhfst_dev.hfst_compile_sfst(filename, "", verbosity)
    elif output == sys.stdout:
       retval = libhfst_dev.hfst_compile_sfst(filename, "cout", verbosity)
    elif output == sys.stderr:
       retval = libhfst_dev.hfst_compile_sfst(filename, "cerr", verbosity)
    else:
       retval = libhfst_dev.hfst_compile_sfst(filename, "", verbosity)
       output.write(unicode(libhfst_dev.get_hfst_sfst_output(), 'utf-8'))

    return retval

def _compile_lexc(**kwargs):
    """
    Compile lexc into a transducer.

    Parameters
    ----------
    * `kwargs` :
        Arguments recognized are: filenames, script, verbosity, with_flags, output.
    * `filenames` :
        The names of the lexc files.
    * `script` :
        The lexc script to be compiled (a string).
    * `verbosity` :
        The verbosity of the compiler, defaults to 0 (silent). Possible values are:
        0, 1, 2.
    * `with_flags` :
        Whether lexc flags are used when compiling, defaults to False.
    * `output` :
        Where output is printed. Possible values are sys.stdout, sys.stderr, a
        StringIO, sys.stderr being the default.

    Returns
    -------
    On success the resulting transducer, else None.
    """
    verbosity=0
    withflags=False
    alignstrings=False
    type = get_default_fst_type()
    import sys
    output=sys.stderr
    filenames=None
    script=None

    for k,v in kwargs.items():
      if k == 'verbosity':
        verbosity=v
      elif k == 'with_flags':
        if v == True:
          withflags = v
      elif k == 'align_strings':
          alignstrings = v
      elif k == 'output':
          output=v
      elif k == 'filenames':
          filenames=v
      elif k == 'script':
          script=v

      else:
        print('Warning: ignoring unknown argument %s.' % (k))

    lexccomp = LexcCompiler(type, withflags, alignstrings)
    lexccomp.setVerbosity(verbosity)

    retval=-1
    if filenames == None:
        lexccomp.parse_line(script)
        retval = lexccomp.compileLexical()
        #retval = libhfst_dev.hfst_compile_lexc_script(lexccomp, script, "")
        #output.write(unicode(libhfst_dev.get_hfst_lexc_output(), 'utf-8'))
    else:
        for filename in filenames:
            lexccomp.parse(filename)
        retval = lexccomp.compileLexical()
        #retval = libhfst_dev.hfst_compile_lexc_files(lexccomp, filenames, "")
        #output.write(unicode(libhfst_dev.get_hfst_lexc_output(), 'utf-8'))

    return retval

def compile_lexc_file(filename, **kwargs):
    """
    Compile lexc file *filename* or into a transducer.

    Parameters
    ----------
    * `filename` :
        The name of the lexc file.
    * `kwargs` :
        Arguments recognized are: verbosity, with_flags, output.
    * `verbosity` :
        The verbosity of the compiler, defaults to 0 (silent). Possible values are:
        0, 1, 2.
    * `with_flags` :
        Whether lexc flags are used when compiling, defaults to False.
    * `output` :
        Where output is printed. Possible values are sys.stdout, sys.stderr, a
        StringIO, sys.stderr being the default.

    Returns
    -------
    On success the resulting transducer, else None.
    """
    return _compile_lexc(filenames=(filename,), **kwargs)

def compile_lexc_files(filenames, **kwargs):
    """
    Compile lexc files *filenames* or into a transducer.

    Parameters
    ----------
    * `filenames` :
        The list of lexc filenames.
    * `kwargs` :
        Arguments recognized are: verbosity, with_flags, output.
    * `verbosity` :
        The verbosity of the compiler, defaults to 0 (silent). Possible values are:
        0, 1, 2.
    * `with_flags` :
        Whether lexc flags are used when compiling, defaults to False.
    * `output` :
        Where output is printed. Possible values are sys.stdout, sys.stderr, a
        StringIO, sys.stderr being the default.

    Returns
    -------
    On success the resulting transducer, else None.
    """
    return _compile_lexc(filenames=filenames, **kwargs)

def compile_lexc_script(script, **kwargs):
    """
    Compile lexc script *script* into a transducer.

    Parameters
    ----------
    * `script` :
        The lexc script to be compiled (a string).
    * `kwargs` :
        Arguments recognized are: verbosity, with_flags, output.
    * `verbosity` :
        The verbosity of the compiler, defaults to 0 (silent). Possible values are:
        0, 1, 2.
    * `with_flags` :
        Whether lexc flags are used when compiling, defaults to False.
    * `output` :
        Where output is printed. Possible values are sys.stdout, sys.stderr, a
        StringIO, sys.stderr being the default.

    Returns
    -------
    On success the resulting transducer, else None.
    """
    return _compile_lexc(script=script, **kwargs)

def _is_weighted_word(arg):
    if isinstance(arg, tuple) and len(arg) == 2 and isinstance(arg[0], str) and isinstance(arg[1], (int, float)):
       return True
    return False

def _check_word(arg):
    if len(arg) == 0:
       raise RuntimeError('Empty word.')
    return arg

def fsa(arg):
    """
    Get a transducer (automaton in this case) that recognizes one or more paths.

    Parameters
    ----------
    * `arg` :
        See example below

    Possible inputs:

      One unweighted identity path:
        'foo'  ->  [f o o]

      Weighted path: a tuple of string and number, e.g.
        ('foo',1.4)
        ('bar',-3)
        ('baz',0)

      Several paths: a list or a tuple of paths and/or weighted paths, e.g.
        ['foo', 'bar']
        ('foo', ('bar',5.0))
        ('foo', ('bar',5.0), 'baz', 'Foo', ('Bar',2.4))
        [('foo',-1), ('bar',0), ('baz',3.5)]

    """
    deftok = HfstTokenizer()
    retval = HfstIterableTransducer()
    if isinstance(arg, str):
       if len(arg) == 0:
           retval.set_final_weight(0, 0) # epsilon transducer with zero weight
       else:
           retval.disjunct(deftok.tokenize(_check_word(arg)), 0)
    elif _is_weighted_word(arg):
       if len(arg) == 0:
           retval.set_final_weight(0, arg[1]) # epsilon transducer with weight
       else:
           retval.disjunct(deftok.tokenize(_check_word(arg[0])), arg[1])
    elif isinstance(arg, tuple) or isinstance(arg, list):
       for word in arg:
           if _is_weighted_word(word):
              if len(word) == 0:
                  retval.set_final_weight(0, word[1]) # epsilon transducer with weight
              else:
                  retval.disjunct(deftok.tokenize(_check_word(word[0])), word[1])
           elif isinstance(word, str):
              if len(word) == 0:
                  retval.set_final_weight(0, 0) # epsilon transducer with zero weight
              else:
                  retval.disjunct(deftok.tokenize(_check_word(word)), 0)
           else:
              raise RuntimeError('Tuple/list element not a string or tuple of string and weight.')
    else:
       raise RuntimeError('Not a string or tuple/list of strings.')
    return HfstTransducer(retval, get_default_fst_type())

def fst(arg):
    """
    Get a transducer that recognizes one or more paths.

    Parameters
    ----------
    * `arg` :
        See example below

    Possible inputs:

      One unweighted identity path:
        'foo'  ->  [f o o]

      Weighted path: a tuple of string and number, e.g.
        ('foo',1.4)
        ('bar',-3)
        ('baz',0)

      Several paths: a list or a tuple of paths and/or weighted paths, e.g.
        ['foo', 'bar']
        ('foo', ('bar',5.0))
        ('foo', ('bar',5.0), 'baz', 'Foo', ('Bar',2.4))
        [('foo',-1), ('bar',0), ('baz',3.5)]

      A dictionary mapping strings to any of the above cases:
        {'foo':'foo', 'bar':('foo',1.4), 'baz':(('foo',-1),'BAZ')}
    """
    if isinstance(arg, dict):
       retval = regex('[0-0]') # empty transducer
       for input, output in arg.items():
           if not isinstance(input, str):
              raise RuntimeError('Key not a string.')
           left = fsa(input)
           right = 0
           if isinstance(output, str):
              right = fsa(output)
           elif isinstance(output, list) or isinstance(output, tuple):
              right = fsa(output)
           else:
              raise RuntimeError('Value not a string or tuple/list of strings.')
           left.cross_product(right)
           retval.disjunct(left)
       return retval
    return fsa(arg)

def fst_to_fsa(fst, separator=''):
    """
    (Experimental)

    Encode a transducer into an automaton, i.e. create a transducer where each
    transition <in:out> of *fst* is replaced with a transition <inSout:inSout>
    where 'S' is *separator*, except if the transition symbol on both sides is
    hfst_dev.EPSILON, hfst_dev.IDENTITY or hfst_dev.UNKNOWN.

    All states and weights of transitions and end states are copied otherwise
    as such. The alphabet is copied, and new symbols which are created when
    encoding the transitions, are inserted to it.

    Parameters
    ----------
    * `fst` :
        The transducer.
    * `separator` :
        The separator symbol inserted between input and output symbols.

    Examples:

        import hfst
        foo2bar = hfst_dev.fst({'foo':'bar'})

    creates a transducer [f:b o:a o:r]. Calling

        foobar = hfst_dev.fst_to_fsa(foo2bar)
        
    will create the transducer [fb:fb oa:oa or:or] and

        foobar = hfst_dev.fst_to_fsa(foo2bar, '^')

    the transducer [f^b:f^b o^a:o^a o^r:o^r].

    """
    encoded_symbols = libhfst_dev.StringSet()
    retval = hfst_dev.HfstIterableTransducer(fst)
    for state in retval.states():
        arcs = retval.transitions(state)
        for arc in arcs:
            input = arc.get_input_symbol()
            output = arc.get_output_symbol()
            if (input == output) and ((input == hfst_dev.EPSILON) or (input == hfst_dev.UNKNOWN) or (input == hfst_dev.IDENTITY)):
                continue
            symbol = input + separator + output
            arc.set_input_symbol(symbol)
            arc.set_output_symbol(symbol)
            encoded_symbols.insert(symbol)
    retval.add_symbols_to_alphabet(encoded_symbols)
    if 'HfstTransducer' in str(type(fst)):
        return hfst_dev.HfstTransducer(retval)
    else:
        return retval

def fsa_to_fst(fsa, separator=''):
    """
    (Experimental)

    Decode an encoded automaton back into a transducer, i.e. create a 
    transducer where each transition <inSout:inSout> of *fsa*, where 'S' is
    the first *separator* found in the compound symbol 'inSout', is replaced
    with a transition <in:out>.

    If no *separator* is found in the symbol, transition is copied as such. All
    states and weights of transitions and end states are copied as such. The
    alphabet is copied, omitting encoded symbols which were decoded according
    to *separator*. Any new input and output symbols extracted from encoded
    symbols are added to the alphabet.

    If *separator* is the empty string, 'in' must either be single-character
    symbol or a special symbol of form '@...@'.

    Parameters
    ----------
    * `fsa` :
        The encoded transducer. Must be an automaton, i.e. for each
        transition, the input and output symbols must be the same. Else, a
        RuntimeError is thrown.
    * `separator` :
        The symbol separating input and output symbol parts in *fsa*. If it is
        the empty string, each encoded transition symbol is must be of form
        'x...' (single-character input symbol 'x') or '@...@...' (special
        symbol as input symbol). Else, a RuntimeError is thrown.

    Examples:

        import hfst
        foo2bar = hfst_dev.fst({'foo':'bar'})  # creates transducer [f:b o:a o:r]
        foobar = hfst_dev.fst_to_fsa(foo2bar, '^')

    creates the transducer [f^b:f^b o^a:o^a o^r:o^r]. Then calling

        foo2bar = hfst_dev.fsa_to_fst(foobar, '^')

    will create again the original transducer [f:b o:a o:r].
    """
    retval = hfst_dev.HfstIterableTransducer(fsa)
    encoded_symbols = libhfst_dev.StringSet()
    for state in retval.states():
        arcs = retval.transitions(state)
        for arc in arcs:
            input = arc.get_input_symbol()
            output = arc.get_output_symbol()
            symbols = []
            if not (input == output):
                raise RuntimeError('Transition input and output symbols differ.')
            if input == "":
                raise RuntimeError('Transition symbol cannot be the empty string.')
            # separator given:
            if len(separator) > 0:
                symbols = input.split(separator, 1)                
            # no separator given:
            else:
                index = input.find('@')
                if not index == 0:
                    symbols.append(input[0])
                    if not input[1] == '':
                        symbols.append(input[1:])
                else:
                    index = input.find('@', 1)
                    if index == -1:
                        raise RuntimeError('Transition symbol cannot have only one "@" sign.')
                    symbols.append(input[0:index+1])
                    if not input[index+1] == '':
                        symbols.append(input[index+1:])
            arc.set_input_symbol(symbols[0])
            arc.set_output_symbol(symbols[-1])
            # encoded symbol to be removed from alphabet of result
            if len(symbols) > 1:
                encoded_symbols.insert(input)
    retval.remove_symbols_from_alphabet(encoded_symbols)
    if 'HfstTransducer' in str(type(fsa)):
        return hfst_dev.HfstTransducer(retval)
    else:
        return retval

def tokenized_fst(arg, weight=0):
    """
    Get a transducer that recognizes the concatenation of symbols or symbol pairs in
    *arg*.

    Parameters
    ----------
    * `arg` :
        The symbols or symbol pairs that form the path to be recognized.

    Example

       import hfst
       tok = hfst_dev.HfstTokenizer()
       tok.add_multichar_symbol('foo')
       tok.add_multichar_symbol('bar')
       tr = hfst_dev.tokenized_fst(tok.tokenize('foobar', 'foobaz'))

    will create the transducer [foo:foo bar:b 0:a 0:z].
    """
    retval = HfstIterableTransducer()
    state = 0
    if isinstance(arg, list) or isinstance(arg, tuple):
       for token in arg:
           if isinstance(token, str):
              new_state = retval.add_state()
              retval.add_transition(state, new_state, token, token, 0)
              state = new_state
           elif isinstance(token, list) or isinstance(token, tuple):
              if len(token) == 2:
                 new_state = retval.add_state()
                 retval.add_transition(state, new_state, token[0], token[1], 0)
                 state = new_state
              elif len(token) == 1:
                 new_state = retval.add_state()
                 retval.add_transition(state, new_state, token, token, 0)
                 state = new_state
              else:
                 raise RuntimeError('Symbol or symbol pair must be given.')
       retval.set_final_weight(state, weight)
       return HfstTransducer(retval, get_default_fst_type())
    else:
       raise RuntimeError('Argument must be a list or a tuple')

def empty_fst():
    """
    Get an empty transducer.

    Empty transducer has one state that is not final, i.e. it does not recognize any
    string.
    """
    return regex('[0-0]')

def epsilon_fst(weight=0):
    """
    Get an epsilon transducer.

    Parameters
    ----------
    * `weight` :
        The weight of the final state. Epsilon transducer has one state that is
        final (with final weight *weight*), i.e. it recognizes the empty string.
    """
    return regex('[0]::' + str(weight))

def concatenate(transducers):
    """
    Return a concatenation of *transducers*.
    """
    retval = epsilon_fst()
    for tr in transducers:
      retval.concatenate(tr)
    retval.minimize()
    return retval

def disjunct(transducers):
    """
    Return a disjunction of *transducers*.
    """
    retval = empty_fst()
    for tr in transducers:
      retval.disjunct(tr)
    retval.minimize()
    return retval

def intersect(transducers):
    """
    Return an intersection of *transducers*.
    """
    retval = None
    for tr in transducers:
      if retval == None:
        retval = HfstTransducer(tr)
      else:
        retval.intersect(tr)
    retval.minimize()
    return retval

def subtract(transducers):
    """
    Return a subtraction of *transducers*.
    """
    retval = None
    for tr in transducers:
      if retval == None:
        retval = HfstTransducer(tr)
      else:
        retval.subtract(tr)
    retval.minimize()
    return retval

def compose(transducers):
    """
    Return a composition of *transducers*.
    """
    retval = None
    for tr in transducers:
        if retval == None:
            retval = HfstTransducer(tr)
        else:
            retval.compose(tr)
    retval.minimize()
    return retval

def cross_product(transducers):
    """
    Return a cross product of *transducers*.
    """
    retval = None
    for tr in transducers:
        if retval == None:
            retval = HfstTransducer(tr)
        else:
            retval.cross_product(tr)
    retval.minimize()
    return retval



class ImplementationType:
    """
    Back-end implementation.

    Attributes:

        SFST_TYPE:               SFST type, unweighted
        TROPICAL_OPENFST_TYPE:   OpenFst type with tropical weights
        LOG_OPENFST_TYPE:        OpenFst type with logarithmic weights (limited support)
        FOMA_TYPE:               FOMA type, unweighted
        XFSM_TYPE:               XFST type, unweighted (limited support)
        HFST_OL_TYPE:            HFST optimized-lookup type, unweighted
        HFST_OLW_TYPE:           HFST optimized-lookup type, weighted
        HFST2_TYPE:              HFST version 2 legacy type
        UNSPECIFIED_TYPE:        type not specified
        ERROR_TYPE:              (something went wrong)

    """
    SFST_TYPE = libhfst_dev.SFST_TYPE
    TROPICAL_OPENFST_TYPE = libhfst_dev.TROPICAL_OPENFST_TYPE
    LOG_OPENFST_TYPE = libhfst_dev.LOG_OPENFST_TYPE
    FOMA_TYPE = libhfst_dev.FOMA_TYPE
    XFSM_TYPE = libhfst_dev.XFSM_TYPE
    HFST_OL_TYPE = libhfst_dev.HFST_OL_TYPE
    HFST_OLW_TYPE = libhfst_dev.HFST_OLW_TYPE
    HFST2_TYPE = libhfst_dev.HFST2_TYPE
    UNSPECIFIED_TYPE = libhfst_dev.UNSPECIFIED_TYPE
    ERROR_TYPE = libhfst_dev.ERROR_TYPE


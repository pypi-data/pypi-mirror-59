"""
A collection of functions for modifying source code that is embeded into the Sphinx documentation.
"""

import sys
import os
import re
import tokenize
import importlib
import inspect
import sqlite3
import subprocess
import tempfile

import numpy as np

from six import StringIO, PY3
from six.moves import cStringIO as cStringIO

from redbaron import RedBaron

sqlite_file = 'feature_docs_unit_test_db.sqlite'    # name of the sqlite database file
table_name = 'feature_unit_tests'   # name of the table to be queried


def remove_docstrings(source):
    """
    Return 'source' minus docstrings.

    Parameters
    ----------
    source : str
        Original source code.

    Returns
    -------
    str
        Source with docstrings removed.
    """
    io_obj = StringIO(source)
    out = ""
    prev_toktype = tokenize.INDENT
    last_lineno = -1
    last_col = 0
    for tok in tokenize.generate_tokens(io_obj.readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]
        # ltext = tok[4] # in original code but not used here
        # The following two conditionals preserve indentation.
        # This is necessary because we're not using tokenize.untokenize()
        # (because it spits out code with copious amounts of oddly-placed
        # whitespace).
        if start_line > last_lineno:
            last_col = 0
        if start_col > last_col:
            out += (" " * (start_col - last_col))
        # This series of conditionals removes docstrings:
        if token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                # This is likely a docstring; double-check we're not inside an operator:
                if prev_toktype != tokenize.NEWLINE:
                    # Note regarding NEWLINE vs NL: The tokenize module
                    # differentiates between newlines that start a new statement
                    # and newlines inside of operators such as parens, brackes,
                    # and curly braces.  Newlines inside of operators are
                    # NEWLINE and newlines that start new code are NL.
                    # Catch whole-module docstrings:
                    if start_col > 0:
                        # Unlabelled indentation means we're inside an operator
                        out += token_string
                    # Note regarding the INDENT token: The tokenize module does
                    # not label indentation inside of an operator (parens,
                    # brackets, and curly braces) as actual indentation.
                    # For example:
                    # def foo():
                    #     "The spaces before this docstring are tokenize.INDENT"
                    #     test = [
                    #         "The spaces before this string do not get a token"
                    #     ]
        else:
            out += token_string
        prev_toktype = token_type
        last_col = end_col
        last_lineno = end_line
    return out


def remove_redbaron_node(node, index):
    """
    Utility function for removing a node using RedBaron.

    RedBaron has some problems with modifying code lines that run across
    multiple lines. ( It is mentioned somewhere online but cannot seem to
    find it now. )

    RedBaron throws an Exception but when you check, it seems like it does
    what you asked it to do. So, for now, we ignore the Exception.
    """

    try:
        node.value.remove(node.value[index])
    except Exception as e:  # no choice but to catch the general Exception
        if str(e).startswith('It appears that you have indentation in your CommaList'):
            pass
        else:
            raise


def replace_asserts_with_prints(source_code):
    """
    Replace asserts with print statements.

    Using RedBaron, replace some assert calls with print statements that print the actual
    value given in the asserts.

    Depending on the calls, the actual value can be the first or second
    argument.
    """

    rb = RedBaron(source_code)  # convert to RedBaron internal structure

    for assert_type in ['assertAlmostEqual', 'assertLess', 'assertGreater', 'assertEqual',
                        'assertEqualArrays', 'assertTrue', 'assertFalse']:
        assert_nodes = rb.findAll("NameNode", value=assert_type)
        for assert_node in assert_nodes:
            assert_node = assert_node.parent
            remove_redbaron_node(assert_node, 0)  # remove 'self' from the call
            assert_node.value[0].replace('print')
            if assert_type not in ['assertTrue', 'assertFalse']:
                remove_redbaron_node(assert_node.value[1], 1)  # remove the expected value argument

    assert_nodes = rb.findAll("NameNode", value='assert_rel_error')
    for assert_node in assert_nodes:
        assert_node = assert_node.parent
        # If relative error tolerance is specified, there are 4 arguments
        if len(assert_node.value[1]) == 4:
            remove_redbaron_node(assert_node.value[1], -1)  # remove the relative error tolerance
        remove_redbaron_node(assert_node.value[1], -1)  # remove the expected value
        remove_redbaron_node(assert_node.value[1], 0)  # remove the first argument which is
        #                                                  the TestCase
        assert_node.value[0].replace("print")

    assert_nodes = rb.findAll("NameNode", value='assert_almost_equal')
    for assert_node in assert_nodes:
        assert_node = assert_node.parent
        # If relative error tolerance is specified, there are 3 arguments
        if len(assert_node.value[1]) == 3:
            remove_redbaron_node(assert_node.value[1], -1)  # remove the relative error tolerance
        remove_redbaron_node(assert_node.value[1], -1)  # remove the expected value
        assert_node.value[0].replace("print")

    source_code_with_prints = rb.dumps()  # get back the string representation of the code
    return source_code_with_prints


def get_method_body(method_code):
    '''Using the RedBaron module, get the body of a method.

    Do not want the definition signature line
    '''

    method_code = '\n' + method_code  # For some reason RedBaron has problems with this if
    #                                                     if it does not start with an empty line
    rb = RedBaron(method_code)
    def_node = rb.findAll("DefNode")[0]  # Look for the 'def' node. Should only be one!
    def_node.value.decrease_indentation(8)  # so that the code is all the way to the left
    return def_node.value.dumps()


def remove_initial_empty_lines_from_source(source):
    """
    Some initial empty lines were added to keep RedBaron happy.
    Need to strip these out before we pass the source code to the
    directive for including source code into feature doc files.
    """

    idx = re.search(r'\S', source, re.MULTILINE).start()
    return source[idx:]


def get_source_code_of_class_or_method(class_or_method_path, remove_docstring=True):
    """
    Return source code as a text string.

    Parameters
    ----------
    class_or_method_path : str
        Package path to the class or function.
    remove_docstring : bool
        Set to False to keep docstrings in the text.
    """

    # First, assume module path since we want to support loading a full module as well.
    try:
        module = importlib.import_module(class_or_method_path)
        source = inspect.getsource(module)

    except ImportError:

        # Second, assume class and see if it works
        try:
            module_path = '.'.join(class_or_method_path.split('.')[:-1])
            module_with_class = importlib.import_module(module_path)
            class_name = class_or_method_path.split('.')[-1]
            cls = getattr(module_with_class, class_name)
            source = inspect.getsource(cls)

        except ImportError:

            # else assume it is a path to a method
            module_path = '.'.join(class_or_method_path.split('.')[:-2])
            module_with_method = importlib.import_module(module_path)
            class_name = class_or_method_path.split('.')[-2]
            method_name = class_or_method_path.split('.')[-1]
            cls = getattr(module_with_method, class_name)
            meth = getattr(cls, method_name)
            source = inspect.getsource(meth)

    # Remove docstring from source code
    if remove_docstring:
        source = remove_docstrings(source)

    return source


sqlite_file = 'feature_docs_unit_test_db.sqlite'    # name of the sqlite database file
table_name = 'feature_unit_tests'   # name of the table to be queried


def get_test_source_code_for_feature(feature_name):
    '''The function to be called from the custom Sphinx directive code
    that includes relevant unit test code(s).

    It gets the test source from the unit tests that have been
    marked to indicate that they are associated with the "feature_name"'''

    # get the:
    #
    #   1. title of the test
    #   2. test source code
    #   3. output of running the test
    #
    # from from the database that was created during an earlier
    # phase of the doc build process using the
    # devtools/create_feature_docs_unit_test_db.py script

    conn = sqlite3.connect(sqlite_file)
    cur = conn.cursor()
    cur.execute('SELECT title, unit_test_source, run_outputs FROM {tn} WHERE feature="{fn}"'.
                format(tn=table_name, fn=feature_name))
    all_rows = cur.fetchall()
    conn.close()

    test_source_code_for_feature = []

    # Loop through all the unit tests that are relevant to this feature name
    for title, unit_test_source, run_outputs in all_rows:
        # add to the list that will be returned
        test_source_code_for_feature.append((title, unit_test_source, run_outputs))

    return test_source_code_for_feature


def remove_raise_skip_tests(source):
    """
    Remove from the code any raise unittest.SkipTest lines since we don't want those in
    what the user sees.
    """
    rb = RedBaron(source)
    raise_nodes = rb.findAll("RaiseNode")
    for rn in raise_nodes:
        # only the raise for SkipTest
        if rn.value[:2].dumps() == 'unittestSkipTest':
            rn.parent.value.remove(rn)
    return rb.dumps()


def remove_leading_trailing_whitespace_lines(src):
    """
    Remove any trailing whitespace lines.

    Parameters
    ----------
    src : str
        Input code.

    Returns
    -------
    str
        Code with trailing whitespace lines removed.
    """
    lines = src.splitlines()

    non_whitespace_lines = []
    for i, l in enumerate( lines ):
        if l and not l.isspace():
            non_whitespace_lines.append(i)
    imin = min(non_whitespace_lines)
    imax = max(non_whitespace_lines)

    return '\n'.join(lines[imin: imax+1])

def split_source_into_input_blocks(src):
    """
    Split source into blocks; the splits occur at prints.

    Parameters
    ----------
    src : str
        Input code.

    Returns
    -------
    list
        List of input code sections.
    """
    rb = RedBaron(src)
    in_code_blocks = []
    in_code_block = []
    # group code until the first print, then repeat
    for r in rb:
        line = r.dumps()
        if not line.endswith('\n'):
            line += '\n'
        in_code_block.append(line)
        if r.type == 'print' or \
            ( len(r.value) == 3 and \
            (r.type, r.value[0].type, r.value[1].type, r.value[2].type) == \
                ('atomtrailers', 'name', 'name', 'call') and \
                r.value[1].value in ['run_model', 'run_driver', 'setup'] ):
            # stop and make an input code block
            in_code_block = ''.join(in_code_block)
            in_code_block = remove_leading_trailing_whitespace_lines(in_code_block)
            in_code_blocks.append(in_code_block)
            in_code_block = []

    if in_code_block: # If anything left over
        in_code_blocks.append(''.join(in_code_block))

    return in_code_blocks


def insert_output_start_stop_indicators(src):
    """
    Insert identifier strings so that output can be segregated from input.

    Parameters
    ----------
    src : str
        String containing input and output lines.

    Returns
    -------
    str
        String with output demarked.
    """
    rb = RedBaron(src)

    src_with_out_start_stop_indicators = []
    input_block_number = 0
    for r in rb:
        line = r.dumps()
        # not sure why some lines from RedBaron do not have newlines
        if not line.endswith('\n'):
            line += '\n'
        if r.type == 'print':
            # src_with_out_start_stop_indicators += 'print("<<<<<{}")'.format(input_block_number) + '\n'
            src_with_out_start_stop_indicators.append(line)
            src_with_out_start_stop_indicators.append('print(">>>>>{}")\n'.format(input_block_number))
        elif len(r.value) == 3 and \
            (r.type, r.value[0].type, r.value[1].type, r.value[2].type) == \
                ('atomtrailers', 'name', 'name', 'call') and \
                r.value[1].value in ['run_model', 'run_driver', 'setup']:
            src_with_out_start_stop_indicators.append(line)
            src_with_out_start_stop_indicators.append('print(">>>>>{}")\n'.format(input_block_number))
        else:
            src_with_out_start_stop_indicators.append(line)
        input_block_number += 1
    return ''.join(src_with_out_start_stop_indicators)


def clean_up_empty_output_blocks(input_blocks, output_blocks):
    """Some of the blocks do not generate output. We only want to have
    input blocks that have outputs.
    """

    new_input_blocks = []
    new_output_blocks = []
    current_in_block = ''
    for in_block, out_block in zip(input_blocks, output_blocks):
        if current_in_block and not current_in_block.endswith('\n'):
            current_in_block += '\n'
        current_in_block += in_block
        if out_block:
            new_input_blocks.append(current_in_block)
            new_output_blocks.append(out_block)
            current_in_block = ''

    # if there was no output, return the one input block and empty output block
    if current_in_block:
        new_input_blocks.append(current_in_block)
        new_output_blocks.append('')

    return new_input_blocks, new_output_blocks


def extract_output_blocks(run_output):
    """
    Identify and extract outputs from source.

    Parameters
    ----------
    run_output : str
        Source code with outputs.

    Returns
    -------
    list of str
        List containing output text blocks.
    """

    output_blocks = []
    # Look for start and end lines that look like this:
    #  <<<<<4
    #  >>>>>4
    output_block = []
    for line in run_output.splitlines():
        if line.startswith('>>>>>'):
            output_blocks.append('\n'.join(output_block))
            output_block = []
        else:
            output_block.append(line)

    if output_block:
        output_blocks.append('\n'.join(output_block))
    return output_blocks


def globals_for_imports(src):
    """
    Generate text that creates a global for each imported class, method, or module.

    It appears that sphinx royally screws up something in python, so that when exec-ing
    code with imports, they aren't always available inside of classes or methods. This
    can be solved by issuing a global for each class, method, or module.

    Parameters
    ----------
    src : str
        Source code to be tested.

    Returns
    -------
    str
        New code string with global statements
    """
    # HACK: A test had problems loading this specific user-defined class under exec+sphinx, so
    # hacking it in.
    new_txt = ['from __future__ import print_function',
               'global Sub',
               'global ImplSimple']

    continuation = False
    for line in src.split('\n'):
        if continuation or 'import ' in line:

            if continuation:
                tail = line
            elif ' as ' in line:
                tail = line.split(' as ')[1]
            else:
                tail = line.split('import ')[1]

            if ', \\' in tail:
                continuation = True
                tail = tail.replace(', \\', '')
            else:
                continuation = False

            modules = tail.split(',')
            for module in modules:
                new_txt.append('global %s' % module.strip())

    return '\n'.join(new_txt)


def get_test_src(method_path):
    """
    Return desired source code for a single feature after testing it.

    Used by embed_test.

    1. Get the source code for a unit test method
    2. Replace the asserts with prints -> source_minus_docstrings_with_prints_cleaned
    3. Split source_minus_docstrings_with_prints_cleaned up into groups of "In" blocks -> input_blocks
    4. Insert extra print statements into source_minus_docstrings_with_prints_cleaned
            to indicate start and end of print Out blocks -> source_with_output_start_stop_indicators
    5. Run the test using source_with_out_start_stop_indicators -> run_outputs
    6. Extract from run_outputs, the Out blocks -> output_blocks
    7. Return source_minus_docstrings_with_prints_cleaned, input_blocks, output_blocks, skipped, failed

    Parameters
    ----------
    method_path : str
        Module hiearchy path to the test.

    Returns
    -------
    str
        Cleaned source code, ready for inclusion in doc.
    str
        Reason that the test failed or was skipped.
    list of str
        List of input code blocks
    list of str
        List of Python output blocks
    bool
        True if test was skipped
    bool
        True if test failed
    """

    #----------------------------------------------------------
    # 1. Get the source code for a unit test method.
    #----------------------------------------------------------

    module_path = '.'.join(method_path.split('.')[:-2])
    class_name = method_path.split('.')[-2]
    method_name = method_path.split('.')[-1]

    test_module = importlib.import_module(module_path)
    cls = getattr(test_module, class_name)
    try:
        import mpi4py
    except ImportError:
        use_mpi = False
    else:
        N_PROCS = getattr(cls, 'N_PROCS', 1)
        use_mpi =  N_PROCS > 1
    meth = getattr(cls, method_name)
    class_source_code = inspect.getsource(cls)

    # Directly manipulating function text to strip header and remove leading whitespace.
    # Should be faster than redbaron
    method_source_code = inspect.getsource(meth)
    meth_lines = method_source_code.split('\n')
    counter = 0
    past_header = False
    new_lines = []
    for line in meth_lines:
        if not past_header:
            n1 = len(line)
            newline = line.lstrip()
            n2 = len(newline)
            tab = n1-n2
            if counter == 0:
                first_len = tab
            elif n1 == 0:
                continue
            if tab == first_len:
                counter += 1
                newline = line[tab:]
            else:
                past_header = True
        else:
            newline = line[tab:]
        # exclude 'global' directives, not needed the way we are running things
        if not newline.startswith("global "):
            new_lines.append(newline)

    method_source = '\n'.join(new_lines[counter:])

    # Remove docstring from source code
    source_minus_docstrings = remove_docstrings(method_source)

    #-----------------------------------------------------------------------------------
    # 2. Replace the asserts with prints -> source_minus_docstrings_with_prints_cleaned
    #-----------------------------------------------------------------------------------

    # Replace some of the asserts with prints of the actual values
    # This calls RedBaron
    source_minus_docstrings_with_prints = replace_asserts_with_prints(source_minus_docstrings)

    # remove raise SkipTest lines
    # We decided to leave them in for now
    # source_minus_docstrings_with_prints = remove_raise_skip_tests(source_minus_docstrings_with_prints)

    # Remove the initial empty lines
    source_minus_docstrings_with_prints_cleaned = remove_initial_empty_lines_from_source(
        source_minus_docstrings_with_prints)

    #-----------------------------------------------------------------------------------
    # 4. Insert extra print statements into source_minus_docstrings_with_prints_cleaned
    #        to indicate start and end of print Out blocks -> source_with_output_start_stop_indicators
    #-----------------------------------------------------------------------------------
    source_with_output_start_stop_indicators = insert_output_start_stop_indicators( source_minus_docstrings_with_prints_cleaned )

    #-----------------------------------------------------------------------------------
    # 5. Run the test using source_with_out_start_stop_indicators -> run_outputs
    #-----------------------------------------------------------------------------------

    # Get all the pieces of code needed to run the unit test method
    global_imports = globals_for_imports(method_source)
    teardown_source_code = get_method_body(inspect.getsource(getattr(cls, 'tearDown')))

    code_to_run = '\n'.join([global_imports,
                             source_with_output_start_stop_indicators,
                             teardown_source_code])

    skipped = False
    failed = False
    try:

        # Use Subprocess if we are under MPI.
        if use_mpi:

            # Write it to a file so we can run it.
            fd, code_to_run_path = tempfile.mkstemp()

            with os.fdopen(fd, 'w') as tmp:
                tmp.write(code_to_run)
                tmp.close()
            env = os.environ.copy()
            env['USE_PROC_FILES'] = '1'
            p = subprocess.Popen(['mpirun', '-n', str(N_PROCS), 'python', code_to_run_path],
                                 env=env)
            p.wait()
            multi_out_blocks = []
            for i in range(N_PROCS):
                with open('%d.out' % i) as f:
                    multi_out_blocks.append(extract_output_blocks(f.read()))
                os.remove('%d.out' % i)
            output_blocks = []
            for i in range(len(multi_out_blocks[0])):
                output_blocks.append('\n'.join(["(rank %d) %s" % (j, m[i]) for j, m in enumerate(multi_out_blocks) if m[i]]))

        # Just Exec the code for serial tests.
        else:

            stdout = sys.stdout
            stderr = sys.stderr
            strout = cStringIO()
            sys.stdout = strout
            sys.stderr = strout
            #
            # # Hacking, but trying to make sure we capture the check config messages.
            # from openmdao.utils.logger_utils import _loggers, get_logger
            # if 'check_config' not in _loggers:
            #     get_logger('check_config', use_format=True)
            # if 'check_partials' not in _loggers:
            #     get_logger('check_partials')
            # if 'check_totals' not in _loggers:
            #     get_logger('check_totals')
            #
            # _loggers['check_config']['logger'].handlers[0].stream = strout
            # _loggers['check_partials']['logger'].handlers[0].stream = strout
            # _loggers['check_totals']['logger'].handlers[0].stream = strout

            # We need more precision from numpy
            save_opts = np.get_printoptions()
            np.set_printoptions(precision=8)

            exec(code_to_run, {})
            np.set_printoptions(precision=save_opts['precision'])
            run_outputs = strout.getvalue()

    except subprocess.CalledProcessError as e:
        # Get a traceback.
        if 'raise unittest.SkipTest' in e.output.decode('utf-8'):
            reason_for_skip = e.output.splitlines()[-1][len('unittest.case.SkipTest: '):]
            run_outputs = reason_for_skip
            skipped = True
        else:
            run_outputs = "Running of embedded test {} in docs failed due to: \n\n{}".format(method_path, e.output.decode('utf-8'))
            failed = True

    except Exception as err:
        if 'SkipTest' in code_to_run:
            txt1 = code_to_run.split('SkipTest(')[1]
            run_outputs = txt1.split(')')[0]
            skipped = True
        else:
            msg = "Running of embedded test {} in docs failed due to: \n\n{}"
            run_outputs = msg.format(method_path, str(err))
            failed = True

    finally:
        if use_mpi:
            os.remove(code_to_run_path)
        else:
            sys.stdout = stdout
            sys.stderr = stderr

    if PY3 and not use_mpi and not isinstance(run_outputs, str):
        run_outputs = "".join(map(chr, run_outputs))  # in Python 3, run_outputs is of type bytes!

    if not skipped and not failed:
        #####################
        ### 3. Split source_minus_docstrings_with_prints_cleaned up into groups of "In" blocks -> input_blocks ###
        #####################
        input_blocks = split_source_into_input_blocks(source_minus_docstrings_with_prints_cleaned)

        #####################
        ### 6. Extract from run_outputs, the Out blocks -> output_blocks ###
        #####################
        if not use_mpi:
            output_blocks = extract_output_blocks(run_outputs)

        # Need to deal with the cases when there is no outputblock for a given input block
        # Merge an input block with the previous block and throw away the output block
        input_blocks, output_blocks = clean_up_empty_output_blocks(input_blocks, output_blocks)
        skipped_failed_output = None
    else:
        input_blocks = output_blocks = None
        skipped_failed_output = run_outputs

    return source_minus_docstrings_with_prints_cleaned, skipped_failed_output, input_blocks, output_blocks, skipped, failed

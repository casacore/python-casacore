# substitute.py: substitute python variables and expressions
# Copyright (C) 1998,1999,2008
# Associated Universities, Inc. Washington DC, USA.
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 675 Massachusetts Ave, Cambridge, MA 02139, USA.
#
# Correspondence concerning AIPS++ should be addressed as follows:
#        Internet email: aips2-request@nrao.edu.
#        Postal address: AIPS++ Project Office
#                        National Radio Astronomy Observatory
#                        520 Edgemont Road
#                        Charlottesville, VA 22903-2475 USA

from six import string_types
import numpy as np

__all__ = ['getlocals', 'getvariable', 'substitute']


def getlocals(back=2):
    """Get the local variables some levels back (-1 is top)."""
    import inspect
    fr = inspect.currentframe()
    try:
        while fr and back != 0:
            fr1 = fr
            fr = fr.f_back
            back -= 1
    except:
        pass
    return fr1.f_locals


def getvariable(name):
    """Get the value of a local variable somewhere in the call stack."""
    import inspect
    fr = inspect.currentframe()
    try:
        while fr:
            fr = fr.f_back
            vars = fr.f_locals
            if name in vars:
                return vars[name]
    except:
        pass
    return None


def substitute(s, objlist=(), globals={}, locals={}):
    """Substitute global python variables in a command string.

    This function parses a string and tries to substitute parts like
    `$name` by their value. It is uses by :mod:`image` and :mod:`table`
    to handle image and table objects in a command, but also other
    variables (integers, strings, etc.) can be substituted.
    The following rules apply:

    1. A name must start with an underscore or alphabetic, followed
       by zero or more alphanumerics and underscores.
    2. String parts enclosed in single or double quotes are literals and
       are left untouched.
       Furthermore a $ can be escaped by a backslash, which is useful
       if an environment variable is used. Note that an extra backslash
       is required in Python to escape the backslash.
       The output contains the quotes and backslashes.
    3. A variable is looked up in the given local and global namespaces.
    4. If the variable `name` has a vector value, its substitution is
       enclosed in square brackets and separated by commas.
    5. A string value is enclosed in double quotes. If the value
       contains a double quote, that quote is enclosed in single quotes.
    6. If the name's value has a type mentioned in the argument `objlist`,
       it is substituted by `$n` (where n is a sequence number) and its
       value is added to the objects of that type in `objlist`.
    7. If the name is unknown or has an unknown type, it is left untouched.

    The `objlist` argument is a list of tuples or lists where each tuple
    or list has three fields:

    1. The first field is the object type (e.g. `table`)
    2. The second field is a prefix for the sequence number (usually empty).
       E.g. regions could have prefix 'r' resulting in a substitution like
       `$r1`.
    3. The third field is a list of objects to be substituted. New objects
       get appended to it. Usually the list is initially empty.

    Apart from substituting variables, it also substitutes `$(expression)`
    by the expression result.
    It correctly handles parentheses and quotes in the expression.
    For example::

        >>> a = 2
        >>> b = 3
        >>> substitute('$(a+b)+$a')
        '5+2'

        >>> substitute('$(a+b+a)')
        '7'

        >>> substitute('$((a+b)+$a)')
        '$((a+b)+$a)'

        >>> substitute('$((a+b)*(a+b))')
        '25'

        >>> substitute('$(len("ab cd( de"))')
        '9'

    Substitution is NOT recursive. E.g. if a=1 and b="$a",
    the result of substitute("$b") is "$a" and not 1.

    """
    # Get the local variables at the caller level if not given.
    if not locals:
        locals = getlocals(3)
    # Initialize some variables.
    backslash = False
    dollar = False
    nparen = 0
    name = ''
    evalstr = ''
    squote = False
    dquote = False
    out = ''
    # Loop through the entire string.
    for tmp in s:
        if backslash:
            out += tmp
            backslash = False
            continue
        # If a dollar is found, we might have a name or expression.
        # Alphabetics and underscore are always part of name.
        if dollar and nparen == 0:
            if tmp == '_' or ('a' <= tmp <= 'z') or ('A' <= tmp <= 'Z'):
                name += tmp
                continue
            # Numerics are only part if not first character.
            if '0' <= tmp <= '9' and name != '':
                name += tmp
                continue
            # $( indicates the start of an expression to evaluate.
            if tmp == '(' and name == '':
                nparen = 1
                evalstr = ''
                continue
            # End of name found. Try to substitute.
            out += substitutename(name, objlist, globals, locals)
            dollar = False

        # Handle possible single or double quotes.
        if tmp == '"' and not squote:
            dquote = not dquote
        elif tmp == "'" and not dquote:
            squote = not squote
        if not dquote and not squote:
            # Count the number of balanced parentheses
            # (outside quoted strings) in the subexpression.
            if nparen > 0:
                if tmp == '(':
                    nparen += 1
                elif tmp == ')':
                    nparen -= 1
                    if nparen == 0:
                        # The last closing parenthese is found.
                        # Evaluate the subexpression.
                        # Add the result to the output.
                        out += substituteexpr(evalstr, globals, locals)
                        dollar = False
                evalstr += tmp
                continue
            # Set a switch if we have a dollar (outside quoted
            # and eval strings).
            if tmp == '$':
                dollar = True
                name = ''
                continue
        # No special character; add it to output or evalstr.
        # Set a switch if we have a backslash.
        if nparen == 0:
            out += tmp
        else:
            evalstr += tmp
        if tmp == '\\':
            backslash = True

        # The entire string has been handled.
        # Substitute a possible last name.
        # Insert a possible incomplete eval string as such.
    if dollar:
        out += substitutename(name, objlist, globals, locals)
    else:
        if nparen > 0:
            out += '$(' + evalstr
    return out


# This function tries to substitute the given name using
# the rules described in the description of function substitute.
def substitutename(name, objlist, globals, locals):
    # If the name is empty, return a single dollar.
    if len(name) == 0:
        return '$'

    # First try as a single variable; otherwise as an expression.
    try:
        v = getvariable(name)
        if v is None:
            v = eval(name, globals, locals)
    except NameError:
        return '$' + name

    # See if the resulting value is one of the given special types.
    try:
        for objtype, objstr, objs in objlist:
            if isinstance(v, objtype):
                objs += [v]
                return '$' + objstr + str(len(objs))
    except:
        pass

    # No specific type, thus a normal value has to be substituted.
    return substitutevar(v)


# This function tries to substitute the given name using
# the rules described in the description of function substitute.
def substituteexpr(expr, globals={}, locals={}):
    try:
        res = eval(expr, globals, locals)
        v = substitutevar(res)
    except:
        # If the expr is undefined, return the original.
        v = '$(' + expr + ')'
    return str(v)


# Substitute a value.
def substitutevar(v):
    out = ''
    if isinstance(v, tuple) or isinstance(v, list) or isinstance(v, np.ndarray):
        out = '['
        first = True
        for tmp in v:
            if first:
                first = False
            else:
                out += ','
            out += substituteonevar(tmp)
        out += ']'
    else:
        out = substituteonevar(v)
    return out


def substituteonevar(v):
    # A string needs to be enclosed in quotes.
    # A vector value is enclosed in square brackets and separated by commas.
    if isinstance(v, string_types):
        return substitutestring(v)
    # A numeric or boolean value is converted to a string.
    # A vector value is enclosed in square brackets and separated by commas.
    # Take care we have enough precision.
    if isinstance(v, bool):
        if v:
            return 'T'
        return 'F'
    return str(v)


# Enclose a string in double quotes.
# If the string contains double quotes, enclose them in single quotes.
# E.g.                         ab"cd
# is returned as     "ab"'"'"cd"
# which is according to the TaQL rules for strings.
def substitutestring(value):
    out = '"'
    for tmp in value:
        if tmp == '"':
            out += '"' + "'" + '"' + "'" + '"'
        else:
            out += tmp
    return out + '"'

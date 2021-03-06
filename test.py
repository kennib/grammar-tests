#!/usr/bin/python

import subprocess
import sys, os

class echo():
	def write(self, string):
		string = string.replace('"', '\\"')
		subprocess.call('echo -ne "%s"' % string, shell=True)

sys.stdout = echo()

calls = {
    1: 'diff -b <(%(script)s %(name)s.grammar) <(cat %(name)s.sets)',
    2: 'diff -b <(%(script)s %(name)s.grammar | sort) <(cat %(name)s.table | sort)',
    3: 'diff -b <(%(script)s %(name)s.grammar %(name)s.input) <(cat %(name)s.output)',
    4: 'diff -b <(%(script)s %(name)s.ebnf | sort) <(cat %(name)s.bnf | sort)',
}

grammar_tests = [
	'trivial',
	'static',
	'plain',
	'easy',
	'medium',
	'isLL1',
	'notLL1',
	'alsonotLL1',
	'binary',
	'recursive',
	'variable',
	'circular',
	'tricky',
]

grammar_tests += ['more/q'+str(x) for x in xrange(1, 16)]

ebnf_tests = [
	'trivial',
	'0or1',
	'0orMore',
	'or',
	'binary',
	'simple',
	'multiple',
	'inside',
	'variable',
	'recursive',
	'circular',
]

ebnf_tests += ['more/'+chr(x) for x in xrange(ord('a'), ord('o')+1)]

def blue(string):
	return "\e[1;34m"+string+"\e[0m"

def red(string):
	return "\e[1;31m"+string+"\e[0m"

def green(string):
	return "\e[1;32m"+string+"\e[0m"

width = max(map(len, calls.values())) + 3*max(map(len, grammar_tests+ebnf_tests))

for i in range(1, 5):
    print blue('Testing question %d...' % i)
    if i == 4:
        tests = ebnf_tests
    else:
        tests = grammar_tests

    script = './question%d.py' % i
    passed = 0
    for test in tests:
        call = calls[i] % {'script': script, 'name': 'tests/%s' % test}
        print ('  $ %s' % call).ljust(width+10),
        
        result = os.popen("bash -c '%s'" % call).read()
        
        if not result:
        	print green("passed")
        	passed += 1
        else:
        	print red("failed")
        	print red(result)
    print

    result = "  Passed %d of %d tests" % (passed, len(tests))
    if passed == len(tests):
        print green(result)
    else:
        print red(result)
    
    print

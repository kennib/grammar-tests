#!/usr/bin/python

import subprocess
import sys, os

class echo():
	def write(self, string):
		subprocess.call('echo -ne "%s"' % string, shell=True)

sys.stdout = echo()

calls = {
    1: 'diff <(%(script)s %(name)s.grammar) <(cat %(name)s.sets)',
    2: 'diff <(%(script)s %(name)s.grammar | sort) <(cat %(name)s.table | sort)',
    3: 'diff <(%(script)s %(name)s.grammar %(name)s.input | sort) <(cat %(name)s.output | sort)',
    4: 'diff <(%(script)s %(name)s.ebnf | sort) <(cat %(name)s.bnf | sort)',
}

grammar_tests = [
	'trivial',
	'easy',
	'isLL1',
	'notLL1',
	'circular',
	'tricky',
]

ebnf_tests = [
	'0or1',
	'0orMore',
	'or',
	'simple',
]

def blue(string):
	return "\e[1;34m"+string+"\e[0m"

def red(string):
	return "\e[1;31m"+string+"\e[0m"

def green(string):
	return "\e[1;32m"+string+"\e[0m"

for i in range(1, 5):
    print blue('Testing question %d...' % i)
    if i == 4:
        tests = ebnf_tests
    else:
        tests = grammar_tests

    script = './question%d.py' % i
    for test in tests:
        call = calls[i] % {'script': script, 'name': 'tests/%s' % test}
        print '  $ %s' % call
        
        result = os.popen("bash -c '%s'" % call).read()
        
        if not result:
        	print green("passed")
        else:
        	print red(result)

#!/usr/bin/python

from os import system
import subprocess

calls = {
    1: 'diff <(%(script)s %(name)s.grammar | sort) <(cat %(name)s.sets | sort)',
    2: 'diff <(%(script)s %(name)s.grammar | sort) <(cat %(name)s.table | sort)',
    3: '%(script)s %(name)s.grammar %(name)s.input | diff - %(name)s.output',
    4: 'diff <(%(script)s %(name)s.ebnf | sort) <(cat %(name)s.bnf | sort)',
}

grammar_tests = ['isLL1', 'circular', 'trivial', 'notLL1', 'tricky']
ebnf_tests = ['0or1', '0orMore', 'or', 'simple']

for i in range(1, 5):
    print 'Testing question %d...' % i
    if i == 4:
        tests = ebnf_tests
    else:
        tests = grammar_tests

    script = './question%d.py' % i
    for test in tests:
        call = calls[i] % {'script': script, 'name': 'tests/%s' % test}
        print '  $ %s' % call
        subprocess.call('bash -c "%s"' % call, shell=True)

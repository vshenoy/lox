import sys

hadError = False

def report(line, where, message):
    print(f'[line {line}] Error {where}: {message}',
          file=sys.stderr)

def error(line, message):
    global hadError
    report(line, '', message)
    hadError = True

import sys
import traceback

import lib.textutils as txtutils

def handle_error(dir: str, save = False, save_last = False) -> str:
    '''
    Custom error handler that prints only the last call
    and outputs the whole stack to a file.\n
    `dir`: path to the directory where error files should be\n
    Returns the filename on which the stack trace is.
    '''
    exc_type, exc_message, exc_traceback = sys.exc_info()

    if not dir.endswith(('/', '\\')):
        dir += '/'
    
    if save_last:
        latest_error_file = open(dir+'latest.error.log', 'w')
        traceback.print_exc(file=latest_error_file)
        txtutils.cprint(txtutils.blue, 'Full stack trace (last error only) in:')
        txtutils.cprint(txtutils.grey, '  '+latest_error_file.name)

    if save:
        error_file = open(dir+txtutils.get_date_text()+'.error.log', 'w')
        traceback.print_exc(file=error_file)
        txtutils.cprint(txtutils.blue, 'Full stack trace in:')
        txtutils.cprint(txtutils.grey, '  '+error_file.name)
    
        
    extracted_tracebacks = traceback.extract_tb(tb=exc_traceback)
    txtutils.cprint(txtutils.yellow, 'Traceback:')
    for extracted_traceback in extracted_tracebacks:
        txtutils.cprint(txtutils.grey, '  '+extracted_traceback.filename, end=':')
        txtutils.cprint(txtutils.grey, extracted_traceback.lineno)
        txtutils.cprint(txtutils.white,'    '+extracted_traceback.line)
    txtutils.cprint(txtutils.red, exc_type.__name__+': ', end='')
    txtutils.cprint(txtutils.red, exc_message)
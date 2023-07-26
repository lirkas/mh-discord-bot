import sys, os
import traceback
import logging as log

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
    dir += 'errors/'
    
    # create dir if it does not exist
    if not os.path.isdir(dir):
        os.makedirs(dir)

    filename_date = txtutils.get_date_text(
        date_format='{y}-{m}-{d}',
        time_format='',
        separator='')
    error_time = txtutils.get_date_text(
        date_format='[{d}-{m}-{y}]',
        time_format='[{h}:{m}:{s}]',
        separator='')
    
    if save_last:
        latest_error_file = open(dir+'latest.error.log', 'w')
        traceback.print_exc(file=latest_error_file)
        txtutils.cprint(txtutils.blue, 'Full stack trace (last error only) in:')
        txtutils.cprint(txtutils.grey, '  '+latest_error_file.name)

    if save:
        error_file = open(dir+filename_date+'.error.log', 'a')
        error_file.write('{:+<22}\n'.format(''))
        error_file.write(error_time+'\n')
        error_file.write('{:+<22}\n'.format(''))
        traceback.print_exc(file=error_file)
        error_file.write('\n')
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

def get_logger(name: str = None):
    '''
    Wrapper for logging.getLogger()
    '''
    logger = log.getLogger(name)
    logger.setLevel(level=log.INFO)
    logger.propagate = False

    for handler in logger.handlers:
        logger.removeHandler(handler)

    handler = log.StreamHandler()
    dt_fmt = '%d-%m][%H:%M:%S'
    time = txtutils.grey.text('[{asctime}]')
    name = txtutils.purple.text('[{name}]')
    formatter = log.Formatter(time+'[{levelname:>8}]'+name+' : {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger
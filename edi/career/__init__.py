import logging
logger = logging.getLogger('uvcsite.edi.career')

def log(message, summary='', severity=logging.DEBUG):
    logger.log(severity, '%s %s', summary, message)

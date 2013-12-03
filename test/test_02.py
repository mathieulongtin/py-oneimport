
from oneimport import *
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s [%(levelname)s] %(message)s')

logger.info('pwd=%s',os.getcwd())
logger.info('prefix=%s',sys.prefix)
logger.info('re.IGNORECASE=%d',re.IGNORECASE)
logger.info('today=%s',datetime.date.today())
logger.info('time=%f',time.time())

d = collections.defaultdict(int)
d['a'] += 10
logger.debug('defaultdict: %s', d)

logger.info("cwd = %s", os.getcwd())


import logging
import sys
import timeit, time

from lang.get_meta import get_meta_model
from main.Main import Main
import stats

def run():
    t = time.time()
    ml = int(t * 1000)
    file_log_name = f"{ml}_concord_log.txt"
    file_handler = logging.FileHandler(filename=file_log_name)
    file_handler.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[file_handler, stream_handler],
        format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    metamodel = get_meta_model()
    rep_config: Main = metamodel.model_from_file(sys.argv[1])
    rep_config.interpret()
    

run()
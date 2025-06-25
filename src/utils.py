"""Вспомогательные функции"""
import os
import re
import fnmatch
from config import logger

def count_files_by_pattern(directory, pattern='*'):
    """Эффективный подсчёт файлов для больших каталогов"""
    logger.debug("count_files_by_pattern() start")
    try:
        count = 0
        pattern_re = re.compile(fnmatch.translate(pattern))

        with os.scandir(directory) as it:
            for entry in it:
                if entry.is_file() and pattern_re.match(entry.name):
                    count += 1
        return count
    except OSError as e:
        logger.error("Ошибка подсчёта файлов: %s" ,str(e))
        return 0

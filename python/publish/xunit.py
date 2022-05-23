import os
import pathlib
from typing import Iterable, Tuple, Union

from lxml import etree

from publish.junit import JUnitTree

with (pathlib.Path(__file__).parent / 'xslt' / 'xunit-to-junit.xslt').open('r', encoding='utf-8') as r:
    transform_xunit_to_junit = etree.XSLT(etree.parse(r))


def parse_xunit_files(files: Iterable[str]) -> Iterable[Tuple[str, Union[JUnitTree, BaseException]]]:
    """Parses xunit files."""
    def parse(path: str) -> Union[JUnitTree, BaseException]:
        if not os.path.exists(path):
            return FileNotFoundError(f'File does not exist.')
        if os.stat(path).st_size == 0:
            return Exception(f'File is empty.')

        try:
            trx = etree.parse(path)
            return transform_xunit_to_junit(trx)
        except BaseException as e:
            return e

    return [(result_file, parse(result_file)) for result_file in files]

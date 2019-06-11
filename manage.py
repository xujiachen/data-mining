import argparse
from functools import partial

from data_mining.utils.logger import logging_config

logging_config = partial(logging_config, relative_path="..", stream_log=True)


def test():
    logging_config("./test.log")
    import unittest
    tests = unittest.TestLoader().discover("tests", pattern="test_*")
    unittest.TextTestRunner().run(tests)


def main():
    ''' Parse command line arguments and execute the code'''
    parser = argparse.ArgumentParser()
    # 测试
    parser.add_argument('--test', '-t', action="store_true")
    # parse args
    args = parser.parse_args()
    # logger = partial(logging_config, relative_path=args.relative_path, stream_log=args.stream_log)

    if args.test:
        test()


if __name__ == '__main__':
    main()

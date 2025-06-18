import argparse
from jgtpy.cli_utils import add_use_fresh_argument_relaxed


def test_relaxed_use_fresh_accepts_both_flags():
    parser = argparse.ArgumentParser()
    add_use_fresh_argument_relaxed(parser, load_from_settings=False)
    args = parser.parse_args(['--fresh', '--notfresh'])
    # jgtcommon post parse logic prioritises --fresh when both flags are set
    # Simulate that behaviour here
    from jgtutils.jgtcommon import __use_fresh__post_parse
    import jgtutils.jgtcommon as jc
    jc.args = args
    __use_fresh__post_parse()
    assert args.fresh is True

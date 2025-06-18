"""Utility helpers for CLI argument parsing."""
from jgtutils import jgtcommon


def add_use_fresh_argument_relaxed(parser, load_from_settings=True):
    """Add --fresh and --notfresh arguments without enforcing exclusivity.

    If both flags are supplied, argparse will set both values to True. The
    post-parse logic in :mod:`jgtutils.jgtcommon` resolves the final
    ``args.fresh`` value by giving priority to ``--fresh`` when both are set.
    This helper mirrors :func:`jgtutils.jgtcommon.add_use_fresh_argument` but
    omits the mutually exclusive restriction so that callers accidentally
    passing both options are still handled gracefully.
    """
    bars_group = jgtcommon._get_group_by_title(
        parser,
        jgtcommon.ARG_GROUP_BARS_TITLE,
        jgtcommon.ARG_GROUP_BARS_DESCRIPTION,
    )
    use_fresh_value = (
        jgtcommon.load_arg_default_from_settings(
            jgtcommon.FRESH_FLAG_ARGNAME,
            False,
            jgtcommon.FRESH_FLAG_ARGNAME_ALIAS,
        )
        if load_from_settings
        else False
    )
    bars_group.add_argument(
        '-' + jgtcommon.FRESH_FLAG_ARGNAME_ALIAS,
        '--' + jgtcommon.FRESH_FLAG_ARGNAME,
        action='store_true',
        help='Freshening the storage with latest market.',
        default=use_fresh_value,
    )
    bars_group.add_argument(
        '-' + jgtcommon.NOT_FRESH_FLAG_ARGNAME_ALIAS,
        '--' + jgtcommon.NOT_FRESH_FLAG_ARGNAME,
        action='store_true',
        help='Output/Input wont be freshed from storage (weekend or tests).',
        default=not use_fresh_value,
    )
    return parser

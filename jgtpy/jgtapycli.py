import warnings

# Ignore FutureWarning
warnings.simplefilter(action="ignore", category=FutureWarning)

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from JGTIDSRequest import JGTIDSRequest

from jgtutils.jgtconstants import (
    IDS_COLUMNS_TO_NORMALIZE
)

columns_to_normalize = IDS_COLUMNS_TO_NORMALIZE  # @a Migrate to jgtutils.jgtconstants

from jgtutils import (
    jgtcommon as jgtcommon,
)

from jgtapyhelper import createIDSService,print_quiet




# @STCGoal CLI

import argparse

def _parse_args():
    from jgtpyconstants import IDSCLI_PROG_DESCRIPTION, IDSCLI_PROG_NAME, IDSCLI_PROG_EPILOG
    parser=jgtcommon.new_parser(IDSCLI_PROG_DESCRIPTION,prog=IDSCLI_PROG_NAME,epilog=IDSCLI_PROG_EPILOG)
    # jgtfxcommon.add_main_arguments(parser)
    jgtcommon.add_instrument_timeframe_arguments(parser)
    # jgtcommon.add_date_arguments(parser)
    # jgtcommon.add_tlid_range_argument(parser)
    #add_bars_amount_V2_arguments
    jgtcommon.add_bars_amount_V2_arguments(parser)
    # jgtcommon.add_output_argument(parser)
    # jgtfxcommon.add_quiet_argument(parser)
    jgtcommon.add_verbose_argument(parser)

    jgtcommon.add_use_fresh_argument(parser)
    jgtcommon.add_keepbidask_argument(parser)
    jgtcommon.add_ids_mfi_argument(parser)
    jgtcommon.add_ids_gator_oscillator_argument(parser)
    jgtcommon.add_ids_balligator_argument(parser)
    jgtcommon.add_ids_talligator_argument(parser)
    jgtcommon.add_ids_fractal_largest_period_argument(parser)
    
    jgtcommon.add_dropna_volume_argument(parser)

    jgtcommon.add_viewpath_argument(parser)
    # parser.add_argument(
    #     "-go",
    #     "--gator_oscillator_flag",
    #     action="store_true",
    #     help="Enable the Gator Oscillator indicator.",
    # )
    # parser.add_argument(
    #     "-mfi",
    #     "--mfi_flag",
    #     action="store_true",
    #     help="Enable the Market Facilitation Index indicator.",
    # )

    parser.add_argument(
        "--bypass_index_reset",
        action="store_true",
        help="Bypass resetting the index.",
    )

    # parser.add_argument(
    #     "-ba",
    #     "--balligator_flag",
    #     action="store_true",
    #     help="Enable the Alligator indicator.",
    # )
    # parser.add_argument(
    #     "-bjaw",
    #     "--balligator_period_jaws",
    #     type=int,
    #     default=89,
    #     help="The period of the Alligator jaws.",
    # )
    # parser.add_argument(
    #     "-lfp",
    #     "--largest_fractal_period",
    #     type=int,
    #     default=89,
    #     help="The largest fractal period.",
    # )
    args = jgtcommon.parse_args(parser)
    return args


def main():


    rq = JGTIDSRequest()
    args = _parse_args()

    # There might be multiple for now
    instrument = args.instrument
    timeframe = args.timeframe

    verbose_level = args.verbose
    #viewpath=args.viewpath
    
    quiet = False
    if verbose_level == 0:
        quiet = True


    process_ids = True

    if process_ids:
        if not quiet:
            print("Processing IDS")
        output = True


    try:

        print_quiet(quiet, "Getting for : " + instrument + "_" + timeframe)
        instruments = instrument.split(",")
        timeframes = timeframe.split(",")

        for instrument in instruments:
            for timeframe in timeframes:
                rq = JGTIDSRequest.from_args(args)
                rq.instrument=instrument
                rq.timeframe=timeframe
                createIDSService(
                    rq=rq,
                    quiet=quiet,
                    verbose_level=verbose_level,
                )

    except Exception as e:
        jgtcommon.print_exception(e)




if __name__ == "__main__":
    main()

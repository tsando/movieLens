#!/usr/bin/env python # required to run programs from command line without the "python " prefix
#
# analyze_movies.py
#
# run as: ./analyze_movies.py (gender|agegroup) <number>

import argparse

##### Functions needed to check right format of arguments in command line
def valid_grouping(s):
    try:
        if s == 'agegroup' or s == 'gender':
            return s
        else:
            raise ValueError
    except ValueError:
        msg = "Not a valid grouping. Should be 'agegroup' or 'gender'."
        raise argparse.ArgumentTypeError(msg)

def valid_int(N):
    try:
        if int(N) > 0:
            return int(N)
        else:
            raise ValueError
    except ValueError:
        msg = "Not a valid number. Should be a positive number >0"
        raise argparse.ArgumentTypeError(msg)

##### Command-line arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('grouping', metavar='gender|agegroup', type=valid_grouping,
                   help="Grouping. Can be either 'gender' or 'agegroup' ")
parser.add_argument('N_movies', metavar='N', type=valid_int,
                   help='Top movies for selected grouping. Must be >0')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print args.grouping, args.N_movies
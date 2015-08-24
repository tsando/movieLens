#!/usr/bin/env python # required to run programs from command line without the "python " prefix
#
# analyze_movies.py
#
# run as: ./analyze_movies.py (gender|agegroup) <number>

import argparse

# Command-line arguments
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('grouping', metavar='gender|agegroup', type=str,
                   help='Grouping. Can be either gender or agegroup')
parser.add_argument('N_movies', metavar='N', type=int,
                   help='Top movies for selected grouping')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print args.N_movies, args.grouping, args.N


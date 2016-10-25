#!/usr/bin/env python
# python 2.7

import sys
import csv
import gzip 
import collections
# with gzip.open('/home/devsci5/depth13Genome.depth.gz') as gzfile:
    # for line in gzfile:

# for line in sys.stdin:
#     print line,
# input_file = "/home/devsci4/data/depth13Genome.depth.txt"
# input_file = sys.stdin
input_file = sys.argv[1]
print input_file
# sys.exit()

def get_avg_coverage(infile):
    total_coverage = 0 
    line_count = 0
    # calculate the average coverage for a column in the file
    with open(infile) as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for line in tsvin:
            line_count += 1
            coverage = line[2]
            total_coverage = total_coverage + int(coverage)
    avg_coverage = total_coverage / line_count
    return avg_coverage

avg_coverage = get_avg_coverage(input_file)
print 'Average Coverage', avg_coverage


def get_binned_stats(infile, avg_coverage):
    # separate the input into binned regions
    bin_size = 100 # size of the bins
    bin_count = 0 # bin iterator
    bin_coverage = 0 # starting coverage vale
    postion_stats = [] # placeholder for bin stats
    with open(infile) as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for line in tsvin:
            if (bin_count <= bin_size):
                # get values from the file line
                chrom = line[0]
                position = line[1]
                bin_position = int(position) / int(bin_size)
                coverage = line[2]
                bin_coverage = int(coverage) + bin_coverage
                if (bin_count == 0):
                    # start of the position
                    position_values = []
                    position_values.append(chrom)
                    # position_values.append(position)
                    position_values.append(bin_position)
                if (bin_count == bin_size):
                    # end of the position
                    # bin_avg_coverage = bin_coverage / bin_count
                    # position_values.append(position)
                    position_values.append(bin_position)
                    # coverage for the binned region / avg cov whole file
                    position_values.append(bin_coverage / avg_coverage) 
                    postion_stats.append(position_values)
                    # RESET
                    bin_count = 0
                    bin_coverage = 0
                    continue
                bin_count += 1
    return postion_stats

postion_stats = get_binned_stats(infile = input_file, avg_coverage = avg_coverage)

for line in postion_stats:
    print('\t'.join(map(str,line)))



# get average coverage per chromosome
def get_chrom_coverage(infile):
    total_coverage = 0 
    line_count = 0
    chrom_coverage_dict = collections.defaultdict(int)
    chrom_count_dict = collections.defaultdict(int)
    # calculate the total coverage per chromosome
    with open(infile) as tsvin:
        tsvin = csv.reader(tsvin, delimiter='\t')
        for line in tsvin:
            line_count += 1
            chrom = line[0]
            coverage = line[2]
            chrom_coverage_dict[chrom] += int(coverage)
            chrom_count_dict[chrom] += 1
    # calculate the average coverage per chromosome
    for key in chrom_coverage_dict.iterkeys():
        chrom_coverage_dict[key] = chrom_coverage_dict[key] / chrom_count_dict[key]
    return chrom_coverage_dict

chrom_coverage_dict = get_chrom_coverage(input_file)
print chrom_coverage_dict.keys()
print chrom_coverage_dict.values()


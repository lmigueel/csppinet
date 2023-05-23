# -*- coding: utf-8 -*-
#
#   This file is part of the tspex package, available at:
#   https://github.com/lucasmiguel/ppinet/
#
#   Tspex is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#   Contact: lucasmigueel@gmail.com

"""
Command-line interface for csppinet
"""

import argparse
import sys
import csppinet


def csppinet_cli(network_file, expression_file,threads, method,value):
	""" Biological network generation and analysis."""

	csppinet.construction(network_file,expression_file,method,value,threads)
	csppinet.network_metrics(expression_file)
	
def main():


	usage_text = '''example:

	 python3 csppinet.py --network_file network.csv --expression_file gene_expession.csv --method pre-threshold --value 2 --threads 2

	'''

	my_parser = argparse.ArgumentParser(epilog=usage_text)
	my_parser.add_argument('--network_file', type=str, help='A csv file containing the network.',required=True)
	my_parser.add_argument('--expression_file', type=str,help='A csv file containing the expression of the genes per condition.',required=True)
    my_parser.add_argument('--method', type=str,help='A method to determine protein expression. Choose between "3-sigma", "percentile" or "pre-threshold".',required=True)
    my_parser.add_argument('--value', type=str,default=0,help='A threshold value for "pre-threshold" or "percentile" method.  In the "pre-threshold" method, the threshold value represents an absolute threshold for gene expression. On the other hand, in the "percentile" method, the threshold value corresponds to the percentile cutoff. For example, a value of 5 represents the 5th percentile, while a value of 25 represents the 25th percentile or the first quartile.',required=False)
my_parser.add_argument('--threads', type=int,default=None,help='Number of threads for multiprocessing. Considere it for large networks.',required=False)

	args = my_parser.parse_args()    


	if len(sys.argv) < 4:
		parser.print_help()
		sys.exit(0)
	
	ppinet_cli(**vars(args))


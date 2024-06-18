import argparse
import sys
import subprocess
import datetime

def generate_params(temps, filename, bin_size, lattice_size):
    seed = 0
    num_warmup_sweeps = 1000
    num_sweeps = 1000
    measurements_per_bin = 10
    num_bins = bin_size
    spin_dim = 1
    print_spin_config = 1
    dim = 2
    J_param = 1
    h = 0

    param_file_name = './params/params_' + filename + '.txt'
    param_file = open(param_file_name, 'w')

    # format the parameter file
    l1 = '#	SIMULATION PARAMETERS\n'
    l2 = '           Temperature List = ' + str(temps) + '\n'
    l3 = '                        Seed = ' + str(seed) + '\n'
    l4 = '   Number of Warm-up Sweeps = ' + str(num_warmup_sweeps) + '\n'
    l5 = '     Sweeps per Measurement = ' + str(num_sweeps) + '\n'
    l6 = '       Measurements per Bin = ' + str(measurements_per_bin) + '\n'
    l7 = '             Number of Bins = ' + str(num_bins) + '\n'
    l8 = '         Dimension of Spins = ' + str(spin_dim) + '\n'
    l9 = '       Print Spins Configs? = ' + str(print_spin_config) + '\n\n'
    l10 = '# LATTICE PARAMETERS\n'
    l11 = '                D = ' + str(dim) + '\n'
    l12 = '                L = ' + str(lattice_size) + '\n\n'
    l13 = '# MODEL PARAMETERS\n'
    l14 = '                J = ' + str(J_param) + '\n'
    l15 = '                h = ' + str(h)


    # write the simulation parameters to the parameter file
    param_file.writelines(
        [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15])

    param_file.close()

    return param_file_name


def run_model(args):
    temps = [args.min_temp + i*args.increment for i in range(int((args.max_temp - args.min_temp) / args.increment) + 1)]

    filename = 't' + str(temps[0]) + '-t' + str(temps[-1]) + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    param_file = generate_params(temps, filename, args.bin_size, args.lattice_size)

    model_args = ['../ON_Model/onmc, filename']
    subprocess.run(model_args, cwd='./params/', check=True)
    print('Spin configurations generated.')


def main():
    # simulation parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bin_size', type=int, default=10,
                        help='Number of spin configurations to generate for each temperature')
    parser.add_argument('-l', '--lattice_size', type=int, default=16,
                        help='Size of lattice to generate spin configurations for')
    parser.add_argument('--increment', type=float, nargs='?', default=0.1,
                        help='Increment to use when generating temperatures')
    parser.add_argument('--min_temp', type=float, nargs='?', default=0.5,
                        help='Minimum temperature to generate data for')
    parser.add_argument('--max_temp', type=float, nargs='?', default=5,
                        help='Maximum temperature to generate data for')
    
    args = parser.parse_args()
    run_model(args)

if __name__ == '__main__':
    main()

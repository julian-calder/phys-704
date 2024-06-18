# Classifying Quantum States of Matter with Machine Learning
Code base for my physics senior project, containing all of the parameter files used for my research as well as a demo directory with the data already generated, allowing one to explore a working example.

## Installation instructions
### 1. Create a virtual environment in which to install packages
Note that we are going to use the built-in `venv` package, instead of dealing with conda environments. Functionality is the same, though.

```bash
$ python3 -m venv ~/.venv/tf
```
This will create a virtual environment in the directory `~/.venv/tf`, which you will then be able to "source" whenever you want to work in the environment. It's important to always activate the environment before you try to work on the code, otherwise the packages won't be visible and things won't work properly. This can be done with
```bash
$ source ~/.venv/tf/bin/activate
```


### 2. Install necessary packages
```bash
(tf) $ python3 -m pip install -r requirements.txt
```

### 3. Install tensorflow package (depending on hardware)
#### NVIDIA GPU
If you have an NVIDIA GPU, you can take advantage of the CUDA architecture to gain a significant computational speedup compared to using CPU-only computation. You can install the NVIDIA driver following [these instructions](https://www.nvidia.com/Download/index.aspx). Verify that it was installed successfully using 
```bash
(tf) $ nvidia-smi
```

Then, we can install the TensorFlow package with
```bash
(tf) $ python3 -m pip install tensorflow[and-cuda]
```

We can verify TensorFlow was installed successfully with GPU support by running 
```bash
(tf) $ python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```
If you see a list of GPU devices, TensorFlow was installed successfully.

#### CPU-only
If you don't have an NVIDIA GPU, you can still use TensorFlow though computation will take longer and your CPU will be under heavy load (not recommended).
```bash
(tf) $ python3 -m pip install tensorflow
```

We can verify TensorFlow was installed successfully by running 
```bash
(tf) $ python3 -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
```
If a tensor is returned, the installation worked.

## Using this code base
Once you have installed all of the necessary packages, we can begin to explore actually producing some data and analyzing it.  
### Setting up the Monte Carlo simulation
To produce the simulated spin configurations and bins, you will need to first clone the GitHub repository made by Lisa Hayward [available here](https://github.com/lhayward/ON_Model). 

Once you have cloned this repository, you need to modify the Makefile where is says "PROG: ". Here you must give a name for the executable which you will run to create the data. I recommend something like 'onmc'.

Some systems might have no issue with this, but make sure that you have `g++` installed, which is the C++ compiler for Linux. Depending on your system, you may need to run `sudo apt install g++` (Ubuntu) or `sudo dnf install g++` (Fedora) to ensure that the C++ compiler is installed.

Once the compiler is installed and you've modified the Makefile, you just need to type `make` in the your shell to create the executable. 

### Creating parameter files
Once your executable has been created, you have to pass it a parameter file with the filename "params_\*filename\*.txt". Below is a sample parameter file, where the important parameters are described as follows: 
```text
#	SIMULATION PARAMETERS
           Temperature List = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.02, 2.04, 2.06, 2.08, 2.1, 2.12, 2.14, 2.16, 2.18, 2.20, 2.22, 2.24, 2.26, 2.28, 2.3, 2.32, 2.34, 2.36, 2.38, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0]
                        Seed = 0
   Number of Warm-up Sweeps = 10000
     Sweeps per Measurement = 100
       Measurements per Bin = 10
             Number of Bins = 5000
         Dimension of Spins = 1
       Print Spins Configs? = 1

# LATTICE PARAMETERS
                D = 2
                L = [4, 4]

# MODEL PARAMETERS
                J = 1
                h = 0
```

#### SIMULATION PARAMETERS:
**Temperature List:** This is where you will type in a list of temperatures, separated by commas, at which you would like the monte carlo simulation to produce a set of spin configurations. The subsequent parameters will be run for each temperature in this list.

**Seed:** This is an initial seed which can be used for randomization of the system. You can vary this seed for every parameter file if you would like, but I kept it at 0 for all of my data generation.

**Number of Warm-up Sweeps:** This is the number of initial number of randomizations that the system will undergo before data sampling occurs. The larger this value is, the more likely you are to ensure no previous influence on the system. Making this value unnecessarily large, though, will slow down the time it takes to collect data for a given temperature.

**Sweeps per Measurement:** This number of sweeps per measurement corresponds to the number of times the monte carlo simulation is randomized before the next data point is collected. The larger this value is, the more likely you are to have each data point being collected be statistically independent from the others (which we want). Making this value too large, though, again slows down the time to generate data.

**Measurements per Bin:** This corresponds to how many statistically independent data points we want to have averaged for each of our bin and spin configuration data points. More measurements per bin gives us more representative data at the cost of, again, increased computation time. I found 10 measurements/bin sufficient for my research.

**Number of Bins:** The number of bins tells us how many individual data points we will get for each temperature. This value is most important when thinking about providing a sufficiently large dataset to feed to your neural network, and I found 5,000 bins per temperature to be sufficient.

**Dimension of Spins:** This value tells us whether we want to produce one-dimensional spins (as in the Ising model) or two-dimensional (like the xy model). Presumably this could be done in three dimensions, though my research did not explore that and I am not certain whether the simulation supports three-dimensional spin configurations.

**Print Spins Configs?:** This boolean value (either 0 or 1) dictates whether the simulation should print out individual spin configurations or not. If we want to train a neural network on the individual spin configurations representing a low-temperature system, this value needs to be set to 1.

#### LATTICE PARAMETERS:
**D:** This value tells the simulation the desired dimensions of our lattice. Since we are trying to study the two-dimensional Ising and XY models, we want this value to be 2.

**L:** This list tells us the specific dimensions of our two-dimensional lattice. I explored 4x4, 8x8, 16x16 and 32x32 sized lattices.

#### MODEL PARAMETERS:
**J:** This value of J corresponds to the energy constant $J$ used to describe the strength of bonds between individual points within a given magnetic lattice. The general convention is to use $J = 1$ here.

**h:** This constant can stay 0

---
Once you have created your parameter file, you can pass it to the simulation as follows. In the directory where you created your executable file, you need to run
```bash
./onmc *filename*
```
after which the simulation will begin. You will notice that both a `spinConfigs_*filename*` and `bins_*filename*` file will be created in same directory. I suggest that you create separate directories for `data` and `bins` and place these files there.

### Processing data once it has been generated
Once the bins and spin configuration files have been created, you can process this data as you would like. You will see a directory titled `demo` which has a sample parameter file which you can use to reproduce the data, and then a corresponding jupyter notebook to show some sample data processing with TensorFlow.
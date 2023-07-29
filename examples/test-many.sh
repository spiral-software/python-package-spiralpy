#! /bin/bash

##  Run examples of the run-xxxx.py scripts
##  These may use pre-libraries (when appropriate transforms and sizes have been
##  pre-built; ensure SP_LIBRARY_PATH is set to point to the library directory)

##  run-batchdft.py examples

echo "Run run-batchdft.py 16x1 60 APar APar True Double"
python run-batchdft.py 16x1 60 APar APar True Double
echo "Run run-batchdft.py 16x1 128 APar APar True Double"
python run-batchdft.py 16x1 128 APar APar True Double
echo "Run run-batchdft.py 16x1 440 APar APar True Double"
python run-batchdft.py 16x1 440 APar APar True Double

echo "Run run-batchdft.py 16x1 80 AVec APar True Double"
python run-batchdft.py 16x1 80 AVec APar True Double
echo "Run run-batchdft.py 16x1 256 AVec APar True Double"
python run-batchdft.py 16x1 256 AVec APar True Double
echo "Run run-batchdft.py 16x1 768 AVec APar True Double"
python run-batchdft.py 16x1 768 AVec APar True Double

echo "Run run-batchdft.py 16x1 64 APar AVec True Double"
python run-batchdft.py 16x1 64 APar AVec True Double
echo "Run run-batchdft.py 16x1 192 APar AVec True Double"
python run-batchdft.py 16x1 192 APar AVec True Double
echo "Run run-batchdft.py 16x1 224 APar AVec True Double"
python run-batchdft.py 16x1 224 APar AVec True Double

echo "Run run-batchdft.py 16x1 128 AVec AVec True Double"
python run-batchdft.py 16x1 128 AVec AVec True Double
echo "Run run-batchdft.py 16x1 440 AVec AVec True Double"
python run-batchdft.py 16x1 440 AVec AVec True Double
echo "Run run-batchdft.py 16x1 1024 AVec AVec True Double"
python run-batchdft.py 16x1 1024 AVec AVec True Double

echo "Run run-batchdft.py 16x1 60 APar APar False Double"
python run-batchdft.py 16x1 60 APar APar False Double
echo "Run run-batchdft.py 16x1 128 APar APar False Double"
python run-batchdft.py 16x1 128 APar APar False Double
echo "Run run-batchdft.py 16x1 440 APar APar False Double"
python run-batchdft.py 16x1 440 APar APar False Double

echo "Run run-batchdft.py 16x1 80 AVec APar False Double"
python run-batchdft.py 16x1 80 AVec APar False Double
echo "Run run-batchdft.py 16x1 256 AVec APar False Double"
python run-batchdft.py 16x1 256 AVec APar False Double
echo "Run run-batchdft.py 16x1 440 AVec APar False Double"
python run-batchdft.py 16x1 440 AVec APar False Double

echo "Run run-batchdft.py 16x1 64 APar AVec False Double"
python run-batchdft.py 16x1 64 APar AVec False Double
echo "Run run-batchdft.py 16x1 192 APar AVec False Double"
python run-batchdft.py 16x1 192 APar AVec False Double
echo "Run run-batchdft.py 16x1 224 APar AVec False Double"
python run-batchdft.py 16x1 224 APar AVec False Double

echo "Run run-batchdft.py 16x1 128 AVec AVec False Double"
python run-batchdft.py 16x1 128 AVec AVec False Double
echo "Run run-batchdft.py 16x1 256 AVec AVec False Double"
python run-batchdft.py 16x1 256 AVec AVec False Double
echo "Run run-batchdft.py 16x1 440 AVec AVec False Double"
python run-batchdft.py 16x1 440 AVec AVec False Double

##  run-dft.py examples
##  Currently DftSolver gives an error when trying to build code for 1D DFT -- it
##  uses the same script for batch DFTs and is fine when batch > 1

##  echo "Run run-dft.py 64 F d GPU"
##  python run-dft.py 64 F d GPU
##  echo "Run run-dft.py 64 F d CPU"
##  python run-dft.py 64 F d CPU
##  echo "Run run-dft.py 64 I d GPU"
##  python run-dft.py 64 I d GPU
##  echo "Run run-dft.py 64 I d CPU"
##  python run-dft.py 64 I d CPU
##  echo "Run run-dft.py 440 F d GPU"
##  python run-dft.py 440 F d GPU
##  echo "Run run-dft.py 440 F d CPU"
##  python run-dft.py 440 F d CPU
##  echo "Run run-dft.py 440 I d GPU"
##  python run-dft.py 440 I d GPU
##  echo "Run run-dft.py 440 I d CPU"
##  python run-dft.py 440 I d CPU

##  run-batchmddft.py examples

echo "Run run-batchmddft.py 48 4 F d GPU"
python run-batchmddft.py 48 4 F d GPU
echo "Run run-batchmddft.py 48 4 F d CPU"
python run-batchmddft.py 48 4 F d CPU
echo "Run run-batchmddft.py 48 4 I d GPU"
python run-batchmddft.py 48 4 I d GPU
echo "Run run-batchmddft.py 48 4 I d CPU"
python run-batchmddft.py 48 4 I d CPU
echo "Run run-batchmddft.py 128 4 F d GPU"
python run-batchmddft.py 128 4 F d GPU
echo "Run run-batchmddft.py 128 4 F d GPU"
python run-batchmddft.py 128 4 F d GPU
echo "Run run-batchmddft.py 128 4 I d GPU"
python run-batchmddft.py 128 4 I d GPU
echo "Run run-batchmddft.py 128 4 I d GPU"
python run-batchmddft.py 128 4 I d GPU

##  run-hockney*.py examples

echo "Run run-hockney130.py "
python run-hockney130.py 
echo "Run run-hockney8.py "
python run-hockney8.py 

##  run-mddft.py examples

echo "Run run-mddft.py 48 F d GPU"
python run-mddft.py 48 F d GPU
##  echo "Run run-mddft.py 48 F d GPU Fortran"
##  python run-mddft.py 48 F d GPU Fortran
echo "Run run-mddft.py 48 I d GPU"
python run-mddft.py 48 I d GPU
##  echo "Run run-mddft.py 48 I d GPU Fortran"
##  python run-mddft.py 48 I d GPU Fortran
echo "Run run-mddft.py 100,224,224 F d GPU"
python run-mddft.py 100,224,224 F d GPU
echo "Run run-mddft.py 100,224,224 I d GPU"
python run-mddft.py 100,224,224 I d GPU
echo "Run run-mddft.py 130 F d GPU"
python run-mddft.py 130 F d GPU
echo "Run run-mddft.py 130 I d GPU"
python run-mddft.py 130 I d GPU

##  run-mdprdft.py examples

echo "Run run-mdprdft.py 48 F d GPU"
python run-mdprdft.py 48 F d GPU
##  echo "Run run-mdprdft.py 48 F d GPU Fortran"
##  python run-mdprdft.py 48 F d GPU Fortran
echo "Run run-mdprdft.py 48 I d GPU"
python run-mdprdft.py 48 I d GPU
##  echo "Run run-mdprdft.py 48 I d GPU Fortran"
##  python run-mdprdft.py 48 I d GPU Fortran
echo "Run run-mdprdft.py 100,224,224 F d GPU"
python run-mdprdft.py 100,224,224 F d GPU
echo "Run run-mdprdft.py 100,224,224 I d GPU"
python run-mdprdft.py 100,224,224 I d GPU
echo "Run run-mdprdft.py 130 F d GPU"
python run-mdprdft.py 130 F d GPU
echo "Run run-mdprdft.py 130 I d GPU"
python run-mdprdft.py 130 I d GPU

##  run-mdrconv.py examples

echo "Run run-mdrconv.py 32 d GPU"
python run-mdrconv.py 32 d GPU
echo "Run run-mdrconv.py 48 d GPU"
python run-mdrconv.py 48 d GPU
echo "Run run-mdrconv.py 48,64,96 d GPU"
python run-mdrconv.py 48,64,96 d GPU
echo "Run run-mdrconv.py 130 d GPU"
python run-mdrconv.py 130 d GPU

##  run-mdrfsconv.py examples

echo "Run run-mdrfsconv.py 32 d GPU"
python run-mdrfsconv.py 32 d GPU
echo "Run run-mdrfsconv.py 64 d GPU"
python run-mdrfsconv.py 64 d GPU

##  run-stepphase.py examples

echo "Run run-stepphase.py 81"
python run-stepphase.py 81
echo "Run run-stepphase.py 125"
python run-stepphase.py 125

exit 0


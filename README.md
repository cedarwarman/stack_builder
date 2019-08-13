# stack_builder

## Description
This script is built to speed the process of making FIJI (ImageJ) stacks for
pollen microscopy experiments. It takes a folder containing a series of
sequentially numbered tif images and outputs user-defined stacks. Make sure the
tif images start with 1, or else the indexes will be off. Otherwise there's no requirements (as far as I
know).

## Usage
```
python3 /python/stack_builder -i /input_directory -r "A 1:30 B 31:60 C 61:90"
```

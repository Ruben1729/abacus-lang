#!/bin/bash

# Remove the extension from the file name
base_name=$(basename $1 .aba)

# Run the commands
nasm -felf64 ${base_name}.asm
ld -o ${base_name} ${base_name}.o
./${base_name}

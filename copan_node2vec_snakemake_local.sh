#!/bin/bash

conda activate snakemake

snakemake -c 2 -s Snakefile2 --rerun-incomplete

#!/bin/bash

conda activate snakemake

snakemake -c 2 --rerun-incomplete

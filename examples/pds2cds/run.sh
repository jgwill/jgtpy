#!/usr/bin/env bash
# Convert a sample PDS file to CDS
pds2cds -f ../../samples/SPX500_H1_240229.pds.full.csv -c 50 -o output.cds.csv

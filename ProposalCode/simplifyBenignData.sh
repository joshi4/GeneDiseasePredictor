#!/bin/sh
awk '{print $1 "\t" $2 "\t" $3}' ../BenignData/benign.bed | sed 's/chr//' > ../BenignData/benignSimple.bed
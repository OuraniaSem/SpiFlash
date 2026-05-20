# SpiFlash
Custom code for analyzing perceptual decision-making task data acquired with PyBpod, a GUI application for interacting with the Sanworks Bpod behavioral control system.

## This package contains analysis tools for:
1. A Go/No-Go task for sensory detection
2. A 2-alternative choice task for sensory discrimination

## Data format requirements
The analysis pipeline requires the following input files:
- Excel file (.xlsx):
  contains timestamps for each trial and all events occurring within a trial.
- JSON file (.json):
  contains metadata about each trial, including:
  a. Trial number and type
  b. Amplitude and Frequency of the stimulus 

## Features
- Behavioral data extraction
- Trial-by-trial analysis
- Psychometric curve fitting
- Visualization utilities

Related publications:
For the Go/No-Go Detection task: 
O.Semelidou, T.Gauvrit, C.Vandromme, et al. “Diminished Signal-to-Noise Ratio Disrupts Somatosensory Population Encoding and Drives Tactile Hyposensitivity in the Fmr1−/y Autism Model.” Advanced Science13, no. 28 (2026):   e19479. https://doi.org/10.1002/advs.202519479

For the 2-Alternative Forced Choice task: 
O. Semelidou, M. Tortochot-Megne Fotso, A. Winderickx, A. Frick (2025) Altered cognitive processes shape tactile perception in autism eLife 14:RP108333 https://doi.org/10.7554/eLife.108333.2 

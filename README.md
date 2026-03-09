# Levels checker
A Python-based Signal Quality Control (QC) tool designed to automate the auditing of large audio datasets. This utility scans directories for .wav, .mp3, and .flac files to verify compliance with RMS Energy and Peak Headroom thresholds.

Key Features

-Dual-Metric Analysis: Calculates Average RMS and True Peak levels using librosa and NumPy.

-Automated Flagging: Identifies files falling outside user-defined dB thresholds.

-Synchronized Reporting: Generates timestamped CSV and JSON reports.

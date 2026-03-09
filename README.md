# RMS-Threshold-Scanner
Automated audio quality control tool to identify high-noise floors and clipping in large datasets for AI training.

Key Features
-Batch Processing: Scans thousands of .wav, .mp3, or .flac files in seconds.

-Precision Metrics: Calculates the average RMS energy across the entire duration of each clip.

-Automated Reporting: Generates a .csv log of all "Flagged" files for easy review.

-Customizable Thresholds: Easily adjust decibel limits based on the specific requirements of the AI model.

Built With Python and:
-Librosa: For audio analysis.

-NumPy: For array processing of audio.

-Pandas: For data logging and CSV export.

How:
-Place your audio files in the /input directory.

-Set your desired threshold in config.py (e.g., -50dB).

-Run the scanner: "python rms-scanner.py"

-Review flagged_audio_report.csv for files requiring manual intervention.

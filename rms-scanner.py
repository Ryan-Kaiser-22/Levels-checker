import librosa
import numpy as np
import os
import csv

# --- CONFIGURATION ---
# Path to your audio files
INPUT_FOLDER = 'audio_samples' 
# RMS Threshold in Decibels (Anything louder than this -dB will be flagged)
# -50.0 is a common "noise floor" cutoff for clean dialogue
THRESHOLD_DB = -50.0 
OUTPUT_CSV = 'flagged_audio_report.csv'

def get_rms_db(audio_path):
    """Loads audio and calculates the average RMS level in decibels."""
    try:
        # Load audio (sr=None preserves original sample rate)
        y, sr = librosa.load(audio_path, sr=None)
        
        # Calculate RMS energy
        rms_data = librosa.feature.rms(y=y)
        avg_rms = np.mean(rms_data)
        
        # Convert power to decibels
        # ref=1.0 is standard for digital full scale
        rms_db = librosa.amplitude_to_db(np.array([avg_rms]), ref=1.0)[0]
        
        return round(rms_db, 2)
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return None

def main():
    # Create the input folder if it doesn't exist for the user
    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"Created folder: {INPUT_FOLDER}. Drop your .wav files there!")
        return

    files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(('.wav', '.mp3', '.flac'))]
    
    if not files:
        print("No audio files found in the input folder.")
        return

    print(f"Scanning {len(files)} files against threshold {THRESHOLD_DB} dB...")

    flagged_data = []

    for filename in files:
        file_path = os.path.join(INPUT_FOLDER, filename)
        db_level = get_rms_db(file_path)

        if db_level is not None:
            # If the level is HIGHER (less negative) than the threshold, flag it
            status = "FLAGGED" if db_level > THRESHOLD_DB else "CLEAN"
            print(f"{filename}: {db_level} dB [{status}]")
            
            if status == "FLAGGED":
                flagged_data.append([filename, db_level])

    # Write results to CSV
    with open(OUTPUT_CSV, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'RMS_dB_Level'])
        writer.writerows(flagged_data)

    print(f"\nScan complete. {len(flagged_data)} files flagged. Report saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
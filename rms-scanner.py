import librosa
import numpy as np
import os
import csv
import json
from datetime import datetime


INPUT_FOLDER = 'audio_samples' 
MIN_RMS_THRESHOLD = -60.0  #flag if file is too quiet/nothing there
MAX_PEAK_THRESHOLD = -5.0 #flag if hotter than this 
OUTPUT_CSV = 'audio_audit_report.csv'


def get_audio_db(audio_path):
    try:
        # sample rate not checked for this script
        y, _ = librosa.load(audio_path, sr=None)
        if len(y) == 0: return None
        
        rms_data = librosa.feature.rms(y=y)
        avg_rms = np.mean(rms_data)
        rms_db = librosa.amplitude_to_db(np.array([avg_rms]), ref=1.0)[0]
        
        peak_sample = np.max(np.abs(y))
        peak_db = librosa.amplitude_to_db(np.array([peak_sample]), ref=1.0)[0]
        
        return round(rms_db, 2), round(peak_db, 2)
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return None

def main():

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    output_csv = f"audit_{timestamp}.csv"
    output_json = f"audit_{timestamp}.json"

    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        return

    files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(('.wav', '.mp3', '.flac'))]
    if not files:
        print("No audio files found.")
        return

    print(f"Scanning {len(files)} files...")

    #export as CSV
    report_data = []
    flagged_count = 0

    for filename in files:
        file_path = os.path.join(INPUT_FOLDER, filename)
        result = get_audio_db(file_path)

        if result is not None:
            rms_val, peak_val = result
            
            if rms_val < MIN_RMS_THRESHOLD:
                status = "FLAGGED: Audio is too low"
            elif peak_val > MAX_PEAK_THRESHOLD:
                status = f"FLAGGED: Audio peaking above {MAX_PEAK_THRESHOLD}db"
            else:
                status = "CLEAN: Levels within range"

            if "FLAGGED" in status:
                flagged_count += 1
            
            print(f"{filename:25} | RMS: {rms_val:>6} | Peak: {peak_val:>6} | {status}")
            
            # report status of all files
            report_data.append([filename, rms_val, peak_val, status])

    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Filename', 'Avg_RMS_dB', 'Peak_dB', 'Status'])
        writer.writerows(report_data)

    json_data = [] 
    for row in report_data:
        json_data.append({
            "filename": row[0],
            "rms_db": round(float(row[1]), 2),   
            "peak_db": round(float(row[2]), 2),
            "status": row[3]
        })

    with open(output_json, "w") as jfile:
        json.dump(json_data, jfile, indent=4)

    print("-" * 30)
    print(f"Scan complete. Total: {len(report_data)} | Flagged: {flagged_count}")
    print(f"Report saved to {output_csv}")
    print(f"JSON report saved to: {output_json}")

if __name__ == "__main__":
    main()
import pandas as pd
import os
import csv
import openpyxl
from datetime import datetime
import StandardTime2425 as st2425
import StandardTime2526 as st2526

# Date threshold
threshold_date = datetime.strptime("2025-07-20", "%Y-%m-%d")

def get_standard_times_module(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    except Exception as e:
        print(f"Invalid date format: {date_str}, error: {e}")
        return st2425  # default
    if date_obj <= threshold_date:
        return st2425
    else:
        return st2526

def calc_std_times_updated(row, indices):
    try:
        std_module = get_standard_times_module(row["Date"])
        prefix = None
        if row["Track"] not in ["ST", "HV"]:
            return None
        # Determine prefix
        if "ALL" in row["Course"].upper():
            prefix = f"STA"
        else:
            prefix = f"STT" if row["Track"] == "ST" else "HV"
        suffix_map = {"Class 1": "C1", "Class 2": "C2", "Class 3": "C3", "Class 4": "C4", "Class 5": "C5", "Group": "GR", "Griffin": "G", "4 Year Olds": "C2"}
        suffix = next((v for k, v in suffix_map.items() if k in row["Class"]), None)
        if not suffix or not prefix:
            return None
        times = getattr(std_module, f"{prefix}{int(row['Distance'])}{suffix}")
        if isinstance(indices, int):
            return round(times[indices], 2)
        return round(sum(times[i] for i in indices), 2)
    except Exception as e:
        print(f"Error in calc_std_times_updated: {e}, row: {row}, indices: {indices}")
        return None

# Calculation functions
def calc_section_times(row, section_map, fields):
    distance = row["Distance"]
    sections = section_map.get(distance)
    if sections is None:
        return None
    return round(sum(float(row.get(f, 0) or 0) for f in fields[:sections]), 2)

calc_funcs = {
    "B400": lambda r: calc_section_times(r, {1000: 2, 1200: 2, 1400: 3, 1600: 3, 1650: 3, 1800: 4, 2000: 4, 2200: 5, 2400: 5},
                                           ["Sec_1_Time", "Sec_2_Time", "Sec_3_Time", "Sec_4_Time", "Sec_5_Time"]),
    "STDB400": lambda r: calc_std_times_updated(r, [0, 1]) if r["Distance"] in [1000, 1200] else
                calc_std_times_updated(r, [0, 1, 2]) if r["Distance"] in [1400, 1600, 1650] else
                calc_std_times_updated(r, [0, 1, 2, 3]) if r["Distance"] in [1800, 2000] else
                calc_std_times_updated(r, [0, 1, 2, 3, 4]) if r["Distance"] in [2200, 2400] else None,
    "TO": lambda r: calc_section_times(r, {1000: 3, 1200: 3, 1400: 4, 1600: 4, 1650: 4, 1800: 5, 2000: 5, 2200: 6, 2400: 6},
                                           ["Sec_1_Time", "Sec_2_Time", "Sec_3_Time", "Sec_4_Time", "Sec_5_Time", "Sec_6_Time"]),
    "STDTO": lambda r: calc_std_times_updated(r, [0, 1, 2]) if r["Distance"] in [1000, 1200] else
                calc_std_times_updated(r, [0, 1, 2, 3]) if r["Distance"] in [1400, 1600, 1650] else
                calc_std_times_updated(r, [0, 1, 2, 3, 4]) if r["Distance"] in [1800, 2000] else
                calc_std_times_updated(r, [0, 1, 2, 3, 4, 5]) if r["Distance"] in [2200, 2400] else None,
    "L400": lambda r: float(r.get({1000: "Sec_3_Time", 1200: "Sec_3_Time", 1400: "Sec_4_Time", 1600: "Sec_4_Time",
                                1650: "Sec_4_Time", 1800: "Sec_5_Time", 2000: "Sec_5_Time", 2200: "Sec_6_Time",
                                2400: "Sec_6_Time"}.get(r["Distance"]), 0) or 0),
    "STDL400": lambda r: calc_std_times_updated(r, 2) if r["Distance"] in [1000, 1200] else
                calc_std_times_updated(r, 3) if r["Distance"] in [1400, 1600, 1650] else
                calc_std_times_updated(r, 4) if r["Distance"] in [1800, 2000] else
                calc_std_times_updated(r, 5) if r["Distance"] in [2200, 2400] else None,
    "L800": lambda r: calc_section_times(r, {1000: 2, 1200: 2, 1400: 2, 1600: 2, 1650: 2, 1800: 2, 2000: 2, 2200: 2, 2400: 2},
                                           ["Sec_2_Time", "Sec_3_Time", "Sec_3_Time", "Sec_4_Time", "Sec_4_Time", "Sec_5_Time", "Sec_5_Time", "Sec_6_Time"]),
    "STDL800": lambda r: calc_std_times_updated(r, [1, 2]) if r["Distance"] in [1000, 1200] else
                calc_std_times_updated(r, [2, 3]) if r["Distance"] in [1400, 1600, 1650] else
                calc_std_times_updated(r, [3, 4]) if r["Distance"] in [1800, 2000] else
                calc_std_times_updated(r, [4, 5]) if r["Distance"] in [2200, 2400] else None,
    "T400": lambda r: round(float(r.get("L800", 0) or 0) - float(r.get("L400", 0) or 0), 2),
    "STDT400": lambda r: round(float(r.get("STDL800", 0) or 0) - float(r.get("STDL400", 0) or 0), 2),
    "CB400": lambda r: round(float(r.get("STDB400", 0) or 0) - float(r.get("B400", 0) or 0), 2),
    "CTO": lambda r: round(float(r.get("STDTO", 0) or 0) - float(r.get("TO", 0) or 0), 2),
    "CL400": lambda r: round(float(r.get("STDL400", 0) or 0) - float(r.get("L400", 0) or 0), 2),
    "CL800": lambda r: round(float(r.get("STDL800", 0) or 0) - float(r.get("L800", 0) or 0), 2),
    "CT400": lambda r: round(float(r.get("STDT400", 0) or 0) - float(r.get("T400", 0) or 0), 2),
    "TC": lambda r: round(float(r.get("CB400", 0) or 0) - float(r.get("CT400", 0) or 0), 2),
    "Style": lambda r: None if r["Distance"] not in [1000, 1200, 1400, 1600, 1650, 1800, 2000, 2200, 2400] else (
        "E" if (styler := round(sum(int(r.get(f"PIR_Sec_{i}", 0) or 0) for i in range(1, {1000: 3, 1200: 3, 1400: 4, 1600: 4,
        1650: 4, 1800: 5, 2000: 5, 2200: 6, 2400: 6}[r["Distance"]])) / ({1000: 2, 1200: 2, 1400: 3, 1600: 3, 1650: 3, 1800: 4,
        2000: 4, 2200: 5, 2400: 5}[r["Distance"]]), 0)) < 2 else "E/P" if styler < 6 else "P" if styler < 9 else "S")
}

# Helper function to safely get brandno
def get_brandno_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        if 'number' in df.columns:
            return df['number'].astype(str).tolist()
        else:
            print(f"Warning: 'number' column not found in {file_path}. Available columns: {df.columns.tolist()}")
            if len(df.columns) > 0:
                return df[df.columns[0]].astype(str).tolist()
            return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

# Input collection
racedate = input("Please input raceday (YYYYMMDD): ").strip()
database_name = input("Please input the database file name (e.g. HKData20250303): ").strip() + ".csv"

# Define the base directory
base_dir = "/Users/Lorenzo/Documents/racing/"
output_dir = os.path.join(base_dir, racedate)

def horsesearch(racenumber, brandno, headers):
    # Set the output file path to the racedate directory
    output_file = os.path.join(output_dir, f"{racedate}{racenumber}racecard.csv")

    with open(database_name, "r", encoding="utf-8") as db_file:
        database = csv.reader(db_file)
        horse_rows = [row for row in database for horse in brandno if horse in row[9]]

    if horse_rows:
        with open(output_file, "w", encoding="utf-8", newline="") as racecard:
            writer = csv.writer(racecard)
            header_list = headers.split(',') + ["Style", "STDB400", "B400", "CB400", "STDTO", "TO", "CTO",
                                                "STDL400", "L400", "CL400", "STDL800", "L800", "CL800",
                                                "STDT400", "T400", "CT400", "TC"]
            writer.writerow(header_list)
            writer.writerows(horse_rows)

        df = pd.read_csv(output_file).drop_duplicates()

        for col, func in calc_funcs.items():
            try:
                df[col] = df.apply(func, axis=1)
            except Exception as e:
                print(f"Error applying {col}: {e}")

        # Define a custom sorting key for surface (Turf vs All Weather) without sorting within Turf courses
        df["Surface_Key"] = df["Course"].apply(lambda x: 0 if x.startswith("TUR") else 1)

        # Sort by "Horse_Code", "Surface_Key", "Distance", "Date"
        df_sorted = df.sort_values(by=["Horse_Code", "Surface_Key", "Distance", "Date"])

        # Drop the temporary "Surface_Key" column to preserve original structure
        df_sorted = df_sorted.drop(columns=["Surface_Key"])

        # Add empty row after each horse group using a list
        frames = []
        empty_row_df = pd.DataFrame([[None] * len(df_sorted.columns)], columns=df_sorted.columns)
        for _, group in df_sorted.groupby("Horse_Code", sort=False):
            frames.append(group)
            frames.append(empty_row_df)

        # Concatenate all frames at once
        result_df = pd.concat(frames, ignore_index=True)

        # Remove the last empty row if it exists
        if not result_df.empty and result_df.iloc[-1].isna().all():
            result_df = result_df.iloc[:-1]

        result_df.to_csv(output_file, index=False)
        return True
    return False

# Main execution
try:
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    os.chdir(output_dir)
    race_files = [f for f in os.listdir() if f.endswith(".csv")]
    print(f"Found {len(race_files)} files in the folder.")

    headers = 'Date,Track,Distance,Class,Course,Going,Race,TAB,Horse_Name,Horse_Code,Jockey,Trainer,Fin_Pos,Margin,Weight,Bodyweight,BP,SP,Overall_Time,Sec_1_Time,Sec_2_Time,Sec_3_Time,Sec_4_Time,Sec_5_Time,Sec_6_Time,Time_To_Sec_1,Time_To_Sec_2,Time_To_Sec_3,Time_To_Sec_4,Time_To_Sec_5,Time_To_Sec_6,PIR_Sec_1,PIR_Sec_2,PIR_Sec_3,PIR_Sec_4,PIR_Sec_5,PIR_Sec_6'

    for race_file in race_files:
        racenumber = race_file.replace('.csv', '').replace(racedate, '')
        os.chdir(base_dir)  # Change to base_dir to access database_name
        brandno = get_brandno_from_csv(os.path.join(output_dir, race_file))
        if horsesearch(racenumber, brandno, headers):
            wb = openpyxl.Workbook()
            csv_path = os.path.join(output_dir, f"{racedate}{racenumber}racecard.csv")
            xlsx_path = os.path.join(output_dir, f"{racedate}{racenumber}.xlsx")
            with open(csv_path, encoding="utf-8") as f:
                for row in csv.reader(f):
                    wb.active.append(row)
            wb.save(xlsx_path)
            print(f"Processed race file: {race_file}")
        else:
            print(f"No matching horses found for race number {racenumber}.")
    os.chdir(output_dir)
    print("All files processed successfully.")
except Exception as e:
    print(f"Error: {e}")

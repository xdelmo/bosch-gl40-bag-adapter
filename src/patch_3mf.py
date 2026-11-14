import os
import sys
import json
import zipfile
import tempfile
import shutil


def modify_3mf(input_3mf, output_3mf):
    overrides = {
        "wall_loops": "4",
        "sparse_infill_density": "40%",
        "sparse_infill_pattern": "gyroid",
        "layer_height": "0.16",
        "enable_support": "0",
        "elefant_foot_compensation": "0",
        "filament_type": ["PETG"],
    }

    filament_specific = ["filament_type"]

    process_keys = [k for k in overrides.keys() if k not in filament_specific]
    filament_keys = [k for k in overrides.keys() if k in filament_specific]

    temp_dir = tempfile.mkdtemp()

    try:
        # Estrazione archivio 3MF
        with zipfile.ZipFile(input_3mf, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        settings_path = os.path.join(temp_dir, "Metadata", "project_settings.config")

        # Lettura e aggiornamento impostazioni
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        for k, v in overrides.items():
            settings[k] = v

        # Aggiornamento different_settings_to_system per evitare reset da UI Bambu Studio
        diff_arr = settings.get("different_settings_to_system", ["", ""])
        while len(diff_arr) < 2:
            diff_arr.append("")

        existing_proc = diff_arr[0].split(";") if diff_arr[0] else []
        existing_fil = diff_arr[1].split(";") if diff_arr[1] else []

        for k in process_keys:
            if k not in existing_proc:
                existing_proc.append(k)
        for k in filament_keys:
            if k not in existing_fil:
                existing_fil.append(k)

        diff_arr[0] = ";".join(sorted(existing_proc))
        diff_arr[1] = ";".join(sorted(existing_fil))
        settings["different_settings_to_system"] = diff_arr

        # Salvataggio impostazioni aggiornate
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

        # Ricreazione archivio 3MF
        with zipfile.ZipFile(output_3mf, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)

        print(f"Successfully generated {output_3mf}")

    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python patch_3mf.py <input> <output>")
        sys.exit(1)
    modify_3mf(sys.argv[1], sys.argv[2])

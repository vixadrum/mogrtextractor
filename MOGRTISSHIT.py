import os
import sys
import zipfile
import shutil
from pathlib import Path

supported = [".mogrt", ".aegraphic", ".zip"]


def safe_mkdir(path):
    Path(path).mkdir(parents=true, exist_ok=true)


def is_zip(file_path):
    try:
        with zipfile.ZipFile(file_path, "r"):
            return true
    except:
        return false


def extract_archive(src_file, out_dir):
    try:
        with zipfile.ZipFile(src_file, "r") as zip_ref:
            zip_ref.extractall(out_dir)
        return true
    except Exception as e:
        print(f"error: {src_file} ({e})")
        return false


def recursive_extract(folder):
    extracted_any = true

    while extracted_any:
        extracted_any = false

        for root, _, files in os.walk(folder):
            for file in files:
                full_path = Path(root) / file

                if full_path.suffix.lower() in supported:
                    out_dir = full_path.with_suffix("")

                    if out_dir.exists():
                        continue

                    temp_file = full_path
                    temp_created = false

                    # temp convert
                    if full_path.suffix.lower() in [".mogrt", ".aegraphic"]:
                        temp_zip = full_path.with_suffix(".zip")
                        shutil.copy(full_path, temp_zip)
                        temp_file = temp_zip
                        temp_created = true

                    if is_zip(temp_file):
                        safe_mkdir(out_dir)

                        if extract_archive(temp_file, out_dir):
                            print(f"[+] extracted {full_path} to {out_dir}")
                            extracted_any = true

                    if temp_created and temp_file.exists():
                        temp_file.unlink()


def main():
    if len(sys.argv) < 3:
        print("input.mogrt outputfolder")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not input_file.exists():
        print("not found")
        sys.exit(1)

    if input_file.suffix.lower() not in supported:
        print("not a mogrt or aegraphics")
        sys.exit(1)

    safe_mkdir(output_dir)

    temp_file = input_file
    temp_created = false

    # convert
    if input_file.suffix.lower() in [".mogrt", ".aegraphic"]:
        temp_zip = output_dir / (input_file.stem + ".zip")
        shutil.copy(input_file, temp_zip)
        temp_file = temp_zip
        temp_created = true

    print(f"extracting {input_file}")

    if not extract_archive(temp_file, output_dir):
        print("error")
        sys.exit(1)

    if temp_created and temp_file.exists():
        temp_file.unlink()

    recursive_extract(output_dir)

    print(f"[+] done {output_dir}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Script to update ZIP archives with extracted mod files.

This script will:
1. Navigate through each game directory in the mods folder
2. Find all non-ZIP files and directories in each game directory
3. Update the existing ZIP archive to include all extracted mod files
4. Keep both the updated ZIP file and the extracted folders

Expected structure:
project/
 ├─ mods/
 │   └─ game[serialNumber]/
 │        ├─ gameModArchive.zip (updated with current files)
 │        ├─ [Mod Folder 1]/
 │        ├─ [Mod Folder 2]/
 │        └─ [Mod Files...]
"""

import os
import zipfile
import shutil
from pathlib import Path
from typing import List, Optional, Tuple
from multiprocessing import Pool, cpu_count
import time


def get_non_zip_items(directory: Path) -> List[Path]:
    items = []
    if not directory.exists():
        return items
    
    for item in directory.iterdir():
        if item.is_file() and item.suffix.lower() != '.zip':
            items.append(item)
        elif item.is_dir():
            items.append(item)
    
    return items


def find_original_zip_name(mod_directory: Path) -> Optional[str]:
    for item in mod_directory.iterdir():
        if item.is_file() and item.suffix.lower() == '.zip':
            return item.name
    return None


def add_to_zip(zip_file: zipfile.ZipFile, source_path: Path, archive_name: str = None):
    if archive_name is None:
        archive_name = source_path.name
    
    if source_path.is_file():
        zip_file.write(source_path, archive_name)
    elif source_path.is_dir():
        if archive_name and not archive_name.endswith('/'):
            archive_name += '/'
        zip_file.writestr(zipfile.ZipInfo(archive_name), '')
        
        for child in source_path.iterdir():
            child_archive_name = f"{archive_name}{child.name}"
            add_to_zip(zip_file, child, child_archive_name)


def compact_mod_directory(mod_directory: Path, game_name: str) -> Tuple[bool, str]:
    try:
        original_zip_name = find_original_zip_name(mod_directory)
        if not original_zip_name:
            return False, f"No ZIP file found in {game_name}"
        
        items_to_compress = get_non_zip_items(mod_directory)
        
        if not items_to_compress:
            return True, f"No files to compress for {game_name}"
        
        zip_path = mod_directory / original_zip_name
        temp_zip_path = mod_directory / f"temp_{original_zip_name}"
        
        with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zip_file:
            for item in items_to_compress:
                add_to_zip(zip_file, item)
        
        if zip_path.exists():
            zip_path.unlink()
        temp_zip_path.rename(zip_path)
        
        return True, f"✓ {game_name}"
        
    except Exception as e:
        return False, f"✗ {game_name}: {str(e)}"


def process_single_game(game_dir: Path) -> Tuple[bool, str]:
    game_name = game_dir.name
    
    return compact_mod_directory(game_dir, game_name)


def process_all_mods(mods_path: Path) -> None:
    if not mods_path.exists():
        print(f"Error: Mods directory does not exist: {mods_path}")
        return
    
    game_directories = [d for d in mods_path.iterdir() if d.is_dir()]
    
    if not game_directories:
        print("No game directories found in the mods folder")
        return
    
    print(f"Found {len(game_directories)} game directories to process")
    print(f"Using {min(cpu_count(), len(game_directories))} CPU cores")
    
    start_time = time.time()
    
    with Pool(processes=min(cpu_count(), len(game_directories))) as pool:
        results = pool.map(process_single_game, game_directories)
    
    processed_count = sum(1 for success, _ in results if success)
    skipped_count = len(results) - processed_count
    
    print(f"\n--- Results ---")
    for success, message in results:
        print(message)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n--- Compacting Complete ---")
    print(f"Successfully processed: {processed_count} games")
    print(f"Skipped: {skipped_count} games")
    print(f"Total time: {elapsed_time:.2f} seconds")
    print(f"Average time per game: {elapsed_time/len(game_directories):.2f} seconds")


def main():
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    mods_path = project_root / "mods"
    
    print("Switch Ultrawide Mods Compactor")
    print("=" * 50)
    print(f"Project root: {project_root}")
    print(f"Mods directory: {mods_path}")
    
    response = input(f"\nProceed with compacting all mod directories? (y/n): ")
    if response.lower() != 'y':
        print("Operation cancelled")
        return
    
    process_all_mods(mods_path)
    
    print("\nCompacting complete!")


if __name__ == "__main__":
    main()

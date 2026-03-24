import argparse

# --- Global Constants ---
TB_TO_BYTES = 1_000_000_000_000      # 1 TB in Bytes
METADATA_RESERVE_PCT = 0.01          # 1% PTU
SAFETY_MARGIN_MULTIPLIER = 0.9       # 10% safety margin
FILE_SIZE_BYTES = 4096               # 4KiB file size

def calculate_from_capacity(total_usable_tb: float) -> dict:
    """Calculates the supported number of files based on the given capacity."""
    total_usable_bytes = total_usable_tb * TB_TO_BYTES
    ptu_reserve_bytes = total_usable_bytes * METADATA_RESERVE_PCT
    ptu_reserve_tb = ptu_reserve_bytes / TB_TO_BYTES
    safe_metadata_bytes = ptu_reserve_bytes * SAFETY_MARGIN_MULTIPLIER
    number_of_files = int(safe_metadata_bytes / FILE_SIZE_BYTES)
    
    return {
        "total_tb": total_usable_tb,
        "ptu_reserve_tb": ptu_reserve_tb,
        "supported_files": number_of_files
    }

def calculate_from_files(number_of_files: int) -> dict:
    """Calculates the required capacity based on the desired number of files."""
    safe_metadata_bytes = number_of_files * FILE_SIZE_BYTES
    ptu_reserve_bytes = safe_metadata_bytes / SAFETY_MARGIN_MULTIPLIER
    total_usable_bytes = ptu_reserve_bytes / METADATA_RESERVE_PCT
    
    total_usable_tb = total_usable_bytes / TB_TO_BYTES
    ptu_reserve_tb = ptu_reserve_bytes / TB_TO_BYTES
    
    return {
        "supported_files": number_of_files,
        "total_tb": total_usable_tb,
        "ptu_reserve_tb": ptu_reserve_tb
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculates metadata reservations for storage clusters in both directions."
    )
    
    # Create a mutually exclusive group where exactly ONE argument is required
    group = parser.add_mutually_exclusive_group(required=True)
    
    group.add_argument(
        "-c", "--capacity", 
        type=float, 
        help="Specifies the cluster capacity in TB to calculate the supported number of files."
    )
    
    group.add_argument(
        "-f", "--files", 
        type=int, 
        help="Specifies the number of files to calculate the required cluster capacity in TB."
    )
    
    args = parser.parse_args()
    
    # --- Format output based on the input ---
    if args.capacity is not None:
        result = calculate_from_capacity(args.capacity)
        print("-" * 55)
        print("Mode: Calculating file count from capacity")
        print("-" * 55)
        print(f"Cluster Capacity:       {result['total_tb']:.2f} TB")
        print(f"Metadata Reservation:   {result['ptu_reserve_tb']:.2f} TB (1% PTU)")
        print(f"Supported 4kB Files:    {result['supported_files']:,}")
        print("-" * 55)
        
    elif args.files is not None:
        result = calculate_from_files(args.files)
        print("-" * 55)
        print("Mode: Calculating capacity from file count")
        print("-" * 55)
        print(f"Desired 4kB Files:          {result['supported_files']:,}")
        print(f"Required Cluster Capacity:  {result['total_tb']:.2f} TB")
        print(f"Resulting PTU Reservation:  {result['ptu_reserve_tb']:.2f} TB (1%)")
        print("-" * 55)
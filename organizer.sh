#!/usr/bin/bash

# Configuration
CSV_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# 1. Creating archive directory if it doesn't exist
mkdir -p "$ARCHIVE_DIR"

# 2. Generating timestamp (format: YYYYMMDD-HHMMSS)
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# 3. Preparing new filename
BASENAME="${CSV_FILE%.*}"          # remove extension
EXTENSION="${CSV_FILE##*.}"        # keep extension (e.g., csv)
NEW_FILENAME="${BASENAME}_${TIMESTAMP}.${EXTENSION}"

# 4. Moving original file to archive with new name (if it exists)
if [ -f "$CSV_FILE" ]; then
    mv "$CSV_FILE" "$ARCHIVE_DIR/$NEW_FILENAME"
    echo "$TIMESTAMP: Archived $CSV_FILE -> $ARCHIVE_DIR/$NEW_FILENAME" >> "$LOG_FILE"
    
    # 5. Creating a fresh empty grades.csv
    touch "$CSV_FILE"
else
    echo "$TIMESTAMP: Warning: $CSV_FILE not found, nothing archived." >> "$LOG_FILE"
fi



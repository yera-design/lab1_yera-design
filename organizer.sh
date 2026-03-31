#!/usr/bin/bash

# Configuration
CSV_FILE="grades.csv"
ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"

# 1. Create archive directory if it doesn't exist
if ! mkdir -p "$ARCHIVE_DIR"; then
    echo "$(date +"%Y%m%d-%H%M%S") [ERROR] Failed to create archive directory: $ARCHIVE_DIR" >> "$LOG_FILE"
    exit 1
fi

# 2. Generate timestamp (format: YYYYMMDD-HHMMSS)
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

# 3. Prepare new filename
BASENAME="${CSV_FILE%.*}"          # remove extension
EXTENSION="${CSV_FILE##*.}"        # keep extension (e.g., csv)
NEW_FILENAME="${BASENAME}_${TIMESTAMP}.${EXTENSION}"

# 4. Move original file to archive with new name (if it exists)
if [ -f "$CSV_FILE" ]; then
    if mv "$CSV_FILE" "$ARCHIVE_DIR/$NEW_FILENAME"; then
        echo "$TIMESTAMP [INFO] Archived $CSV_FILE -> $ARCHIVE_DIR/$NEW_FILENAME" >> "$LOG_FILE"
    else
        echo "$TIMESTAMP [ERROR] Failed to archive $CSV_FILE" >> "$LOG_FILE"
        exit 1
    fi

    # 5. Create a fresh empty grades.csv
    if ! touch "$CSV_FILE"; then
        echo "$TIMESTAMP [ERROR] Failed to create new $CSV_FILE" >> "$LOG_FILE"
        exit 1
    fi
else
    echo "$TIMESTAMP [WARN] $CSV_FILE not found, nothing archived." >> "$LOG_FILE"
fi

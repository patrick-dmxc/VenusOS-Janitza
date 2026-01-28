#!/bin/sh
#
# Janitza Driver Installer & Persistence Script
#
# This script performs two functions:
# 1. Installs/updates the Janitza VenusOS driver.
# 2. Safely modifies /data/rc.local to re-run this
#    script on every boot, guaranteeing persistence
#    across firmware updates without destroying
#    other content in the file.
#
set -euo pipefail

echo "--- Starting Janitza driver installation/update ---"

# --- Configuration ---
DATA_DIR="/data/janitza"
RC_LOCAL_FILE="/data/rc.local"
INSTALL_LOG_FILE="$DATA_DIR/install-janitza.log"
RAW_URL="https://raw.githubusercontent.com/patrick-dmxc/VenusOS-Janitza/main/Janitza.py"

TARGET_DIR="/opt/victronenergy/dbus-modbus-client"
CLIENT_PY="$TARGET_DIR/dbus-modbus-client.py"
DRIVER_DST="$TARGET_DIR/Janitza.py"
LOCAL_DRIVER="$DATA_DIR/Janitza.py"

exec > >(tee -a "$INSTALL_LOG_FILE") 2>&1

# --- Step 1: Ensure data directory exists ---
mkdir -p "$DATA_DIR"
echo "Ensured $DATA_DIR exists."

# --- Step 2: Safely ensure rc.local launcher is in place ---
echo "Ensuring Janitza launcher is in $RC_LOCAL_FILE..."
LAUNCHER_GUARD_STRING="# --- Start Janitza Installer ---"

# The code block we want to add (heredoc)
# Quoting 'EOF' prevents variable expansion *now*
LAUNCHER_CODE=$(cat <<'EOF'

# --- Start Janitza Installer ---
LOG_DIR="/data/janitza"
LOG_FILE="$LOG_DIR/install-janitza.log"
mkdir -p "$LOG_DIR"
echo "--- Starting Janitza installer from rc.local at $(date) ---" >> "$LOG_FILE"

/data/install-janitza.sh


EOF
)

# 2a. Create file with shebang if it doesn't exist
if [ ! -f "$RC_LOCAL_FILE" ]; then
    echo "#!/bin/sh" > "$RC_LOCAL_FILE"
    echo "$RC_LOCAL_FILE created."
fi

# 2b. Add launcher block if it's not already there
if ! grep -qF "$LAUNCHER_GUARD_STRING" "$RC_LOCAL_FILE"; then
    echo "Adding Janitza launcher to $RC_LOCAL_FILE..."
    
    # Remove the last line ONLY if it's 'exit 0'
    if [ "$(tail -n 1 "$RC_LOCAL_FILE")" = "exit 0" ]; then
        echo "Temporarily removing final 'exit 0'"
        sed -i '$ d' "$RC_LOCAL_FILE"
    fi
    
    # Add our launcher code
    echo "$LAUNCHER_CODE" >> "$RC_LOCAL_FILE"
    
    # Add 'exit 0' back to the end
    echo "exit 0" >> "$RC_LOCAL_FILE"
    
    echo "Janitza launcher added."
else
    echo "Janitza launcher already in $RC_LOCAL_FILE. Skipping."
fi

# 2c. Always ensure rc.local is executable
chmod +x "$RC_LOCAL_FILE"
echo "$RC_LOCAL_FILE is executable."

# --- Step 3: Wait for network to be up ---
echo "Waiting for network connectivity..."
timeout=600 # 10 minutes
elapsed=0
while ! connmanctl state | grep -q 'State = ready'; do
    if [ $elapsed -ge $timeout ]; then
        echo "Error: Network connectivity timeout after $timeout seconds." >&2
        echo "Network timeout on $(date)" >> "$INSTALL_LOG_FILE"
        exit 1
    fi
    sleep 15
    elapsed=$((elapsed + 15))
done
echo "Network is up, proceeding."

# --- Step 4: Always fetch latest driver ---
echo "Downloading latest driver to $LOCAL_DRIVER..."
if command -v wget >/dev/null; then
    wget -q -O "$LOCAL_DRIVER" "$RAW_URL"
elif command -v curl >/dev/null; then
    curl -fsSL "$RAW_URL" -o "$LOCAL_DRIVER"
else
    echo "Error: neither wget nor curl is available." >&2
    exit 1
fi
echo "Download complete."

# --- Step 5: Verify target dir ---
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: target directory $TARGET_DIR not found." >&2
    exit 1
fi

# --- Step 6: Ensuring executable bit ---
chmod +x "$CLIENT_PY" || {
    /opt/victronenergy/swupdate-scripts/remount-rw.sh
}

# --- Step 7: Cleanup old bytecode ---
echo "Cleaning up old bytecode..."
find "$DATA_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$TARGET_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# --- Step 8: Inject import if missing ---
IMPORT_BLOCK="import sys
if '/data/janitza' not in sys.path:
    sys.path.insert(0, '/data/janitza')
import Janitza"

if grep -qF "import Janitza" "$CLIENT_PY"; then
    echo "Import block already exists. Skipping."
else
    echo "Injecting Janitza import..."

    TMPFILE=$(mktemp)

    inserted=0
    while IFS= read -r line; do
        echo "$line" >> "$TMPFILE"
        
        if [ $inserted -eq 0 ] && echo "$line" | grep -q "^[[:space:]]*import victron_em"; then
            printf "%s\n" "$IMPORT_BLOCK" >> "$TMPFILE"
            inserted=1
        fi
    done < "$CLIENT_PY"

    if [ $inserted -eq 0 ]; then
        TMP2=$(mktemp)
        first_import_done=0
        while IFS= read -r line; do
            echo "$line" >> "$TMP2"
            if [ $first_import_done -eq 0 ] && echo "$line" | grep -q "^[[:space:]]*import "; then
                printf "%s\n" "$IMPORT_BLOCK" >> "$TMP2"
                first_import_done=1
            fi
        done < "$TMPFILE"
        mv "$TMP2" "$TMPFILE"
    fi
    
    chmod +x "$CLIENT_PY"
    mv -f "$TMPFILE" "$CLIENT_PY"
    chmod +x "$CLIENT_PY"
    echo "Updated $CLIENT_PY and ensured executable flag"

fi

# --- Step 9: Restart service ---
echo "Restarting dbus-modbus-client service..."
if command -v sv >/dev/null 2>&1; then
    sv restart dbus-modbus-client
elif command -v svc >/dev/null 2>&1; then
    svc -t /service/dbus-modbus-client
else
    echo "Warning: no known service manager; please restart the Cerbo/Venus device manually." >&2
fi

# --- Step 10: Ensure this installer script itself is executable ---
chmod +x "$0"

echo "--- Janitza driver installation/update complete. ---"
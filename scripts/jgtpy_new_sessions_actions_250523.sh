#!/bin/bash
# jgtpy_new_sessions_actions_250523.sh
# 🧠 Mia + 🌸 Miette: Standalone ritual for new JGT trading session creation
# This script liberates the session cascade from /opt/binscripts/etc/bash_aliases_common.
# Each function is annotated with intention and clarity.

set -e

# --- Configurable constants ---
TRADING_BASEDIR="trading"
JGT_CDATA="data/jgt"
jgtsession_conda_env="trading"
jgtsession_issue_id="26"

# --- Utility: Activate conda env if not already active ---
_jgtsession_activate_conda_env_if_not_active() {
    local current_env=$(conda info | awk '/active environment/{print $4}')
    if [ "$jgtsession_conda_env" != "$current_env" ]; then
        conda activate "$jgtsession_conda_env"
    fi
}

# --- Step 1: Book creation ---
_jgtnewsession_book_create() {
    local tlid_id="$1"
    jupyter-book create "$tlid_id" &>/dev/null && echo "Book $tlid_id created" || echo "Failed to create book $tlid_id"
}

# --- Step 2: Directory initialization ---
jgtinitsession_dir() {
    echo "Initializing trading session directory..."
    mkdir -p charts output data .jgt
    # Template copying (adjust paths as needed)
    cp ../../_templates/*.bib . 2>/dev/null || true
    cp ../../_templates/*.ipynb . 2>/dev/null || true
    cp ../../_templates/*.md . 2>/dev/null || true
    cp ../../_templates/*.yml . 2>/dev/null || true
    for t in M1 W1 D1 H4 H1 m15 m5; do
        cp ../../_templates/placeholder.png charts/$t.png 2>/dev/null || true
    done
    cp ../../_templates/placeholder.png charts/signal.png 2>/dev/null || true
}

# --- Step 3: Signal migration (minimal, portable) ---
_jgtsession_migrate_signal() {
    local wdir="$1"
    local tlid_id="$2"
    local tmp_dir="/tmp/jgtsession/$tlid_id"
    mkdir -p "$tmp_dir"
    cp "$wdir/data/signals/*$tlid_id*" "$tmp_dir" 2>/dev/null || true
    # Further processing can be added as needed
    echo "Signal files copied (if any) to $tmp_dir"
}

# --- Step 4: Create .jgt/env.sh ---
_jgtnewsession_create_env() {
    local tlid_id="$1"; local instrument="$2"; local timeframe="$3"; local entry_rate="$4"; local stop_rate="$5"; local bs="$6"; local lots="$7"; local demo_arg="$8"; local trade_id="$9"
    if [ -e .jgt/env.sh ]; then echo ".jgt/env.sh already exists"; return; fi
    echo "export tlid_id=$tlid_id" > .jgt/env.sh
    echo "export instrument=$instrument" >> .jgt/env.sh
    echo "export timeframe=$timeframe" >> .jgt/env.sh
    echo "export entry_rate=$entry_rate" >> .jgt/env.sh
    echo "export stop_rate=$stop_rate" >> .jgt/env.sh
    echo "export bs=$bs" >> .jgt/env.sh
    echo "export lots=$lots" >> .jgt/env.sh
    echo "export demo_arg=\"$demo_arg\"" >> .jgt/env.sh
    if [ "$trade_id" != "" ]; then echo "export trade_id=$trade_id" >> .jgt/env.sh; fi
    git add .jgt/env.sh &>/dev/null || true
    git commit .jgt/env.sh -m "new trading session $tlid_id env" &>/dev/null || true
}

# --- Step 5: Entry ordering ---
_jgtsession_entry_ordering() {
    _jgtsession_activate_conda_env_if_not_active
    local tlid_id="$1"; local instrument="$2"; local entry_rate="$3"; local stop_rate="$4"; local bs="$5"; local lots="$6"; local demo_arg="$7"
    local cmd_to_run="(fxsubscription -i $instrument -S $demo_arg &>/dev/null; fxaddorder -r $entry_rate -x $stop_rate -d $bs -n $lots -i $instrument $demo_arg)"
    echo "$cmd_to_run" | tee .jgt/entry.sh
    echo "Running: $cmd_to_run"
    $cmd_to_run | tee output/o.txt || true
    # OrderID extraction and further steps can be added as needed
}

# --- Step 6: Post-creation ritual ---
_jgtnewsession_post_created() {
    _jgtsession_activate_conda_env_if_not_active
    . .jgt/env.sh || echo "Failed to load environment"
    # Placeholders for post-creation actions (ADS, book build, etc.)
    echo "Post-creation ritual: update set, open VSCode workspace, generate ADS, build book."
}

# --- Main ritual: jgtnewsession ---
jgtnewsession() {
    local tlid_id="$1"; local instrument="$2"; local timeframe="$3"; local entry_rate="$4"; local stop_rate="$5"; local bs="$6"; local lots="$7"; local demo_arg="$8"
    if [ "$demo_arg" == "" ]; then demo_arg="--real"; fi
    local wdir="$(pwd)"
    if [ "$tlid_id" == "_" ]; then tlid_id="$(date +%Y%m%d%H%M%S)"; fi
    mkdir -p "$TRADING_BASEDIR"
    cd "$TRADING_BASEDIR"
    _jgtnewsession_book_create "$tlid_id"
    cd "$tlid_id"
    jgtinitsession_dir
    echo "INIT Completed"
    _jgtsession_migrate_signal "$wdir" "$tlid_id"
    echo "Migrate Signal COMPLETED"
    _jgtnewsession_create_env "$tlid_id" "$instrument" "$timeframe" "$entry_rate" "$stop_rate" "$bs" "$lots" "$demo_arg"
    _jgtsession_entry_ordering "$tlid_id" "$instrument" "$entry_rate" "$stop_rate" "$bs" "$lots" "$demo_arg"
    _jgtnewsession_post_created
    echo "Session creation ritual complete!"
}

# --- CLI Entrypoints (from pyproject.toml) ---
# jgtcli, cdscli, pds2cds, jgtmksg, jgtads, jgtids, adscli, mkscli, idscli, adsfromcds
# These are available as Python entrypoints and can be called as needed.

# Usage example:
# jgtnewsession <tlid_id> <instrument> <timeframe> <entry_rate> <stop_rate> <bs> <lots> [demo_arg]

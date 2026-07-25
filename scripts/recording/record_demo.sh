#!/bin/bash
# ============================================================================
# Legal AI Copilot — Automated Screen Recording Script
# ============================================================================
# Uses xdotool for cursor/keyboard control and ffmpeg for screen capture.
# Records each scene as an independent file in recordings/
#
# Usage:
#   ./scripts/recording/record_demo.sh [scene_number]
#   ./scripts/recording/record_demo.sh        # record all scenes
#   ./scripts/recording/record_demo.sh 4      # record only scene 4
#
# Prerequisites:
#   - Backend running on http://localhost:8000
#   - Frontend running on http://localhost:5173
#   - Chrome installed
#   - xdotool installed
#   - ffmpeg installed
#   - Display :0 available
# ============================================================================

set -euo pipefail

# Configuration
RESOLUTION="1920x1080"
FPS="30"
FRONTEND_URL="http://localhost:3000"
RECORDINGS_DIR="$(dirname "$0")/../../recordings"
CHROME_WINDOW_NAME="Legal AI Copilot - Demo"

# Cursor helpers
CURSOR_SPEED="200"  # pixels per second for smooth movements

mkdir -p "$RECORDINGS_DIR"

# ============================================================================
# Helper functions
# ============================================================================

# Move cursor smoothly to (x, y) over a given duration in seconds
move_cursor() {
    local x=$1 y=$2 duration=${3:-1}
    xdotool mousemove --sync "$x" "$y"
    sleep "$duration"
}

# Move cursor slowly (for visible smooth movement)
# Animates movement in small steps to create visible cursor motion
move_cursor_slow() {
    local x=$1 y=$2 duration=${3:-2}
    local current_x current_y steps step_delay dx dy
    
    # Get current position
    eval $(xdotool getmouselocation --shell)
    current_x=$X
    current_y=$Y
    
    # Calculate steps (aim for ~30px per step)
    local dist=$(( (current_x - x) * (current_x - x) + (current_y - y) * (current_y - y) ))
    dist=$(echo "sqrt($dist)" | bc -l 2>/dev/null || echo "100")
    dist=${dist%.*}
    [ -z "$dist" ] && dist=100
    [ "$dist" -lt 1 ] && dist=1
    
    steps=$(( dist / 30 ))
    [ "$steps" -lt 1 ] && steps=1
    [ "$steps" -gt 50 ] && steps=50
    
    step_delay=$(echo "scale=3; $duration / $steps" | bc -l 2>/dev/null || echo "0.05")
    
    dx=$(( (x - current_x) / steps ))
    dy=$(( (y - current_y) / steps ))
    
    for i in $(seq 1 $steps); do
        current_x=$(( current_x + dx ))
        current_y=$(( current_y + dy ))
        xdotool mousemove "$current_x" "$current_y"
        sleep "$step_delay"
    done
    
    # Final exact position
    xdotool mousemove --sync "$x" "$y"
    sleep 0.5
}

# Click at current position
click() {
    local delay_after=${1:-0.5}
    xdotool click 1
    sleep "$delay_after"
}

# Type text character by character
type_text() {
    local text=$1 delay=${2:-0.05}
    xdotool type --delay $(echo "$delay * 1000 / 1" | bc) "$text"
    sleep 1
}

# Press Enter key
press_enter() {
    xdotool key Return
    sleep 1
}

# Scroll down by N pixels
scroll_down() {
    local pixels=${1:-400}
    local clicks=$((pixels / 100))
    for i in $(seq 1 $clicks); do
        xdotool click --window $(xdotool getactivewindow) 5
        sleep 0.1
    done
    sleep 1
}

# Scroll up by N pixels
scroll_up() {
    local pixels=${1:-400}
    local clicks=$((pixels / 100))
    for i in $(seq 1 $clicks); do
        xdotool click --window $(xdotool getactivewindow) 4
        sleep 0.1
    done
    sleep 1
}

# Start ffmpeg recording for a scene
start_recording() {
    local scene_num=$1 scene_name=$2
    local output="$RECORDINGS_DIR/scene_$(printf '%02d' $scene_num)_${scene_name}.mp4"
    
    ffmpeg -y \
        -f x11grab \
        -framerate $FPS \
        -video_size $RESOLUTION \
        -i :0.0+0,0 \
        -c:v libx264 \
        -preset fast \
        -crf 18 \
        -pix_fmt yuv420p \
        "$output" &
    
    FFMPEG_PID=$!
    RECORDING_FILE="$output"
    echo "  Recording started: $output (PID: $FFMPEG_PID)"
    sleep 2  # buffer before actions
}

# Stop ffmpeg recording
stop_recording() {
    echo "  Stopping recording..."
    kill -INT $FFMPEG_PID
    wait $FFMPEG_PID 2>/dev/null || true
    sleep 1
    echo "  Saved: $RECORDING_FILE"
}

# Launch Chrome at specific URL with a clean profile
launch_chrome() {
    local url=$1
    local profile_dir="/tmp/chrome-recording-profile"
    rm -rf "$profile_dir" 2>/dev/null || true
    google-chrome \
        --user-data-dir="$profile_dir" \
        --window-size=1920,1080 \
        --window-position=0,0 \
        --disable-extensions \
        --disable-notifications \
        --no-first-run \
        --no-default-browser-check \
        --disable-default-apps \
        --disable-popup-blocking \
        --disable-translate \
        --start-maximized \
        "$url" &
    CHROME_PID=$!
    sleep 6  # wait for Chrome to fully load
    
    # Focus the Chrome window
    xdotool search --onlyvisible --name "Chrome" windowactivate --sync 2>/dev/null || \
    xdotool search --onlyvisible --class "google-chrome" windowactivate --sync 2>/dev/null || true
    sleep 1
}

# Close Chrome
close_chrome() {
    kill $CHROME_PID 2>/dev/null || true
    sleep 2
}

# ============================================================================
# Scene recordings
# ============================================================================

# Scene 01 — Intro (00:00–00:30)
record_scene_01() {
    echo "=== Scene 01: Intro ==="
    launch_chrome "$FRONTEND_URL/login"
    start_recording 1 "intro"
    
    # Cursor at center, static screen
    move_cursor_slow 960 540 3
    # Move to logo
    move_cursor_slow 960 120 2
    sleep 3
    # Move back to center
    move_cursor_slow 960 540 2
    sleep 5
    # Move to credentials area
    move_cursor_slow 960 650 2
    sleep 8
    # Return to center
    move_cursor_slow 960 540 2
    sleep 3
    
    stop_recording
    close_chrome
}

# Scene 02 — Problem (00:30–01:15)
record_scene_02() {
    echo "=== Scene 02: Problem ==="
    launch_chrome "$FRONTEND_URL/login"
    start_recording 2 "problem"
    
    move_cursor_slow 960 540 2
    sleep 3
    # Move to email field
    move_cursor_slow 960 420 2
    sleep 3
    # Move to password field
    move_cursor_slow 960 490 2
    sleep 3
    # Move to login button
    move_cursor_slow 960 580 2
    sleep 5
    # Return to center
    move_cursor_slow 960 540 2
    sleep 8
    
    stop_recording
    close_chrome
}

# Scene 03 — Architecture (01:15–02:00)
record_scene_03() {
    echo "=== Scene 03: Architecture ==="
    launch_chrome "$FRONTEND_URL/login"
    start_recording 3 "architecture"
    
    # Neutral position
    move_cursor 1700 950 2
    sleep 3
    # Move to Advogado button
    move_cursor_slow 960 650 2
    sleep 3
    # Move to Admin button
    move_cursor_slow 960 720 2
    sleep 3
    # Move to center
    move_cursor_slow 960 540 2
    sleep 5
    # Move to login button
    move_cursor_slow 960 580 2
    sleep 8
    
    stop_recording
    close_chrome
}

# Scene 04 — Login (02:00–02:30)
record_scene_04() {
    echo "=== Scene 04: Login ==="
    launch_chrome "$FRONTEND_URL/login"
    start_recording 4 "login"
    
    # Click Advogado demo button
    move_cursor_slow 960 650 1
    sleep 0.5
    click 0.5
    sleep 2
    
    # Click Entrar
    move_cursor_slow 960 580 1
    sleep 0.5
    click 0.5
    sleep 5  # wait for redirect to dashboard
    
    # Cursor at center on dashboard
    move_cursor_slow 960 540 2
    sleep 5
    
    stop_recording
    close_chrome
}

# Scene 05 — Dashboard (02:30–03:00)
record_scene_05() {
    echo "=== Scene 05: Dashboard ==="
    # Login first
    launch_chrome "$FRONTEND_URL/login"
    sleep 3
    xdotool search --name "Chrome" windowactivate --sync
    move_cursor_slow 960 650 1
    click 0.5
    sleep 1
    move_cursor_slow 960 580 1
    click 0.5
    sleep 5  # wait for dashboard
    
    start_recording 5 "dashboard"
    
    # Cursor at center
    move_cursor_slow 960 540 2
    sleep 2
    
    # Move to navbar, traverse items
    move_cursor_slow 200 32 2
    sleep 1
    # Move across navbar
    for x in 300 400 500 600 700 800 900 1000 1100; do
        move_cursor_slow $x 32 0.4
    done
    sleep 1
    
    # Move to user/role area
    move_cursor_slow 1750 32 2
    sleep 2
    
    # Move to first document card
    move_cursor_slow 400 300 2
    sleep 3
    
    # Move to Upload PDF button
    move_cursor_slow 1700 120 2
    sleep 2
    
    # Click Upload PDF
    click 0.5
    sleep 3  # wait for navigation
    
    stop_recording
    close_chrome
}

# Scene 06 — Upload (03:00–04:00)
record_scene_06() {
    echo "=== Scene 06: Upload ==="
    # Login and navigate to upload
    launch_chrome "$FRONTEND_URL/login"
    sleep 3
    xdotool search --name "Chrome" windowactivate --sync
    move_cursor_slow 960 650 1
    click 0.5
    sleep 1
    move_cursor_slow 960 580 1
    click 0.5
    sleep 5
    # Navigate to upload
    move_cursor_slow 1700 120 2
    click 0.5
    sleep 3
    
    start_recording 6 "upload"
    
    # Click title field
    move_cursor_slow 960 350 2
    click 0.5
    type_text "Contrato de Prestação de Serviços" 0.05
    sleep 2
    
    # Click drop zone
    move_cursor_slow 960 550 2
    click 0.5
    sleep 2
    # File dialog - type path and enter
    type_text "$(realpath Contrato_Prestacao_Servicos_Teste.pdf)" 0.01
    sleep 1
    press_enter
    sleep 3
    
    # Click "Fazer Upload" button
    move_cursor_slow 960 750 2
    sleep 0.5
    click 0.5
    
    # Wait for processing (do NOT move cursor)
    echo "  Waiting for upload processing..."
    sleep 15
    
    # Success screen visible
    move_cursor_slow 960 540 3
    sleep 5
    
    stop_recording
    close_chrome
}

# Scene 07 — Analysis (04:00–05:30) — REQUIRES OPENAI
record_scene_07() {
    echo "=== Scene 07: Analysis (REQUIRES OPENAI) ==="
    launch_chrome "$FRONTEND_URL/login"
    sleep 3
    xdotool search --name "Chrome" windowactivate --sync
    move_cursor_slow 960 650 1
    click 0.5
    sleep 1
    move_cursor_slow 960 580 1
    click 0.5
    sleep 5
    # Navigate to analysis
    move_cursor_slow 500 32 2
    click 0.5
    sleep 3
    
    start_recording 7 "analysis"
    
    # Select document from dropdown
    move_cursor_slow 960 200 2
    click 0.5
    sleep 1
    # Select first option
    move_cursor_slow 960 250 1
    click 1
    
    # Wait for loading
    echo "  Waiting for analysis loading..."
    sleep 15
    
    # Move to summary card
    move_cursor_slow 960 350 2
    sleep 3
    
    # Scroll down to grid
    scroll_down 400
    sleep 3
    
    # Move to Partes card
    move_cursor_slow 400 500 2
    sleep 3
    
    # Move to Datas card
    move_cursor_slow 960 500 2
    sleep 3
    
    # Move to Valores card
    move_cursor_slow 1500 500 2
    sleep 3
    
    # Move to Cláusulas card
    move_cursor_slow 400 800 2
    sleep 3
    
    # Scroll back up
    scroll_up 600
    sleep 2
    
    # Move to "Iniciar Chat" button
    move_cursor_slow 1700 900 2
    sleep 3
    
    stop_recording
    close_chrome
}

# Scene 08 — Chat (05:30–05:30) — REQUIRES OPENAI
record_scene_08() {
    echo "=== Scene 08: Chat (REQUIRES OPENAI) ==="
    launch_chrome "$FRONTEND_URL/login"
    sleep 3
    xdotool search --name "Chrome" windowactivate --sync
    move_cursor_slow 960 650 1
    click 0.5
    sleep 1
    move_cursor_slow 960 580 1
    click 0.5
    sleep 5
    # Navigate to chat
    move_cursor_slow 400 32 2
    click 0.5
    sleep 3
    
    start_recording 8 "chat"
    
    # Click "Nova Conversa"
    move_cursor_slow 200 150 2
    click 1
    
    # Click message input
    move_cursor_slow 960 950 2
    click 0.5
    type_text "Quais riscos existem neste contrato?" 0.05
    sleep 2
    
    # Click send
    move_cursor_slow 1850 950 1
    sleep 0.5
    click 0.5
    
    # Wait for response
    echo "  Waiting for AI response..."
    sleep 20
    
    # Move to response
    move_cursor_slow 960 500 2
    sleep 5
    
    # Move to citations
    move_cursor_slow 960 700 2
    sleep 3
    
    # Scroll to disclaimer
    scroll_down 200
    sleep 2
    move_cursor_slow 960 850 2
    sleep 5
    
    stop_recording
    close_chrome
}

# Scene 09 — Risks (07:00–08:30)
record_scene_09() {
    echo "=== Scene 09: Risks ==="
    launch_chrome "$FRONTEND_URL/login"
    sleep 3
    xdotool search --name "Chrome" windowactivate --sync
    move_cursor_slow 960 650 1
    click 0.5
    sleep 1
    move_cursor_slow 960 580 1
    click 0.5
    sleep 5
    # Navigate to risks
    move_cursor_slow 600 32 2
    click 0.5
    sleep 3
    
    start_recording 9 "risks"
    
    # Select document
    move_cursor_slow 960 200 2
    click 0.5
    sleep 1
    move_cursor_slow 960 250 1
    click 2
    
    # Click "Analyze Risks"
    move_cursor_slow 960 350 2
    sleep 0.5
    click 0.5
    
    # Wait for analysis
    echo "  Waiting for risk analysis..."
    sleep 10
    
    # Move to overall risk card
    move_cursor_slow 960 300 2
    sleep 5
    
    # Move to risk cards
    move_cursor_slow 400 500 2
    sleep 3
    
    # Click Sources
    move_cursor_slow 300 650 2
    sleep 0.5
    click 2
    
    # Move to expanded sources
    move_cursor_slow 600 750 2
    sleep 3
    
    # Scroll to disclaimer
    scroll_down 300
    sleep 2
    move_cursor_slow 960 850 2
    sleep 5
    
    stop_recording
    close_chrome
}

# Scene 10 — Automations (08:30–09:15)
record_scene_10() {
    echo "=== Scene 10: Automations ==="
    launch_chrome "$FRONTEND_URL/login"
    sleep 3
    xdotool search --name "Chrome" windowactivate --sync
    move_cursor_slow 960 650 1
    click 0.5
    sleep 1
    move_cursor_slow 960 580 1
    click 0.5
    sleep 5
    # Navigate to automations
    move_cursor_slow 700 32 2
    click 0.5
    sleep 3
    
    start_recording 10 "automations"
    
    # Cursor at center
    move_cursor_slow 960 400 2
    sleep 3
    
    # Move to status badge
    move_cursor_slow 300 300 2
    sleep 3
    
    # Move to progress bar
    move_cursor_slow 600 350 2
    sleep 3
    
    # Move to webhook status
    move_cursor_slow 1300 350 2
    sleep 3
    
    # Move to filter
    move_cursor_slow 1700 120 2
    sleep 2
    
    # Scroll down
    scroll_down 300
    sleep 2
    
    # Move to links
    move_cursor_slow 400 500 2
    sleep 3
    move_cursor_slow 600 500 2
    sleep 3
    
    stop_recording
    close_chrome
}

# Scene 11 — Reviews (09:15–10:15)
record_scene_11() {
    echo "=== Scene 11: Reviews ==="
    launch_chrome "$FRONTEND_URL/login"
    sleep 3
    xdotool search --name "Chrome" windowactivate --sync
    move_cursor_slow 960 650 1
    click 0.5
    sleep 1
    move_cursor_slow 960 580 1
    click 0.5
    sleep 5
    # Navigate to reviews
    move_cursor_slow 800 32 2
    click 0.5
    sleep 3
    
    start_recording 11 "reviews"
    
    # Move to filters
    move_cursor_slow 1700 120 2
    sleep 2
    
    # Move to first card in list
    move_cursor_slow 400 250 2
    sleep 3
    
    # Click on card to open detail
    click 0.5
    sleep 5  # wait for detail to load
    
    # Move to content
    move_cursor_slow 960 400 2
    sleep 3
    
    # Scroll to history
    scroll_down 300
    sleep 2
    move_cursor_slow 960 600 2
    sleep 3
    
    # Move to review buttons
    move_cursor_slow 700 830 2
    sleep 2
    
    # Click Aprovar
    move_cursor_slow 600 830 1
    sleep 0.5
    click 0.5
    sleep 2
    
    # Type comment
    move_cursor_slow 960 870 1
    click 0.5
    type_text "Análise aprovada." 0.05
    sleep 2
    
    # Click Confirmar
    move_cursor_slow 960 920 1
    sleep 0.5
    click 1
    sleep 3
    
    stop_recording
    close_chrome
}

# Scene 12 — Insights (10:15–11:00)
record_scene_12() {
    echo "=== Scene 12: Insights ==="
    launch_chrome "$FRONTEND_URL/login"
    sleep 3
    xdotool search --name "Chrome" windowactivate --sync
    move_cursor_slow 960 650 1
    click 0.5
    sleep 1
    move_cursor_slow 960 580 1
    click 0.5
    sleep 5
    # Navigate to insights
    move_cursor_slow 900 32 2
    click 0.5
    sleep 3
    
    start_recording 12 "insights"
    
    # Move to 4 top cards
    move_cursor_slow 200 200 2
    sleep 2
    move_cursor_slow 600 200 1
    sleep 2
    move_cursor_slow 1000 200 1
    sleep 2
    move_cursor_slow 1400 200 1
    sleep 3
    
    # Scroll to grid
    scroll_down 300
    sleep 2
    
    # Move to Análises por Tipo
    move_cursor_slow 400 500 2
    sleep 3
    
    # Move to Status das Revisões
    move_cursor_slow 1400 500 2
    sleep 3
    
    # Move to Riscos por Severidade
    move_cursor_slow 400 750 2
    sleep 3
    
    # Move to Automações por Status
    move_cursor_slow 1400 750 2
    sleep 3
    
    # Scroll to estimativa
    scroll_down 300
    sleep 2
    
    # Move to estimativa
    move_cursor_slow 960 850 2
    sleep 3
    
    # Move to aviso
    scroll_down 100
    sleep 1
    move_cursor_slow 960 950 2
    sleep 3
    
    stop_recording
    close_chrome
}

# Scene 13 — Comparison (11:00–11:30) — REQUIRES OPENAI
record_scene_13() {
    echo "=== Scene 13: Comparison (REQUIRES OPENAI) ==="
    launch_chrome "$FRONTEND_URL/login"
    sleep 3
    xdotool search --name "Chrome" windowactivate --sync
    move_cursor_slow 960 650 1
    click 0.5
    sleep 1
    move_cursor_slow 960 580 1
    click 0.5
    sleep 5
    # Navigate to comparison
    move_cursor_slow 1100 32 2
    click 0.5
    sleep 3
    
    start_recording 13 "comparison"
    
    # Select document A
    move_cursor_slow 600 250 2
    click 0.5
    sleep 1
    move_cursor_slow 600 300 1
    click 1
    
    # Select document B
    move_cursor_slow 1300 250 2
    click 0.5
    sleep 1
    move_cursor_slow 1300 320 1
    click 1
    
    # Click Comparar
    move_cursor_slow 960 400 2
    sleep 0.5
    click 0.5
    
    # Wait for comparison
    echo "  Waiting for comparison..."
    sleep 15
    
    # Move to result
    move_cursor_slow 960 600 2
    sleep 5
    
    stop_recording
    close_chrome
}

# Scene 14 — Closing (11:30–12:30)
record_scene_14() {
    echo "=== Scene 14: Closing ==="
    launch_chrome "$FRONTEND_URL/login"
    sleep 3
    xdotool search --name "Chrome" windowactivate --sync
    move_cursor_slow 960 650 1
    click 0.5
    sleep 1
    move_cursor_slow 960 580 1
    click 0.5
    sleep 5
    # Navigate to dashboard
    move_cursor_slow 200 32 2
    click 0.5
    sleep 3
    
    start_recording 14 "closing"
    
    # Cursor at center, static
    move_cursor_slow 960 540 2
    sleep 10
    
    # Move to navbar slowly
    move_cursor_slow 500 32 3
    sleep 5
    
    # Return to center
    move_cursor_slow 960 540 3
    sleep 10
    
    # Move to neutral position
    move_cursor_slow 1700 950 2
    sleep 8
    
    stop_recording
    close_chrome
}

# ============================================================================
# Main execution
# ============================================================================

# Scenes that require OpenAI API
OPENAI_SCENES="7 8 13"

# Check if a specific scene was requested
if [[ $# -gt 0 ]]; then
    scene_num=$(printf '%02d' $1)
    echo "Recording single scene: $scene_num"
    record_scene_$scene_num
    echo "Done!"
    exit 0
fi

# Record all scenes
echo "Starting full demo recording..."
echo "Scenes requiring OpenAI: $OPENAI_SCENES"
echo ""

for scene in 01 02 03 04 05 06 07 08 09 10 11 12 13 14; do
    record_scene_$scene
    echo ""
    sleep 3  # pause between scenes
done

echo "=== All scenes recorded ==="
echo "Files in $RECORDINGS_DIR:"
ls -lh "$RECORDINGS_DIR"/scene_*.mp4 2>/dev/null || echo "No files found"

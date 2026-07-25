#!/bin/bash
# ============================================================================
# Record all 14 scenes and generate a report
# ============================================================================

set -euo pipefail

RECORDINGS_DIR="$(dirname "$0")/../../recordings"
REPORT_FILE="$RECORDINGS_DIR/RECORDING_REPORT.md"

mkdir -p "$RECORDINGS_DIR"

# Clean up old files
rm -f "$RECORDINGS_DIR"/scene_*.mp4 2>/dev/null || true

echo "=========================================="
echo "Legal AI Copilot — Full Demo Recording"
echo "=========================================="
echo "Starting at: $(date)"
echo ""

START_TIME=$(date +%s)

# Record all 14 scenes
for scene in 01 02 03 04 05 06 07 08 09 10 11 12 13 14; do
    scene_int=$((10#$scene))
    echo "Recording scene $scene..."
    
    scene_start=$(date +%s)
    
    if ./scripts/recording/record_demo.sh $scene_int 2>&1 | grep -E "Saved:|Error|FAIL" ; then
        scene_end=$(date +%s)
        scene_duration=$((scene_end - scene_start))
        echo "  ✓ Scene $scene completed in ${scene_duration}s"
    else
        echo "  ✗ Scene $scene failed"
    fi
    
    echo ""
    sleep 2
done

END_TIME=$(date +%s)
TOTAL_DURATION=$((END_TIME - START_TIME))

echo "=========================================="
echo "Recording completed at: $(date)"
echo "Total time: ${TOTAL_DURATION}s"
echo "=========================================="
echo ""

# Generate report
echo "Generating report..."

{
    echo "# Legal AI Copilot — Recording Report"
    echo ""
    echo "**Date**: $(date)"
    echo ""
    echo "**Total Duration**: ${TOTAL_DURATION}s (~$((TOTAL_DURATION / 60))m)"
    echo ""
    echo "## Scenes Recorded"
    echo ""
    
    for scene in 01 02 03 04 05 06 07 08 09 10 11 12 13 14; do
        scene_file="$RECORDINGS_DIR/scene_${scene}_"*.mp4
        if [ -f $scene_file 2>/dev/null ]; then
            size=$(ls -lh "$scene_file" 2>/dev/null | awk '{print $5}')
            duration=$(ffprobe -v quiet -print_format json -show_format "$scene_file" 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"{float(d['format']['duration']):.0f}s\")" 2>/dev/null || echo "?")
            echo "- **Scene $scene**: $size ($duration)"
        else
            echo "- **Scene $scene**: ❌ NOT FOUND"
        fi
    done
    
    echo ""
    echo "## Summary"
    echo ""
    total_size=$(du -sh "$RECORDINGS_DIR" 2>/dev/null | awk '{print $1}')
    echo "**Total size**: $total_size"
    echo ""
    echo "**Status**: $(ls -1 "$RECORDINGS_DIR"/scene_*.mp4 2>/dev/null | wc -l)/14 scenes recorded"
    
} > "$REPORT_FILE"

echo "Report saved to: $REPORT_FILE"
cat "$REPORT_FILE"

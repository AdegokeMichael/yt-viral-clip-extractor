#!/bin/bash

VIDEO_PATH=$1
START=$2
DURATION=$3
OUTPUT_PATH=$4

mkdir -p "$(dirname "$OUTPUT_PATH")"

ffmpeg -ss "$START" -i "$VIDEO_PATH" -t "$DURATION" -c:v libx264 -c:a aac "$OUTPUT_PATH"
#!/bin/bash

while true
do
    echo "Updating NFL scores at $(date)"
    python3 generate_scores_page.py
    echo "Scores updated. Waiting 60 seconds..."
    sleep 60
done
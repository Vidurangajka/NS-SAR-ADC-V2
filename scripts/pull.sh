#!/bin/bash

echo "Starting sync from Cadence server..."

rsync -avz --exclude='*.cdslck*' --exclude='*.log*' --exclude='.git' \
    user23@10.8.158.20:/home/user23/NS_SAR_ADC/libraries/ ~/Workspace/Git/NS_SAR_ADC/libraries/

rsync -avz --exclude='*.cdslck*' --exclude='*.log*' --exclude='.git' \
    user23@10.8.158.20:/home/user23/NS_SAR_ADC/simulation/adc_output.csv ~/Workspace/Git/NS_SAR_ADC/simulation/adc_output.csv

# rsync -avz --exclude='*.cdslck*' --exclude='*.log*' --exclude='.git' \
#     user23@10.8.158.20:/home/user23/NS_SAR_ADC/doc/ ~/Workspace/Git/NS_SAR_ADC/doc/

echo "Sync complete!"

pw-play /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || echo -e "\a"


echo "Running CSV benchmark..."
# python3 ~/Workspace/Git/NS_SAR_ADC/scripts/csv_benchmark.py

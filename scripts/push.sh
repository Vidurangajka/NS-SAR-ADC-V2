#!/bin/bash

echo "Sending to Cadence server..."

# rsync -avz --exclude='*.cdslck*' --exclude='*.log*' --exclude='.git/'   ~/Workspace/Git/NS_SAR_ADC/ user23@10.8.158.20:/home/user23/NS_SAR_ADC/
rsync -avz --exclude='*.cdslck*' --exclude='*.log*' --exclude='.git/'   ~/Workspace/Git/NS_SAR_ADC/libraries/NS_SAR_behavioural/ user23@10.8.158.20:/home/user23/NS_SAR_ADC/libraries/NS_SAR_behavioural/

echo "Send complete!"
pw-play /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null || echo -e "\a"
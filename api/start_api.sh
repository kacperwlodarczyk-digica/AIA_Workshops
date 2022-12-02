#!/bin/bash
API_PATH="AIA_Workshops/api"

# Extract 2 last components of current path
LAST_2=$(echo `pwd` | rev | cut -d'/' -f-2 | rev)

if [[ "$LAST_2" = "$API_PATH" ]]
then
    python3.9 src/main.py
else
    echo "You should run this script from ${API_PATH} directory. Change directory and rerun the script."
    exit 1
fi

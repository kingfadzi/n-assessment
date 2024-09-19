#!/bin/bash

# Check if all necessary arguments are provided
if [ $# -lt 6 ]; then
  echo "Usage: $0 <host> <instance> <port> <db> <table> <datecol> [limit]"
  exit 1
fi

# Assign arguments to variables
HOST=$1
INSTANCE=$2
PORT=$3
DB=$4
TABLE=$5
DATECOL=$6
LIMIT=$7

# Build the python command
CMD="python your_script_name.py --host $HOST --instance $INSTANCE --port $PORT --db $DB --table $TABLE --datecol $DATECOL"

# Add limit option if provided
if [ ! -z "$LIMIT" ]; then
  CMD="$CMD --limit $LIMIT"
fi

# Execute the Python script
echo "Executing: $CMD"
$CMD

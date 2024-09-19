#!/bin/bash

# Hard-coded database connection parameters for SQL Server
HOST="your_host"
INSTANCE="your_instance"
PORT="your_port"
DB="your_db"

# Check if the necessary parameters for the table are provided
if [ $# -lt 2 ]; then
  echo "Usage: $0 <table> <datecol> [period] [limit]"
  exit 1
fi

# Command line parameters for variable inputs
TABLE=$1
DATECOL=$2
PERIOD=$3   # Optional
LIMIT=$4    # Optional

# Build the command
CMD="python get_giant_table.py --host $HOST --instance $INSTANCE --port $PORT --db $DB --table $TABLE --datecol $DATECOL"

# Include period if provided
if [[ ! -z "$PERIOD" ]]; then
  CMD="$CMD --period $PERIOD"
fi

# Include limit if provided
if [[ ! -z "$LIMIT" ]]; then
  CMD="$CMD --limit $LIMIT"
fi

# Execute the command
echo "Executing: $CMD"
$CMD

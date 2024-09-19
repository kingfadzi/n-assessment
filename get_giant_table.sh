#!/bin/bash

# Hard-coded database connection parameters for SQL Server
HOST="your_host"
INSTANCE="your_instance"
PORT="your_port"
DB="your_db"

# Check if the necessary parameters for the table are provided
if [ $# -lt 2 ]; then
  echo "Usage: $0 <table> <datecol> [limit]"
  exit 1
fi

# Command line parameters for variable inputs
TABLE=$1
DATECOL=$2
LIMIT=$3  # This is optional

# Build the command
CMD="python get_giant_table.py --host $HOST --instance $INSTANCE --port $PORT --db $DB --table $TABLE --datecol $DATECOL"

# Include limit if provided
if [[ ! -z "$LIMIT" ]]; then
  CMD="$CMD --limit $LIMIT"
fi

# Execute the command
echo "Executing: $CMD"
$CMD

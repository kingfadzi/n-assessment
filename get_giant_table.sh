#!/bin/bash

# Script to run Python script with variable table, date column, and limit

# Check if all necessary connection arguments are provided
if [ $# -lt 4 ]; then
  echo "Usage: $0 <host> <instance> <port> <db>"
  echo "Follow this command with: <table> <datecol> [limit]"
  exit 1
fi

# Fixed database connection parameters
HOST=$1
INSTANCE=$2
PORT=$3
DB=$4

# Request user input for variable parameters
read -p "Enter the table name: " TABLE
read -p "Enter the date column: " DATECOL
read -p "Optional - Enter the limit (Press enter to skip): " LIMIT

# Build the command
CMD="python your_script_name.py --host $HOST --instance $INSTANCE --port $PORT --db $DB --table $TABLE --datecol $DATECOL"

# Add limit if provided
if [[ ! -z "$LIMIT" ]]; then
  CMD="$CMD --limit $LIMIT"
fi

# Execute the command
echo "Executing: $CMD"
$CMD

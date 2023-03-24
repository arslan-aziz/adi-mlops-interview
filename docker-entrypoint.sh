#!/bin/bash

if [ $# -eq 0 ]; then
    /bin/bash
fi

CMD_ARG=$1

if [ "$CMD_ARG" == "run" ]; then
    python -m data_ingestion.main
elif [ "$CMD_ARG" == "test" ]; then
    pytest .
elif [ "$CMD_ARG" == "help" ]; then
    echo "Run with the command \"run\" to run the data ingestion job."
    echo "Run with the command \"test\" to run unit tests."
else
    echo "Invalid command $CMD_ARG. Try running \"help\" to see available options."
fi

# accept argument of run or test
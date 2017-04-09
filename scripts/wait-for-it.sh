#!/bin/sh

#   Use this script to test if a given TCP host/port are available

cmdname=$(basename $0)

echoerr() { if [[ $QUIET -ne 1 ]]; then echo "$@" 1>&2; fi }

usage()
{
    cat << USAGE >&2
Usage:
    $cmdname host:port [-s] [-t timeout] [-- command args]
    -h HOST | --host=HOST       Host or IP under test
    -p PORT | --port=PORT       TCP port under test
                                Alternatively, you specify the host and port as host:port
    # -s | --strict               Only execute subcommand if the test succeeds
    -q | --quiet                Dont output any status messages
    -t TIMEOUT | --timeout=TIMEOUT
                                Timeout in seconds, zero for no timeout
    -- COMMAND ARGS             Execute command with args after the test finishes
USAGE
    exit 1
}




# process arguments
while [[ $# -gt 0 ]]
do
    case "$1" in
        -h)
        HOST="$2"
        if [[ $HOST == "" ]]; then break; fi
        shift 2
        ;;
        --host=*)
        HOST="${1#*=}"
        shift 1
        ;;
        -p)
        PORT="$2"
        if [[ $PORT == "" ]]; then break; fi
        shift 2
        ;;
        --port=*)
        PORT="${1#*=}"
        shift 1
        ;;
        -t)
        TIMEOUT="$2"
        if [[ $TIMEOUT == "" ]]; then break; fi
        shift 2
        ;;
        --timeout=*)
        TIMEOUT="${1#*=}"
        shift 1
        ;;
        -q | --quiet)
        QUIET=1
        shift 1
        ;;
        --)
        shift
        CLI="$@"
        break
        ;;
        --help)
        usage
        ;;
        *)
        echoerr "Unknown argument: $1"
        usage
        ;;
    esac
done


TIMEOUT=${TIMEOUT:-15}
QUIET=${QUIET:-0}
SHOULD_EXECUTE=0

if [[ "$HOST" == "" || "$PORT" == "" || $CLI == "" ]]; then
    echoerr "Error: you need to provide host and port to test condition and a command to run after the test is successfull."
    usage
    exit 1
else
    echo "Commmand : $CLI"

    start_ts=$(date +%s)
    while :
    do
        # (echo > /dev/tcp/$HOST/$PORT) >/dev/null 2>&1
        nc "$HOST" "$PORT" < /dev/null > /dev/null 2>&1
        result=$?
        if [[ $result -eq 0 ]]; then
            end_ts=$(date +%s)
            echoerr "$HOST:$PORT is available after $((end_ts - start_ts)) seconds"
            SHOULD_EXECUTE=1
            break
        fi
        end_ts=$(date +%s)
        if [[ $((TIMEOUT - $((end_ts - start_ts)))) -lt 0 ]]; then
            echoerr "timeout reached, exiting"
            break
        else
            echoerr "$HOST:$PORT is not available - sleeping"
            sleep 1
        fi
    done

    echo "Should execute : $SHOULD_EXECUTE"
    if [[ $SHOULD_EXECUTE -eq 1 ]]; then
        echoerr "$HOST:$PORT is up - executing command"
        exec $CLI
    fi

fi






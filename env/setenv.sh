# usage: source env/setenv.sh <environment>
# e.g. source env/setenv.sh replica
# check that we were passed a environment parameter and that we have a corresponding .env file in the env/ directory

if [ -z "$1" ]; then
    echo "Usage: source env/setenv.sh <env>"
    echo "  where <env> matches the name of a .env file without the extension"
    return 1
fi

if [ ! -f env/env.$1 ]; then
    echo "Error: env/env.$1 does not exist"
    return 1
fi

set -o allexport

# Clear environment variables

# Load environment variables from env file
source env/env.$1
EXTRA_ENV_FILE=env/env.$1

set +o allexport

# add (env) to the prompt
export PS1=${PS1:-}"($1) "

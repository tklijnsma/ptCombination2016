# export STARTDIR="$(fullpath $(dirname ${BASH_SOURCE[0]}))"
export STARTDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd $STARTDIR
. scripts/functions.sh

chmod +x scripts/*

export PATH="$(fullpath scripts):$PATH"
export PYTHONPATH="$(fullpath scripts):$PYTHONPATH"
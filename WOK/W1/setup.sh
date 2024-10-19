#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\e[0;31m'
GREEN='\e[0;32m'
YELLOW='\e[0;33m'
NC='\e[0m' 

# Banner setup 

banner1() {
    echo -e "-----------------------------------------------"
    echo -e "  Shell script to setup the following "
    echo -e "${GREEN}  Tyer - uv add typer   ${NC}"
    echo -e "${GREEN}     ${NC}"
    echo -e "-----------------------------------------------"
}


# Execution Sequence 
banner1
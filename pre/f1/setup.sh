#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\e[0;31m'
GREEN='\e[0;32m'
YELLOW='\e[0;33m'
NC='\e[0m' 

# Banner setup 

b1() {
    curl https://snips.sh/f/7l7_Yp0Htz
}


b2() {
    echo -e "-----------------------------------------------"
    echo -e "  Shell script to setup the following "
    echo -e "${GREEN}  uv add typer asyncio rich requests pytest-playwright  ${NC}"
    echo -e "${GREEN}  uvx playwright install --with-deps ${NC}"
    echo -e "-----------------------------------------------"
}

s1() {
    echo -e "${YELLOW} Executing ${NC}"
    uv add asyncio rich requests pytest-playwright
    uvx playwright install --with-deps
    uv tree
}


# Execution Sequence 
b1 # Main Banner 
b2 # Banner Text
s1
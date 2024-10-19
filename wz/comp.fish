#!/bin/fish
function comp
    echo ""
    echo ""
    echo " The following commands will b executed with this "
    echo (set_color FF55BB) " tar cvf - * | xz -T0 -9e -c > panty.tar.xz "
    echo (set_color 16FF00) " xz --list panty.tar.xz "
    tar cvf - * | xz -T0 -9e -c > panty.tar.xz
    xz --list panty.tar.xz
    ls -al panty.tar.xz
    curl  https://snips.sh/f/5d1unzQuUf
    echo " Decompresss= : tar -xvf panty.tar.xz -C <sniff - makedirectoryfirst>  "
end

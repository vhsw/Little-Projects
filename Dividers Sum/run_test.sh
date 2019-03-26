#!/bin/zsh

OUT=results.md

# header
printf "# Results\n\n" >> $OUT
printf "| Language " >> $OUT
for pow in {1..8}
do
    printf "| $((10**$pow)) " >> $OUT
done;
printf "|\n|$(printf "%0.s-" {1..78})|\n" >> $OUT


# data
for app in c cpp python rust
do
    printf "| $app" >> $OUT
    for pow in {1..8}
    do
        n=$((10**$pow))
        printf " | $(/usr/bin/time  -f"%e" ./$app'_dividers' $n 2>&1 > /dev/null)" >> $OUT
    done;
    printf " |\n" >> $OUT
done;

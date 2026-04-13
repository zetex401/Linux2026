# Answers

## Question 1
If there is no `set -e`, the script continues even after an error like `ls /nonexistent`. This is dangerous because later commands may use invalid data and produce incorrect results.

## Question 2
`[[ -f "$1" ]]` is safer than `[ -f "$1" ]` because it handles edge cases better. The second one may break if variables are not quoted or contain spaces.

## Question 3
`for file in $(ls *.log)` is an anti-pattern because it breaks filenames with spaces. The correct way is `for file in ./*.log; do ...; done`.

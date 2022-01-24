#!/bin/sh

export REVIEWDOG_GITHUB_API_TOKEN="${INPUT_GITHUB_TOKEN}"

python3 /usr/local/bin/converter.py $GITHUB_WORKSPACE/${INPUT_LINT_XML_FILE}
cat output_checkstyle.xml | reviewdog -f=checkstyle -name="Android Lint PR Review" -reporter="github-pr-review" -level="${INPUT_LEVEL}" ${INPUT_REVIEWDOG_FLAGS} -tee
cat output_checkstyle.xml | reviewdog -f=checkstyle -name="Android Lint PR Check" -reporter="github-pr-check" -level="${INPUT_LEVEL}" ${INPUT_REVIEWDOG_FLAGS} -tee

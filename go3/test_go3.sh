#!/bin/bash

# Script for running Go3 unit and basic functional tests

PROGRAM="go3.sh"
OUTPUTDIR="results_test_go3"
GO0DIR="../go0and1"

gogui-regress $PROGRAM -output $OUTPUTDIR $GO0DIR/test_go_base.tst
gogui-regress $PROGRAM -output $OUTPUTDIR $GO0DIR/test_simple_ko.tst
gogui-regress $PROGRAM -output $OUTPUTDIR $GO0DIR/test_suicide.tst
gogui-regress $PROGRAM -output $OUTPUTDIR test_go3.tst

# To do: add python unit tests for pattern code
# TESTS="test_pattern.py test_pattern_util.py test_go3.py"
#  
# for unit_test in $TESTS; do
#     python3 $unit_test
# done

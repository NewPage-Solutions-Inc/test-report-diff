
# The path to the directory containing the test report(s)
REP_DIR=$1
if [ "$REP_DIR" = "" ]
then
  REP_DIR="."
fi

# the filename for the failures report from the new run
NEW_FAILS=$2
if [ "$NEW_FAILS" = "" ]
then
  NEW_FAILS="fails.csv"
fi

test_report_diff -en "$REP_DIR/$NEW_FAILS" ~/Downloads/empty.json "$REP_DIR"

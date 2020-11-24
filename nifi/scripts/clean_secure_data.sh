#!/bin/bash
cd /opt/nifi/data/awaitingapproval/approved/processed || { echo 'Processed approval directory not found. Exiting.' ; exit 1; }
rm * || { echo 'Nothing to delete in processed approval directory.' ; }
cd /opt/nifi/data/awaitingapproval || { echo 'Awaiting approval directory not found. Exiting.' ; exit 1; }
rm *.json || { echo 'Nothing to delete in awaiting approval directory.' ; }
cd /opt/nifi/data/sum_report || { echo 'Summary report directory not found. Exiting.' ; exit 1; }
rm -r * || { echo 'Nothing to delete in sum_report directory.' ; }
cd /opt/nifi/data/popdataupload/processed || { echo 'Popdata upload directory not found. Exiting.' ; exit 1; }
rm -r * || { echo 'Nothing to delete in popdata upload directory.' ; }
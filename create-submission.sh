#/bin/sh
output_file=prj2code.tgz
./gen-report-pdf.sh
rm -f $output_file
tar -czf $output_file README.txt Report.pdf requirements.txt timePhase1.sh *.py

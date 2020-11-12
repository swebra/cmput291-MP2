#/bin/sh
output_file=prjcode.tgz
./gen-report-pdf.sh
rm -f $output_file
# tar -czf $output_file README.txt Report.pdf

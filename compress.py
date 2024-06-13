#!/usr/bin/env python3

import os,sys

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("PDF Compress File")
	parser.add_argument("-i", "--install", help="Install GhostScript", action="store_true",default=False)
	parser.add_argument("-f", "--file", help="The pdf file to compress.",nargs=1, default=None)
	parser.add_argument("--max", help="The max file size (MB).",nargs=1, default=[3])
	parser.add_argument("--compression", help="The starting compression value",nargs=1, default=[60])
	args,unknown = parser.parse_known_args()
	return args

<user>@4f05d1901f06 /sync # 
........................... while current_size > 3:
...........................     current_size = compress(file='thenticate_report.pdf', file_out='thenticate_report_JUSTGHOSTSCRIPT.pdf', compress_value=compression)
...........................     print(f"!!!!!Current Size of file: [{current_size}]")
...........................     compression -= 2
...........................     #import time;time.sleep(5)
...........................
........................... ^Iparser.add_argument("--save", help="Don't delete the repository",action="store_true",default=False)

def compress(file='thenticate_report.pdf', file_out='thenticate_report_mini.pdf', compress_value=75):
...........................     import os,sys,mystring
...........................     if os.path.exists(file_out):os.remove(file_out)
...........................     
...........................     
...........................     size=None
...........................     if os.path.exists(file_out):
...........................         size = os.stat(file_out).st_size/(1024*1024)
...........................     return size

if __name__ == "__main__":
	args = getArgs()
    if args.install:
        os.system("apt-get install -y ghostscript")
    if args.file:
        file = str(args.file[0]).strip()
        file_out = file.replace(".pdf", "_compressed.pdf")

        current_size = 100;
        compress_value=args.compression[0];
        max_file_size=args.max[0];


        while current_size > max_file_size:
            if os.path.exists(file_out):os.remove(file_out)

            cmd = f"gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/screen -dColorImageResolution={compress_value} -dGrayImageResolution={compress_value} -dMonoImageResolution={compress_value} -dColorImageDownsampleType=/Bicubic -dGrayImageDownsampleType=/Bicubic -dMonoImageDownsampleType=/Subsample -dEmbedAllFonts=true -dSubsetFonts=true -dAutoRotatePages=/None  -sOutputFile={file_out} {file}"
            
            print(cmd);os.system(cmd);
            if os.path.exists(file_out):
                current_size = os.stat(file_out).st_size/(1024*1024)
            else:
                print("FILE DOESN'T EXIST")
                sys.exit(-1)

        print(f"Compressed the file {file} to {file_out} with the following parameters {{compression:{compress_value},final_size:{current_size}}}")
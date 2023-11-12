import os,sys

def run(string):
	print(string)
	os.system(string)

def getArgs():
	import argparse
	parser = argparse.ArgumentParser("mp")
	parser.add_argument("-i","--input", help="Convert the mp4 to whatever",nargs=1, default=None)
	parser.add_argument("--mp3", action="store_true",default=False, help="convert to mp3")
	return parser.parse_args()

if __name__ == '__main__':
	args = getArgs()
	if args.mp3:
		run(f"ffmpeg -i {args.input[0]} -vn {args.input[0].replace('.mp4','.mp3')}")
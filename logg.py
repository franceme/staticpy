def follow(filename):
    thefile = open(filename, "r")

    import os,time
    '''generator function that yields new lines in a file
    '''
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)
    
    # start infinite loop
    while True:
        # read last line of file
        line = thefile.readline()        # sleep if file hasn't been updated
        if not line:
            time.sleep(.1)
            continue

        yield line

def getArgs():
    import argparse
    parser = argparse.ArgumentParser("Following")
    parser.add_argument("-f","--file", help="File to watch",nargs=1, default=None)
    return parser.parse_args()

if __name__ == '__main__':
    args = getArgs()

    logg = follow(args.file[0])
    for line in logg:
        print(line,end='', flush=True)

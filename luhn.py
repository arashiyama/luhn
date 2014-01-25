#!/usr/bin/python
from __future__ import print_function
import sys, string, argparse, signal

def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

def cardLuhnChecksumIsValid(card_number):
    """ checks to make sure that the card passes a luhn mod-10 checksum """
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    for count in range(0, num_digits):
        digit = int(card_number[count])
        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum = sum + digit
    return ( (sum % 10) == 0 )

def starout(card_number,starout=True):
    """ drop middle digits from PAN. We're going to assume 13 digit PANs are all dead now """
    if starout:
        return(card_number[0:5]+"******"+card_number[-4:])
    else:
        return(card_number)
    
def main(me,argv):
    # setup some vars
    panlist=[]
    # parse arguments - the default with no arguments will be to take argv (or stdin) as a list of PANs to be luhn'd
    # should accept STDIN, -i FILENAME, or cmdlinkargs
    parser=argparse.ArgumentParser(description='A Luhn checker with benefits!')
    parser.add_argument('-s','--nostarout', help="Disable display masking",action="store_false")
    parser.add_argument('PAN',nargs='?',default=False,help="Optionally provide PAN on command line")
    parser.add_argument('-i','--input',help="name of input file (defaults to STDIN)", nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-o','--output', help="name of output file (defaults to STDOUT)",nargs='?', type=argparse.FileType('a'), default=sys.stdout)
    args=parser.parse_args()
    
# FIX ARG PROCESSING (or should that be argh)
    if args.PAN:
        panlist.append(args.PAN.strip())
    else:
        for l in args.input:
            l=l.strip()
            if len(l)==16:
                panlist.append(l)
            # else drop silently
# Need to present a list of numbers to the function.
    if len(panlist)<1:
        print (me,": Glurk. No PANs. Giving up.")
        exit(2)
    for pan in panlist:
        if cardLuhnChecksumIsValid(pan):
            print ("[+] Valid PAN",starout(pan,args.nostarout), file=args.output)
        else:
            print ("[-] Invalid PAN",starout(pan,args.nostarout), file=args.output)    

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main(sys.argv[0],sys.argv[1:])

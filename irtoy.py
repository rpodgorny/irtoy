#!/bin/env python

import serial
import time
import sys

dev = '/dev/ttyACM0'
command = None
fn = None

def read_all(p):
	ret = ''
	while p.inWaiting(): ret += p.read(1)
	return ret
#enddef

def reset(p):
	#p.write('\xff' * 10)
	p.write('\x00' * 10)
	p.write('s')
	print repr(p.read(3))
	p.write('\x24')
	p.write('\x25')
	p.write('\x26')

	p.write('\x23')
	print 'kuku', repr(p.read(8))
#enddef

def send(p, buf):
	p.write('\x03')

	req = ord(p.read(1))
	while req and buf:
		print req
		p.write(buf[:req])
		buf = buf[req:]
		req = ord(p.read(1))
	#endwhile

	print repr(p.read(3))
	print repr(p.read(1))
#enddef

def main():
	global command, fn
	command = sys.argv[1]
	fn = sys.argv[2]

	if command not in ('recv', 'send'):
		print 'unknown command %s!' % command
		return
	#endif

	if not fn:
		print 'filename not specified!'
		return
	#endif

	p = serial.Serial(dev)
	#while p.inWaiting(): p.read(1)

	reset(p)

	if command == 'recv':
		f = open(fn, 'w')
	elif command == 'send':
		f = open(fn, 'r')
		buf = f.read(10000)
		print repr(buf), len(buf)
		f.close()
		send(p, buf)
		time.sleep(1)
		p.close()
		return
	#endif

	buf = ''
	while 1:
		buf += p.read(1)
		print '.',

		if buf.endswith('\xff\xff'):
			print repr(buf), len(buf)

			f.write(buf)
			f.close()
			break
		#endif
	#endwhile

	p.close()
#enddef

if __name__ == '__main__': main()

#!/usr/bin/python

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


def reset(p):
	#p.write('\xff' * 10)
	p.write(b'\x00' * 10)
	p.write(b's')
	print(repr(p.read(3)))
	p.write(b'\x24')
	p.write(b'\x25')
	p.write(b'\x26')

	#p.write(b'\x23')
	#print('kuku %s' % repr(p.read(8)))


def send(p, buf):
	p.write(b'\x03')

	req = ord(p.read(1))
	while req and buf:
		print(req)
		p.write(buf[:req])
		buf = buf[req:]
		req = ord(p.read(1))

	res = p.read(3)
	transmitted = (res[1] << 8) + res[2]
	print(transmitted)

	print(repr(p.read(1)))


def main():
	global command, fn
	command = sys.argv[1]
	fns = sys.argv[2:]

	if command not in ('recv', 'send'):
		print('unknown command %s!' % command)
		return

	if not fns:
		print('filename(s) not specified!')
		return

	p = serial.Serial(dev)

	print('consuming leftover bytes')
	while p.inWaiting():
		p.read(1)
		print('.')

	print('reset')
	reset(p)

	if command == 'recv':
		print('recv')
		f = open(fns[0], 'wb')
	elif command == 'send':
		print('send')
		for fn in fns:
			f = open(fn, 'rb')
			buf = f.read(10000)
			print('%s %s' % (repr(buf), len(buf)))
			f.close()
			send(p, buf)
			time.sleep(1)

		p.write(b'\x00' * 10)
		#time.sleep(1)
		p.close()
		return

	buf = b''
	while 1:
		buf += p.read(1)
		print('.')

		if buf.endswith(b'\xff\xff'):
			print('%s %s' % (repr(buf), len(buf)))

			f.write(buf)
			f.close()
			break

	p.close()


if __name__ == '__main__':
	main()

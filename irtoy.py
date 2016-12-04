#!/usr/bin/python3

import serial
import time
import sys


dev = '/dev/ttyACM0'
command = None
fn = None


# TODO: unused?
def read_all(p):
	ret = b''
	while p.inWaiting():
		ret += p.read(1)
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
		return 1

	if not fns:
		print('filename(s) not specified!')
		return 1

	p = serial.Serial(dev)

	print('consuming leftover bytes')
	while p.inWaiting():
		p.read(1)
		sys.stdout.write('.')
		sys.stdout.flush()

	print('reset')
	reset(p)

	if command == 'recv':
		print('recv')
		buf = b''
		while 1:
			buf += p.read(1)
			sys.stdout.write('.')
			sys.stdout.flush()
			if buf.endswith(b'\xff\xff'):
				print('%s %s' % (repr(buf), len(buf)))
				break
		with open(fns[0], 'wb') as f:
			f.write(buf)
	elif command == 'send':
		print('send')
		for fn in fns:
			with open(fn, 'rb') as f:
				buf = f.read(10000)
			print('%s %s' % (repr(buf), len(buf)))
			send(p, buf)
			time.sleep(1)

		p.write(b'\x00' * 10)
		#time.sleep(1)

	p.close()
	return 0


if __name__ == '__main__':
	sys.exit(main())

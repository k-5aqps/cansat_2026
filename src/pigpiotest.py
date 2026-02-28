import pigpio
pi = pigpio.pi()
print(pi.connected)
pi.stop()

#1がでればOK-->0ならsudo pigpiod or sudo systemctl enable pigpiod で再起動
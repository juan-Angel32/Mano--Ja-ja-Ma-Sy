import network
import socket
from machine import Pin, ADC
from time import sleep

# Configurar los pines de entrada para los sensores flex
flex_5 = ADC(Pin(36))  # ADC1_CH0 (GPIO 36)
flex_4 = ADC(Pin(39))  # ADC1_CH3 (GPIO 39)
flex_3 = ADC(Pin(34))  # ADC1_CH6 (GPIO 34)
flex_2 = ADC(Pin(35))  # ADC1_CH7 (GPIO 35)
flex_1 = ADC(Pin(32))  # ADC1_CH4 (GPIO 32)

# Función para mapear los valores como en Arduino
def map_value(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Conectar a la red Wi-Fi
ssid = 'TuSSID'
password = 'TuContraseña'
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)

# Esperar a que se establezca la conexión
while not ap.active():
    sleep(1)

print('Conexión establecida, IP:', ap.ifconfig()[0])

# Configurar el socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
sock = socket.socket()
sock.bind(addr)
sock.listen(1)

print('Esperando conexión...')

while True:
    cl, addr = sock.accept()
    print('Conectado desde', addr)
    
    # Leer y mapear los valores de los sensores flex
    flex_5_val = map_value(flex_5.read(), 630, 730, 80, 20)
    flex_4_val = map_value(flex_4.read(), 520, 710, 70, 175)
    flex_3_val = map_value(flex_3.read(), 510, 680, 140, 10)
    flex_2_val = map_value(flex_2.read(), 580, 715, 90, 175)
    flex_1_val = map_value(flex_1.read(), 550, 700, 90, 175)
    
    # Crear el mensaje con los valores leídos
    msg = "{},{},{},{},{}".format(flex_5_val, flex_4_val, flex_3_val, flex_2_val, flex_1_val)
    
    # Enviar el mensaje
    cl.send(msg)
    cl.close()
    
    # Esperar un momento antes de la siguiente lectura
    sleep(1)

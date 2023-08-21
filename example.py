import slippylib

ready = False

slippy = slippylib.SlipPy("/dev/ttyACM0")

def message(dest_address, src_address, rssi, snr, msg_id, message):
    print(f"<{src_address}> {message}")
    #print(f"More Info:\n  TO: {dest_address}\n  RSSI: {rssi}\n  SNR: {snr}\n  MESSAGE ID: {msg_id}")

def ready(addr):
    #print(f"Your address is: {addr}")

    global ready
    ready = True

slippy.on_message = message
slippy.on_ready = ready

while True:
    if ready: 
        ip = input("ip: ")
        message = input("message: ")
        print(f"Sending: \"{message}\"")
        slippy.send(ip, message)

import slippylib

ready = False

slippy = slippylib.SlipPy("/dev/ttyACM0")

def message(dest_address, src_address, rssi, snr, msg_id, message):
    print(f"<{src_address}> {message}")
    print(f"More Info:\n  TO: {dest_address}\n  RSSI: {rssi}\n  SNR: {snr}\n  MESSAGE ID: {msg_id}")

def error(error):
    print(f"ERROR: {error}")

def info(info):
    if info == "READY":
        global ready
        ready = True
    
    if info == "INIT":
        print("Starting SlipyMesh...")

slippy.on_message = message
slippy.on_error = error
slippy.on_info = info

while True:
    if ready: 
        ip = input("ip: ")
        message = input("message: ")
        print(f"Sending: \"{message}\" to: {ip}")
        slippy.send(ip, message)

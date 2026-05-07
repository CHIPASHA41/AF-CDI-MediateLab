import argparse
from pymodbus.client import ModbusTcpClient

parser = argparse.ArgumentParser()
parser.add_argument("--target", required=True)
args = parser.parse_args()

client = ModbusTcpClient(args.target, port=502)
client.connect()

result = client.read_holding_registers(address=10, count=1, slave=1)

if result.isError():
    print("READ FAILED")
else:
    print("READ SUCCESS:", result.registers)

client.close()

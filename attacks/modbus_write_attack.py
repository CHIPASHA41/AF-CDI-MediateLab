import argparse
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ConnectionException

parser = argparse.ArgumentParser()
parser.add_argument("--target", required=True)
parser.add_argument("--value", type=int, default=1)
args = parser.parse_args()

client = ModbusTcpClient(args.target, port=502, timeout=3)

try:
    if not client.connect():
        print("WRITE FAILED / BLOCKED: connection could not be established")
    else:
        result = client.write_register(address=10, value=args.value, slave=1)

        if result.isError():
            print("WRITE FAILED / BLOCKED")
        else:
            print("WRITE SUCCESS: register 40010 modified")

except ConnectionException:
    print("WRITE FAILED / BLOCKED: mediation layer prevented the request")

finally:
    client.close()

from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

store = ModbusSlaveContext(
    co=ModbusSequentialDataBlock(0, [0] * 100),
    hr=ModbusSequentialDataBlock(0, [0] * 100),
)

context = ModbusServerContext(slaves=store, single=True)

print("Starting Modbus TCP server on port 502...")
StartTcpServer(context=context, address=("0.0.0.0", 502))

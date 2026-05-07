#!/bin/bash

for i in {1..30}
do
    echo "Trial $i"

    e1 /home/cornelius/AF-CDI-MediateLab/venv/bin/python clients/modbus_read.py --target 10.0.0.11
    e1 /home/cornelius/AF-CDI-MediateLab/venv/bin/python attacks/modbus_write_attack.py --target 10.0.0.11

    sleep 1
done

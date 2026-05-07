# AF-CDI-MediateLab

## Architecture-First Cybersecurity for Critical Digital Infrastructure

AF-CDI-MediateLab is a Mininet/Ryu-based emulation project for evaluating architecture-first cybersecurity in IT–OT environments. The project demonstrates how a protocol-aware SDN mediation layer can preserve legitimate Modbus TCP read operations while blocking unauthorized write commands.

## Project Objective

The objective is to reproduce and validate an architecture-first cybersecurity framework for Critical Digital Infrastructure (CDI), focusing on trust-boundary mediation between enterprise IT and operational technology (OT) domains.

## Technologies Used

- Ubuntu 22.04 WSL
- Mininet
- Open vSwitch
- OpenFlow 1.3
- Ryu SDN Controller
- Python
- pyModbus
- pandas
- matplotlib

## Network Topology

The emulated topology consists of:

- 10 enterprise hosts: e1–e10
- 5 OT hosts: o1–o5
- 1 OpenFlow switch acting as the mediation layer
- 1 Ryu SDN controller

## Experiment Summary

Two architectures were tested:

### 1. Conventional Architecture

Legitimate Modbus read traffic succeeds, but unauthorized Modbus write traffic also succeeds.

Example result:

```text
READ SUCCESS: [0]
WRITE SUCCESS: register 40010 modified

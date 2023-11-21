# Network-on-Chip (NoC) Simulator

This is a cycle-accurate NoC simulator designed to study the impact of process variations on a mesh network with routers.

## Project Overview

As systems-on-chips become more complex, traditional bus-based networks are inefficient, leading to the development of network-on-chip architectures. This simulator models a 3x3 mesh NoC with routers supporting XY and YX routing, considering process variations.

## Project Structure

- `noc.py`: Main simulator code.
- `Makefile`: Build automation instructions.
- `traffic.txt`: File describing packet insertion into the NoC.
- `delays.txt`: File specifying delays for router elements.
- `Mod_Traffic.txt`: Modified traffic file (bonus feature).
- `Graph1.png`, `Graph2.png`: Graphs depicting flit transfers and latency.
- `Log_File.txt`: Log file generated by the simulator.
- `Report.txt`: Report file comparing PVS and PVA modes.
- `README.md`: Project documentation.

## Getting Started


### Running the Simulator

1. Clone the repository:

   ```bash
   git clone https://github.com/nabhrajput/CA_EPE
   cd NoC-Simulator

# Project Evaluation Deliverables

## Mid-Project Evaluation (MPE) Deliverables

1. **Simulator reads and interprets traffic file.**
2. **Simulator reads and interprets delays file.**
3. **Supports at least one routing algorithm.**
4. **Can inject packets based on the traffic file.**
5. **Generates log file for PVA mode.**
6. **Generates report file for PVA mode.**

## End-Project Evaluation (EPE) Deliverables

   During the End-Project Evaluation (EPE) phase, ensure that all initially planned features and functionalities are fully implemented. This includes addressing any aspects or components of the NoC simulator that were not completed or refined during the Mid-Project Evaluation (MPE). Consider the following tasks to fulfill this requirement:

   - **Router Components:** Verify that each router in the NoC mesh includes all necessary components, such as the crossbar, switch allocator, input buffers, and I/O ports. Ensure the proper functioning and interaction of these elements.

   - **Routing Algorithms:** Confirm that both XY routing and YX routing are fully supported, as specified in the project description. Validate that the simulator correctly interprets the chosen routing algorithm from the command line arguments.

   - **Traffic File Processing:** Ensure that the simulator accurately reads and processes the traffic file. Validate that packets (comprising header, body, and tail flits) are injected into the NoC at the specified clock cycles.

   - **Delay Handling:** Verify the simulator's ability to read delay information from the delays file. Confirm that nominal delays are applied consistently in the Process-Variation-Agnostic (PVA) mode.

   - **Simulation Modes:** Implement and test both simulation modes, i.e., Process-Variation-Agnostic (PVA) and Process-Variation-Supported (PVS). In PVS mode, ensure that delays are randomly assigned to router elements based on a Gaussian Normal Distribution, as specified.

   - **Logging and Reporting:** Validate that the simulator generates the required log file, providing a detailed account of each clock cycle's activities. Also, ensure that the report file accurately compares PVA and PVS simulation modes, highlighting any impact of process variation.

   - **Graph Generation:** Implement the generation of two types of graphs for both PVA and PVS modes: one depicting the number of flits sent over each connection and another showing packet transfer latency.
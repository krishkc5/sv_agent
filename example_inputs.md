# Example Hardware Designs to Try

## Basic Combinational Logic

### Simple Gates & Operations
- `4-bit adder with carry out`
- `8-bit subtractor`
- `4-bit AND gate`
- `2-bit XOR gate`
- `8-to-1 multiplexer`
- `3-to-8 decoder`
- `4-to-2 priority encoder`

### Arithmetic
- `4-bit multiplier`
- `8-bit comparator`
- `Absolute value circuit for 8-bit signed input`
- `Min/max finder for two 8-bit inputs`
- `Divider by 3 for 8-bit input`

### Data Processing
- `Barrel shifter for 8-bit input`
- `Leading zero counter for 8-bit input`
- `Population counter that counts 1s in an 8-bit value`
- `Parity generator for 8-bit input`
- `Gray code to binary converter`
- `Binary to Gray code converter`

### Specialized
- `7-segment display decoder for 4-bit BCD input`
- `CRC-8 calculator`
- `Hamming code encoder for 4-bit data`
- `Even parity checker`

## Sequential Logic (with clocks)

### Counters
- `2-bit counter with enable`
- `4-bit up/down counter`
- `Decade counter (0-9)`
- `Ring counter`

### State Machines
- `Traffic light controller with 3 states`
- `Vending machine controller accepting nickels and dimes`
- `Sequence detector for pattern 1011`
- `Debounce circuit for button input`

### Memory & Registers
- `4-bit shift register`
- `FIFO buffer with 4 entries`
- `8-bit register file with 4 registers`

### Communication
- `UART transmitter`
- `SPI controller`
- `I2C state machine`

## Tips

- Start simple (gates, adders, muxes)
- Combinational logic usually works on first attempt
- Sequential logic with clocks may take a few iterations
- Be specific about bit widths
- Describe expected behavior clearly

## Example Session

```bash
python3 agent.py
```

Then enter:
```
Population counter that counts the number of 1s in an 8-bit input
```

The agent will generate the design, testbench, compile, simulate, and open Surfer automatically.

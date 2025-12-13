# SV Agent

LLM-powered SystemVerilog code generator with automatic verification loop.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add your OpenAI API key from https://platform.openai.com/api-keys

## Requirements

- Python 3.7+
- Verilator (for simulation)

Install Verilator:
```bash
# macOS
brew install verilator

# Ubuntu/Debian
apt-get install verilator
```

## Usage

```bash
python agent.py
```

Enter a hardware description and the agent will generate SystemVerilog design and testbench files, then iterate until Verilator passes or max attempts reached.

## Configuration

Edit `.env`:
- `OPENAI_API_KEY` - Your OpenAI API key
- `SV_AGENT_MODEL` - Model to use (default: gpt-4o-mini)
- `SV_AGENT_MAX_ATTEMPTS` - Max iteration attempts (default: 10)

## Output

- `design.sv` - Generated hardware module
- `tb.sv` - Self-checking testbench
- `obj_dir/` - Verilator build artifacts

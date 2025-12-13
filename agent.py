import os
import subprocess
from pathlib import Path

try:
    from openai import OpenAI # type: ignore
except ImportError:  # pragma: no cover - surfaced at runtime
    OpenAI = None


def load_env_file(path: str = ".env") -> None:
    """Load environment variables from a simple .env file if one exists."""
    env_path = Path(path)
    if not env_path.is_file():
        return

    for raw_line in env_path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if (value.startswith("'") and value.endswith("'")) or (
            value.startswith('"') and value.endswith('"')
        ):
            value = value[1:-1]
        os.environ.setdefault(key, value)


def _int_from_env(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


load_env_file()

MODEL = os.environ.get("SV_AGENT_MODEL", "gpt-4o-mini")
MAX_ATTEMPTS = _int_from_env("SV_AGENT_MAX_ATTEMPTS", 10)
_client = None

BASE_PROMPT = """
Return exactly two SystemVerilog files.

FILE design.sv:
- One module named dut
- Inputs must be explicitly sized
- Output must be explicitly sized
- All intermediate math must use explicit width
- If sequential logic is needed, use always_ff with posedge clk
- Add clock and reset inputs only if sequential logic is required
- Avoid latches unless explicitly requested

FILE tb.sv:
- Must instantiate dut module
- If design has clock, generate clock with: always #5 clk = ~clk;
- If design has reset, assert reset initially then deassert
- Must be fully self-checking using assert
- Must finish simulation with $finish
- Must call $dumpfile and $dumpvars to generate VCD

Hard rules:
- Output ONLY raw SystemVerilog
- No markdown
- No commentary
- Exact format:

<DESIGN>
(code)
</DESIGN>
<TB>
(code)
</TB>
"""


def get_openai_client():
    global _client
    if _client is not None:
        return _client

    if OpenAI is None:
        raise RuntimeError(
            "The `openai` package is not installed. Run `pip install -r requirements.txt`."
        )

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Export it or add it to .env (OPENAI_API_KEY=\"...\")."
        )

    _client = OpenAI(api_key=api_key)
    return _client


def call_llm(spec, error_log):
    client = get_openai_client()
    system_prompt = BASE_PROMPT.strip()
    user_prompt = f"Spec:\n{spec.strip()}\n"
    if error_log:
        user_prompt += f"\nLast Verilator errors:\n{error_log.strip()}\n"

    try:
        response = client.chat.completions.create(
            model=MODEL,
            max_tokens=2048,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
    except Exception as exc:
        raise RuntimeError(f"OpenAI API request failed: {exc}") from exc

    text = response.choices[0].message.content if response.choices else ""
    if not text:
        raise RuntimeError("Model returned an empty response")
    return text


def extract_blocks(text):
    if "<DESIGN>" not in text or "<TB>" not in text:
        return None, None
    try:
        design = text.split("<DESIGN>")[1].split("</DESIGN>")[0].strip()
        tb = text.split("<TB>")[1].split("</TB>")[0].strip()
        return design, tb
    except Exception:
        return None, None


def run_verilator():
    subprocess.run("rm -rf obj_dir *.vcd", shell=True)

    build = subprocess.run(
        "verilator --binary -sv design.sv tb.sv --trace -Wno-EOFNEWLINE -Wno-DECLFILENAME",
        shell=True,
        capture_output=True,
        text=True,
    )

    if build.returncode != 0:
        return False, build.stderr

    sim = subprocess.run(
        "./obj_dir/Vdesign",
        shell=True,
        capture_output=True,
        text=True,
    )

    if sim.returncode != 0:
        return False, sim.stderr

    return True, ""


def open_surfer():
    vcd_files = subprocess.run(
        "ls -t *.vcd 2>/dev/null | head -1",
        shell=True,
        capture_output=True,
        text=True,
    )
    vcd_file = vcd_files.stdout.strip()
    if vcd_file:
        subprocess.Popen(["surfer", vcd_file])


def main():
    spec = input("Describe the hardware behavior: ").strip()
    error_log = ""

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"\nATTEMPT {attempt}")

        try:
            raw = call_llm(spec, error_log)
        except RuntimeError as exc:
            error_log = str(exc)
            print(error_log)
            continue

        design, tb = extract_blocks(raw)

        if design is None or tb is None:
            error_log = "Missing <DESIGN> or <TB> tags"
            print("Format failure")
            continue

        with open("design.sv", "w") as f:
            f.write(design)

        with open("tb.sv", "w") as f:
            f.write(tb)

        ok, error_log = run_verilator()

        if ok:
            print("PASS")
            open_surfer()
            return
        else:
            print("Verilator failed:")
            print(error_log)

    print("FAILED AFTER MAX ATTEMPTS")


if __name__ == "__main__":
    main()

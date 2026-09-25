#!/usr/bin/env python3
"""
Run this on your Mac where mlx_audio is installed:
    python transcribe_local.py thinkingoutloud.m4a

Or if installed via uv tool:
    uvx mlx-audio transcribe thinkingoutloud.m4a --model mlx-community/whisper-large-v3-turbo
"""
import subprocess
import sys
from pathlib import Path

def transcribe_with_mlx_audio(audio_path: str, output_path: str = None):
    """Transcribe using mlx_audio CLI"""
    audio_file = Path(audio_path)
    if not audio_file.exists():
        print(f"Error: {audio_path} not found")
        sys.exit(1)

    output = output_path or audio_file.with_suffix('.txt')

    # Try uvx first (uv tool interface)
    cmd = [
        "uvx", "mlx-audio", "transcribe",
        str(audio_file),
        "--model", "mlx-community/whisper-large-v3-turbo",
        "--output", str(output)
    ]

    print(f"Transcribing {audio_file.name}...")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Success! Output: {output}")
            print(result.stdout)
        else:
            print(f"Error: {result.stderr}")
            # Fallback: try direct mlx_audio import
            print("\nTrying direct Python import...")
            try:
                from mlx_audio.transcribe import transcribe
                text = transcribe(str(audio_file))
                Path(output).write_text(text)
                print(f"Success via Python API! Output: {output}")
            except ImportError:
                print("mlx_audio not available via Python import either")
    except FileNotFoundError:
        print("uvx not found, trying direct mlx-audio command...")
        cmd[0] = "mlx-audio"
        cmd.pop(0)  # Remove uvx
        subprocess.run(["mlx-audio", "transcribe", str(audio_file)])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe_local.py <audio_file> [output_file]")
        print("\nOr run directly:")
        print("  uvx mlx-audio transcribe thinkingoutloud.m4a")
        sys.exit(1)

    audio = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    transcribe_with_mlx_audio(audio, output)

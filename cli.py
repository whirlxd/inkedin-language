import argparse
import sys
from main import interpret

def run_file(filename):
    # only lnk files cuz that does help with language aura
    if not filename.endswith('.lnk'):
        print(f"Error: LinkedIn Language only supports .lnk files. Got: {filename}")
        print("Please use a .lnk file extension for LinkedIn Language programs.")
        return
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        print(f"--- Running: {filename} ---")
        interpret(code)
        print(f"--- Finished: {filename} ---\n")
    except FileNotFoundError:
        print(f"File not found: {filename}")

def view_code(filename):

    if not filename.endswith('.lnk'):
        print(f"Error: LinkedIn Language only supports .lnk files. Got: {filename}")
        print("Please use a .lnk file extension for LinkedIn Language programs.")
        return
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            print(f.read())
    except FileNotFoundError:
        print(f"File not found: {filename}")

def shell_mode():
    print("🔵 LinkedIn Language Interactive Shell (type 'exit' or Ctrl+C to quit)")
    buffer = ""
    prompt = "lnkdnlng> "
    while True:
        try:
            line = input(prompt)
            if line.strip() == "exit":
                print("Exiting shell.")
                break
            if line.strip() == "":
                continue
            buffer += line + "\n"
            try:
                interpret(buffer)
                buffer = ""
            except Exception as e:
                print(f"Error: {e}")
                buffer = ""
        except (KeyboardInterrupt, EOFError):
            print("\nExiting shell.")
            break

def main():
    parser = argparse.ArgumentParser(
        description="LinkedIn Language CLI - Run, view, or interact with LinkedIn Language code."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Path(s) to LinkedIn Language (.lnk) file(s) to run"
    )
    parser.add_argument(
        "--view",
        action="store_true",
        help="View the code instead of running it"
    )
    parser.add_argument(
        "--shell",
        action="store_true",
        help="Start an interactive shell"
    )
    parser.add_argument(
        "--help-cmd",
        action="store_true",
        help="Show help for LinkedIn Language CLI commands"
    )

    args = parser.parse_args()

    if args.help_cmd:
        print("""
LinkedIn Language CLI Help
--------------------------
Usage:
  python cli.py [files ...] [--view] [--shell] [--help-cmd]

Options:
  files         One or more .lnk files to run or view (ONLY .lnk extension supported)
  --view        View the code in the file(s) instead of running
  --shell       Start an interactive shell for LinkedIn Language
  --help-cmd    Show this help message

Examples:
  python cli.py myprog.lnk
  python cli.py file1.lnk file2.lnk
  python cli.py --view myprog.lnk
  python cli.py --shell

Note: Only .lnk files are supported for LinkedIn Language programs.
""")
        sys.exit(0)

    if args.shell:
        shell_mode()
        sys.exit(0)

    if not args.files:
        parser.print_help()
        sys.exit(1)

    for filename in args.files:
        if args.view:
            view_code(filename)
        else:
            run_file(filename)

if __name__ == "__main__":
    main()
    
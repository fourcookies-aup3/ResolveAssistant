import sys
import os
import time
import argparse

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from ai_agent import AIAgent
import input_control
import autonomous_engine

def main():
    parser = argparse.ArgumentParser(description="ResolveAssistant AI")
    parser.add_argument("--fully-auto", action="store_true", help="Start in fully autonomous video factory mode")
    args = parser.parse_args()

    agent = AIAgent()

    if args.fully_auto:
        autonomous_engine.start_fully_autonomous_mode()
        return

    print("--- ResolveAssistant Live Mode ---")

    # Auto-launch
    resolve_path = os.getenv("RESOLVE_PATH")
    if input_control.launch_resolve(resolve_path):
        input_control.wait_for_window()
        input_control.focus_window()
        print("Resolve is ready. Taking control...")

    print("\nWelcome! Your AI-powered video editing companion is online.")
    print("Type a command (e.g., 'create project My Movie') or 'exit' to quit.")

    while True:
        try:
            command = input("\nResolveAI (LIVE)> ")
            if command.lower() in ['exit', 'quit']:
                break

            input_control.focus_window()
            print(f"Executing: {command}...")
            response = agent.process_command(command)
            print(f"Assistant: {response}")

        except EOFError:
            break
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()

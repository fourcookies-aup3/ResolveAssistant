import sys
import os
import time

# Add src to path if running from root
sys.path.append(os.path.join(os.path.dirname(__file__)))

from ai_agent import AIAgent
import input_control

def main():
    agent = AIAgent()

    print("--- ResolveAssistant Live Mode ---")

    # Automatically launch DaVinci Resolve
    resolve_path = os.getenv("RESOLVE_PATH")
    if input_control.launch_resolve(resolve_path):
        input_control.wait_for_window()
        input_control.focus_window()
        print("Resolve is ready. Taking control...")
    else:
        print("Proceeding without automatic launch. Please ensure DaVinci Resolve is open and focused.")

    print("\nWelcome! Your AI-powered video editing companion is online.")
    print("Every command you type will be executed live on your screen.")
    print("Type a command (e.g., 'create project My Movie') or 'exit' to quit.")

    while True:
        try:
            command = input("\nResolveAI (LIVE)> ")
            if command.lower() in ['exit', 'quit']:
                break

            # Ensure window is focused before each command
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

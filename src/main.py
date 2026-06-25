import sys
import os

# Add src to path if running from root
sys.path.append(os.path.join(os.path.dirname(__file__)))

from ai_agent import AIAgent

def main():
    agent = AIAgent()
    print("Welcome to ResolveAssistant! Your AI-powered video editing companion.")
    print("Type a command (e.g., 'create project My Movie') or 'exit' to quit.")

    while True:
        try:
            command = input("ResolveAI> ")
            if command.lower() in ['exit', 'quit']:
                break

            response = agent.process_command(command)
            print(response)
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error processing command: {e}")

if __name__ == "__main__":
    main()

import watcher
import database
from database import ProcessedFile
import editor_actions
import input_control
import os
import time

def start_fully_autonomous_mode():
    """
    Fire-and-forget mode: Scans for files and edits them without user input.
    """
    print("--- STARTING FULLY AUTONOMOUS VIDEO FACTORY ---")
    print("AI is now monitoring Source folder for new footage.")

    while True:
        try:
            # 1. Check database for already processed files
            session = database.get_session()
            processed = [p.filename for p in session.query(ProcessedFile).all()]

            # 2. Scan for new files
            new_files = watcher.get_new_files(processed)

            if new_files:
                for filepath in new_files:
                    filename = os.path.basename(filepath)
                    print(f"Autonomous AI: Detected new video - {filename}")

                    if watcher.wait_for_file_ready(filepath):
                        # 3. Automation Logic
                        success = editor_actions.professional_auto_edit(
                            project_name=f"Auto_{int(time.time())}",
                            source_clips=[filepath]
                        )

                        if success:
                            # 4. Trigger Render
                            editor_actions.render_project()

                            # 5. Mark as processed
                            new_entry = ProcessedFile(filename=filename, status='completed')
                            session.add(new_entry)
                            session.commit()
                            print(f"Autonomous AI: Finished editing {filename}. Ready for next task.")
                        else:
                            print(f"Autonomous AI: Failed to edit {filename}. Retrying later.")

            session.close()

            # Wait 30 seconds before next scan
            time.sleep(30)

        except KeyboardInterrupt:
            print("Shutting down Autonomous Mode.")
            break
        except Exception as e:
            print(f"Error in Autonomous Loop: {e}")
            time.sleep(10)

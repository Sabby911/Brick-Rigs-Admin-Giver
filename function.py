import os
import configparser

# Path to your Brick Rigs folder (change this to your actual game folder)
BRICKRIGS_FOLDER = r"C:\Path\To\Brick Rigs"
ADMIN_FILE = os.path.join(BRICKRIGS_FOLDER, "admin.ini")

def grant_admin(target: str) -> bool:
    """
    Grants admin in Brick Rigs by creating/updating admin.ini in the game folder.
    target: username or Steam64ID
    Returns True if successful, False otherwise.
    """
    try:
        # Create the Brick Rigs folder if it doesn't exist
        if not os.path.exists(BRICKRIGS_FOLDER):
            os.makedirs(BRICKRIGS_FOLDER)

        # Use ConfigParser to manage INI file
        config = configparser.ConfigParser()

        # If the file exists, read it
        if os.path.exists(ADMIN_FILE):
            config.read(ADMIN_FILE)

        # Ensure a section exists for admins
        if not config.has_section("Admins"):
            config.add_section("Admins")

        # Add the target admin
        if config.has_option("Admins", target):
            print(f"{target} is already an admin.")
        else:
            config.set("Admins", target, "true")
            with open(ADMIN_FILE, "w") as f:
                config.write(f)
            print(f"Admin granted to {target} in admin.ini.")

        return True

    except Exception as e:
        print(f"Error granting admin: {e}")
        return False

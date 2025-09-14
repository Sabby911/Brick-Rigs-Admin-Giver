import os
import configparser

# Path to your Brick Rigs folder
BRICKRIGS_FOLDER = r"C:\Path\To\Brick Rigs"  # CHANGE THIS to your actual folder
ADMIN_FILE = os.path.join(BRICKRIGS_FOLDER, "admin.ini")

def grant_admin(target: str) -> bool:
    """
    Grants admin in Brick Rigs by creating/updating admin.ini
    target: username or Steam64ID
    Returns True if successful, False otherwise.
    """
    try:
        # Make sure the Brick Rigs folder exists
        if not os.path.exists(BRICKRIGS_FOLDER):
            os.makedirs(BRICKRIGS_FOLDER)

        # ConfigParser to manage INI file
        config = configparser.ConfigParser()

        # Read the file if it exists
        if os.path.exists(ADMIN_FILE):
            config.read(ADMIN_FILE)

        # Ensure section exists
        if not config.has_section("Admins"):
            config.add_section("Admins")

        # Add target to admins
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

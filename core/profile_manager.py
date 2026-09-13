import json
import os


def get_profile_path(profile_folder, profile_name):
    """
    Create the file path for a profile.
    """

    file_name = profile_name.strip().replace(" ", "_") + ".json"

    return os.path.join(profile_folder, file_name)


def save_profile(profile_folder, profile_name, profile_data):
    """
    Save a profile as a JSON file.
    """

    os.makedirs(profile_folder, exist_ok=True)

    file_path = get_profile_path(profile_folder, profile_name)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(profile_data, file, indent=4)

    return file_path


def load_profile(profile_folder, profile_name):
    """
    Load a saved profile.
    """

    file_path = get_profile_path(profile_folder, profile_name)

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def list_profiles(profile_folder):
    """
    Return all saved profile names.
    """

    if not os.path.exists(profile_folder):
        return []

    profiles = []

    for file_name in os.listdir(profile_folder):

        if file_name.endswith(".json"):
            profile_name = file_name[:-5]
            profile_name = profile_name.replace("_", " ")
            profiles.append(profile_name)

    return profiles


def delete_profile(profile_folder, profile_name):
    """
    Delete a saved profile.
    """

    file_path = get_profile_path(profile_folder, profile_name)

    if os.path.exists(file_path):
        os.remove(file_path)
        return True

    return False
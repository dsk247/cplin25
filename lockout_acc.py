import os

def modify_common_auth():
    file_path = "/etc/pam.d/common-auth"
    temp_file_path = file_path + ".tmp"

    # does file exist?
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return

    try:
        with open(file_path, "r") as original_file:
            lines = original_file.readlines()

        # is the required line present?
        required_line = "auth    required                        pam_tally2.so deny=5 unlock_time=300 onerr=fail\n"
        if required_line not in lines:
            lines.insert(0, required_line)

        # change lines that have pam_tally2.so
        for i, line in enumerate(lines):
            if "pam_tally2.so" in line and "deny=" not in line:
                lines[i] = line.strip() + " deny=5 unlock_time=1800 onerr=fail\n"

        # write changes to a temporary file
        with open(temp_file_path, "w") as temp_file:
            temp_file.writelines(lines)

        # replace the original file with the modified one
        os.replace(temp_file_path, file_path)
        print(f"Modified {file_path} successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

if __name__ == "__main__":
    modify_common_auth()

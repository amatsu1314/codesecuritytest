import os
import stat

def vulnerable_insecure_file_permissions():
    """
    CWE-732: Insecure File Permissions
    INTENTIONAL_VULNERABILITY (TEST ONLY)
    """
    filename = "insecure.txt"
    with open(filename, "w") as f:
        f.write("test data")

    # ✗ 脆弱: 誰でも読み書きできる 777
    os.chmod(filename, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    print(f"[CWE-732] Created file with insecure permissions: {filename}")


def vulnerable_information_exposure():
    """
    CWE-200: Information Exposure
    INTENTIONAL_VULNERABILITY (TEST ONLY)
    """
    try:
        1 / 0
    except Exception as e:
        # ✗ 脆弱: 内部パスや例外をそのまま表示
        print("[CWE-200] Error occurred:", e)




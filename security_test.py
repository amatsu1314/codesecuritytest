#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security Scanner Test Script (Python)
------------------------------------
このスクリプトは、セキュリティスキャナ（Trend Micro Code Security 等）の検証用です。
以下を含みます：
  - EICAR テスト文字列の動的生成（eicar.com を作成）
  - 意図的な脆弱サンプル（SAST 検証目的）
    * CWE-78: OS Command Injection
    * CWE-89: SQL Injection
    * CWE-94/95: Code/Eval Injection
    * CWE-798: Hard-coded Secrets
    * CWE-327: Weak Hash (MD5)

"""

import base64
import hashlib
import os
import sqlite3
import sys

# --------------------------
# EICAR: 動的生成（改行なし）
# --------------------------
# EICAR テスト文字列（ASCII, 改行なし）
_EICAR_ASCII = "X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
# Base64（参考：ときどき平文検出を避けたい環境向けに）
_EICAR_B64 = "WDVPIVAlQEFQWzRcUFpYNTQoUF4pN0NDKTd9JEVJQ0FSLVNUQU5EQVJELUFOVElWSVUtVEVTVC1GSUxFISRIK0gq"

def generate_eicar(output_path: str = "eicar.com", use_base64: bool = False):
    """
    use_base64=True の場合、Base64 からデコードして書き出します。
    """
    if use_base64:
        data = base64.b64decode(_EICAR_B64)
    else:
        data = _EICAR_ASCII.encode("ascii")

    with open(output_path, "wb") as f:
        f.write(data)
    print(f"[EICAR] Generated: {output_path} ({len(data)} bytes)")

# ------------------------------------------
# 以下、意図的な脆弱コード（SAST 検証用）
# ------------------------------------------

# CWE-798: Hard-coded Secrets（テスト用にあえて埋め込み）
HARDCODED_API_KEY = "AKIA-TEST-EXAMPLE-KEY"  # INTENTIONAL_VULNERABILITY (TEST ONLY) - CWE-798

def weak_hash_md5(s: str) -> str:
    """
    CWE-327: 弱いハッシュ関数の使用例（MD5）
    INTENTIONAL_VULNERABILITY (TEST ONLY) - CWE-327
    """
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def vulnerable_command_injection(user_input: str):
    """
    CWE-78: OS Command Injection
    INTENTIONAL_VULNERABILITY (TEST ONLY) - Do NOT use this pattern in production.
    例: user_input = "127.0.0.1; echo injected"
    """
    cmd = f"ping -c 1 {user_input}"
    print("[CWE-78] Executing:", cmd)
    # 実行したくない場合はコメントアウトしてください
    os.system(cmd)


def vulnerable_sql_injection(user_input: str):
    """
    CWE-89: SQL Injection
    INTENTIONAL_VULNERABILITY (TEST ONLY)
    """
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()
    cur.execute("CREATE TABLE users(name TEXT, password TEXT)")
    cur.execute("INSERT INTO users VALUES('admin','secret')")

    # 脆弱: 文字列連結でクエリ構築
    query = f"SELECT * FROM users WHERE name = '{user_input}'"
    print("[CWE-89] Query:", query)
    try:
        for row in cur.execute(query):
            print("[CWE-89] Row:", row)
    except Exception as e:
        print("[CWE-89] Exception:", e)
    finally:
        conn.close()


def vulnerable_eval(code_str: str):
    """
    CWE-94/95: 任意コード実行 / eval の使用
    INTENTIONAL_VULNERABILITY (TEST ONLY)
    例: code_str = "__import__('os').name"
    """
    print("[CWE-94/95] Evaluating:", code_str)
    try:
        result = eval(code_str)  # 脆弱：外部入力をそのまま eval
        print("[CWE-94/95] Result:", result)
    except Exception as e:
        print("[CWE-94/95] Exception:", e)


def main():
    """
    使い方:
      python3 security_test.py                 # 何もせず説明を表示
      python3 security_test.py eicar           # eicar.com を生成
      python3 security_test.py eicar_b64       # Base64 から生成
      python3 security_test.py cmd "<input>"   # コマンドインジェクション例を実行
      python3 security_test.py sql "<input>"   # SQLインジェクション例を実行
      python3 security_test.py eval "<code>"   # eval 脆弱例を実行
      python3 security_test.py md5 "<text>"    # 弱いハッシュ例（MD5）
    """
    if len(sys.argv) < 2:
        print(main.__doc__)
        return

    action = sys.argv[1].lower()

    if action == "eicar":
        generate_eicar("eicar.com", use_base64=False)
    elif action == "eicar_b64":
        generate_eicar("eicar.com", use_base64=True)
    elif action == "cmd":
        user_input = sys.argv[2] if len(sys.argv) > 2 else "127.0.0.1; echo injected"
        vulnerable_command_injection(user_input)
    elif action == "sql":
        user_input = sys.argv[2] if len(sys.argv) > 2 else "admin'--"
        vulnerable_sql_injection(user_input)
    elif action == "eval":
        code_str = sys.argv[2] if len(sys.argv) > 2 else "2 + 2"
        vulnerable_eval(code_str)
    elif action == "md5":
        text = sys.argv[2] if len(sys.argv) > 2 else "password"
        print("[CWE-327] MD5:", weak_hash_md5(text))
    else:
        print("[!] Unknown action:", action)
        print(main.__doc__)


if __name__ == "__main__":
    main()

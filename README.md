# Security Scanner Test (Python)

> ⚠️ このリポジトリはセキュリティスキャナ検証専用です。  
> EICAR の生成と、意図的な脆弱コード（CWEタグ付き）を含みます。  
> 本番利用や共有環境への持ち込みは禁止。

## 使い方
```bash
python3 security_test.py eicar        # EICAR 生成
python3 security_test.py sql "admin'--"
python3 security_test.py cmd "127.0.0.1; echo injected"
python3 security_test.py eval "2+2"
python3 security_test.py md5 "password"

import os
import sys
from typing import Any, Dict

import snowflake.connector


def get_env(name: str, required: bool = True, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if required and (value is None or value == ""):
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value or ""


def build_connection_params() -> Dict[str, Any]:
    return {
        "account": get_env("SNOWFLAKE_ACCOUNT"),
        "user": get_env("SNOWFLAKE_USER"),
        "password": get_env("SNOWFLAKE_PASSWORD"),
        "warehouse": get_env("SNOWFLAKE_WAREHOUSE", required=False),
        "database": get_env("SNOWFLAKE_DATABASE", required=False),
        "schema": get_env("SNOWFLAKE_SCHEMA", required=False),
        "role": get_env("SNOWFLAKE_ROLE", required=False),
    }


def main() -> None:
    try:
        params = build_connection_params()
        with snowflake.connector.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute("select * from demo.public.test limit 10")
                rows = cur.fetchall()
                colnames = [c[0] for c in cur.description]

        # Print as TSV for easy copy
        print("\t".join(colnames))
        for row in rows:
            print("\t".join(str(v) if v is not None else "" for v in row))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


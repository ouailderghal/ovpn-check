#!/usr/bin/env python3

import argparse
import OpenSSL
import re
import sys

from datetime import datetime, timedelta

def get_args() -> argparse.Namespace:
    _prog: str = "OpenVPN Expiration Checker"
    _description: str = "Checks for the expiration date of an OpenVPN profile"

    parser = argparse.ArgumentParser(prog=_prog, description=_description)
    parser.add_argument("profile", help="Path to OpenVPN profile")
    args: argparse.Namespace = parser.parse_args()
    return args

def read_profile(path: str) -> str:
    try:
        with open(path, "r") as profile_file:
            profile: str = profile_file.read()
            if not profile.strip():
                raise ValueError(f"The file at '{path}' is empty.")
            return profile
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at '{path}' does not exist.")
    except PermissionError:
        raise PermissionError(f"Permission denied: Unable to read the file at '{path}'.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading '{path}': {e}")

def main() -> None:
    args = get_args()

    profile: str = read_profile(args.profile)
    regex_cert: re.Pattern = re.compile("<cert>(.*)</cert>", re.IGNORECASE|re.DOTALL)
    match_cert: re.Match | None = regex_cert.search(profile)

    if not match_cert:
        print(f"[ERR] Could not parse certificate from {args.profile} profile")
        sys.exit(1)

    cert: str = match_cert.group(1)
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    expiration_date_from_cert: str = x509.get_notAfter().decode("utf-8")
    expiration_timestamp: datetime = datetime.strptime(expiration_date_from_cert, "%Y%m%d%H%M%SZ")
    time_delta: timedelta = expiration_timestamp - datetime.now()
    print(f"[INFO] VPN certificate expires on {expiration_timestamp.strftime('%d/%m/%Y at %H:%M:%S')} in {time_delta.days} days")

if __name__ == "__main__":
    main()

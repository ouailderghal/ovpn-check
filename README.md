# OpenVPN Expiration Checker

A Python script to check the expiration date of an OpenVPN profile's certificate and notify the user if the expiration is within a configurable warning period.

## Features
- Parses an OpenVPN profile to extract the certificate expiration date.
- Sends a desktop notification if the certificate is about to expire (default: 7 days before expiration).
- Provides a clear summary of the certificate's expiration status.

## Requirements
- Python 3.9+
- `openssl` library
- Desktop environment supporting `notify-send`

## Usage
Run the script with the path to your OpenVPN profile:
```bash
python3 ovpn-check.py /path/to/your.ovpn
```

If the certificate is nearing expiration (within 7 days by default), the script will:
- Send a desktop notification (using `notify-send`).
- Print the expiration details to the standard output.

## Configuration
To adjust the warning period, modify the `LIMIT_BEFORE_WARNING_DAYS` constant in the script:
```python
LIMIT_BEFORE_WARNING_DAYS: int = 7
```

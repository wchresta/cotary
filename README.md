# cotary
Cotary allows you to prove that you have a document without releasing it.

# Installation
Make sure you have the python requirements installed given in `requirements.txt`.

This can be achieved using pip (omit `--user` to install it system-wide).
```
$ pip install --user -r reqirements.txt
```

Then make `./cotary` executable and execute it:
```
$ chmod +x cotary
$ ./cotary -h
```

# Configuration
Configuration of Twitter APIs is done using a yaml config file.
At the moment, these are the options. Default config file is in `~/.config/cotary/config.yaml`.

```yaml
twitter:
    message: 
        'I own a file with checksum {checksum} (cotary)'
    consumer:
        key: xyz
        secret: abcd
    access_token:
        key: 123
        secret: 7890
```

# Usage
```
usage: cotary.py [-h] [-c] [--config [CONFIG]] [-q] [file]

Publish the checksum of a file on Twitter.

positional arguments:
  file               File for which to publish checksum. If none is given,
                     read from stdin

optional arguments:
  -h, --help         show this help message and exit
  -c, --calc_only    Only calculate and print the checksum, do not publish it
  --config [CONFIG]  Use given config instead of ~/.local/cotary/config.yaml
  -q, --quiet        Do not print any messages
```

# Example

```
$ ./cotary README.md 
checksum: openssl_sha256:66ca5ae6f1f3760ad7258cc1d1e906ec8853a0e4da2b2de42f55036cffe8f8a2
Status published at 2019-01-16 15:18:38
```

Leads to this Twitter message:


![I own a file with checksum openssl\_sha256:66ca5ae6f1f3760ad7258cc1d1e906ec8853a0e4da2b2de42f55036cffe8f8a2 (cotary)](screenshot.png)

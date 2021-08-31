# kcatreplay
Replay events on kafkatopic easily.

To install: 
1. Clone this repository
2. `bash ./install.sh`

```
usage: kcatreplay [-h] [-c CONFIG_FILE] -t TOPIC [-K KEY_DELIMITER] [--skip-verification] [-d] input_file

positional arguments:
  input_file

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        defaults to "dev.conf"
  -t TOPIC, --topic TOPIC
  -K KEY_DELIMITER, --key-delimiter KEY_DELIMITER
  --skip-verification   skip checking validity of kafka events in input file
  -d, --dry-run         do not actually replay event, useful to check if input file will pass validation.
```

Note that topic is _not_ optional.

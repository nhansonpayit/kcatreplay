#!/usr/bin/env python3
import os.path
import re
from argparse import ArgumentParser
import subprocess
from subprocess import CalledProcessError


def kafkacat_replay(input_file, config_file, topic, key_delimiter):
    input_file_path = os.path.abspath(input_file)
    mounted_temp_file = '/mnt/kafka_events.tmp'
    os.environ['KAFKACAT_DOCKER_OPTS'] = f'-v {input_file_path}:{mounted_temp_file}'
    return subprocess.run(['kafkacat',
                           '-q',
                           '-P',
                           '-K', key_delimiter,
                           '-F', config_file,
                           '-t', topic,
                           '-l', mounted_temp_file,
                           ]).returncode


def input_file_valid(input_filename, key_delimiter):
    pattern = key_delimiter.join(
        [r'^[a-fA-F\d]{8}-[a-fA-F\d]{4}-[a-fA-F\d]{4}-[a-fA-F\d]{4}-[a-fA-F\d]{12}', r'{.*}$'])
    valid_kafka_record = re.compile(pattern)
    with open(input_filename, mode='r') as infile:
        for line in infile:
            if not valid_kafka_record.match(line):
                return False
    return True


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-c', '--config-file', default='dev.conf', help='defaults to "dev.conf"')
    parser.add_argument('-t', '--topic', required=True)
    parser.add_argument('-K', '--key-delimiter', default=';')
    parser.add_argument('--skip-verification', action='store_true', help='''skip checking validity of kafka events in \
input file''')
    parser.add_argument('-d', '--dry-run', action='store_true', help='''do not actually replay event, useful to check \
if input file will pass validation.''')
    parser.add_argument('input_file')

    args = parser.parse_args()

    try:
        subprocess.check_output(['hash', 'kafkacat'])
    except CalledProcessError:
        parser.exit(status=1, message='''No kafkacat executable found.''')

    if not args.skip_verification:
        if not input_file_valid(args.input_file, args.key_delimiter):
            parser.exit(status=1, message='''Input file does not appear to contain valid kafka events. Be sure you are
including the key when generating your input file with kafkacat, i.e. use the -K option.''')

    if args.dry_run:
        exit(0)

    exit(kafkacat_replay(args.input_file, args.config_file, args.topic, args.key_delimiter))

#!/usr/bin/env python3
"""Get information about the ISS and its current position."""

import argparse
import sys
from iss_email import Email
from iss import ISS

iss = ISS()
email = Email()

LOGO = """
  _____  _____ _____ 
 |_   _|/ ____/ ____|
   | | | (___| (___  
   | |  \___ \\___  \ 
  _| |_ ____) |___) |
 |_____|_____/_____/ 
                                          
"""


def send_notification(latitude, longitude) -> int:
    """Send an email if the ISS is overhead and it is nighttime."""
    if iss.is_iss_overhead(latitude, longitude) and iss.is_night(latitude, longitude):
        email.send_notification()
        return 0
    return 1


def main(argv=None) -> int:
    """Entrypoint for ISS notifier."""
    print(LOGO)
    # Create the parser
    description = 'Check if the ISS is overhead!'
    job_options = argparse.ArgumentParser(description=description)

    # Add the arguments
    job_options.add_argument('--configure',
                             default=False,
                             action='store_true',
                             help='Configure an email address.')
    job_options.add_argument('-l',
                             '--list',
                             default=False,
                             dest='people',
                             action='store_true',
                             help='List out the personal currently aboard the ISS.')
    job_options.add_argument('-c',
                             '--check',
                             default=False,
                             action='store_true',
                             help='Check if the ISS is overhead.')
    job_options.add_argument('-n',
                             '--notify',
                             default=False,
                             action='store_true',
                             help='Send an email notification.')
    job_options.add_argument('-o',
                             '--open',
                             default=False,
                             dest='browser',
                             action='store_true',
                             help='Open a map and see the current location of the ISS.')
    job_options.add_argument('-t',
                             '--latitude',
                             default=False,
                             action='store',
                             help='Provide a latitude to check.')
    job_options.add_argument('-g',
                             '--longitude',
                             default=False,
                             action='store',
                             help='Provide a longitude to check.')
    args = job_options.parse_args(argv)

    configure = args.configure
    people = args.people
    check = args.check
    notify = args.notify
    browser = args.browser
    latitude = float(args.latitude)
    longitude = float(args.longitude)

    if configure:
        email.configure()
    elif browser:
        iss.iss_current_location()
    elif people:
        people = iss.people_aboard()
        for person in people:
            print(person)
        return 0
    else:
        print("Must provide a latitude and longitude.")
        return 1

    if check:
        if iss.is_iss_overhead(latitude, longitude):
            print("Yes!")
        else:
            print("No...Sorry.")
        return 0
    if notify:
        send_notification(latitude, longitude)
    return 0


if __name__ == "__main__":
    sys.exit(main())

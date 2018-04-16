#!/usr/bin/env python
# -*- coding: utf_8 -*-

import nmap


def main():
    nmapScan = nmap.PortScannerAsync()
    nmapScan.scan(hosts='127.0.0.1', arguments='-sS -Pn -n --open -p 21,22,135,139,445', callback=callback_result)
    while nmapScan.still_scanning():
        print("[*]Waiting")
        nmapScan.wait(2)
    print("[*]Complete")


def callback_result(host, scan_result):
    print '-' * 60
    print host, scan_result


if __name__ == '__main__':
    main()

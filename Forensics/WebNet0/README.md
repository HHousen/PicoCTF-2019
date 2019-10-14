# WebNet0

## Problem

> We found this packet capture and key. Recover the flag. You can also find the file in /problems/webnet0_0_363c0e92cf19b68e5b5c14efb37ed786.

* [Packet Capture](./capture.pcap)
* [Key](./picopico.key)

## Solution

1. Open in Wireshark
2. Go to Edit > Preferences > Protocols > TLS > RSA keys list
3. Add the key to the list (don't worry about ip and other columns)
4. Flag is in decrypted TLS section of the now visible HTTP packets
```
HTTP/1.1 200 OK
Date: Fri, 23 Aug 2019 15:56:36 GMT
Server: Apache/2.4.29 (Ubuntu)
Last-Modified: Mon, 12 Aug 2019 16:50:05 GMT
ETag: "5ff-58fee50dc3fb0-gzip"
Accept-Ranges: bytes
Vary: Accept-Encoding
Content-Encoding: gzip
*Pico-Flag: picoCTF{nongshim.shrimp.crackers}*
Content-Length: 821
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html
```

### Flag

`picoCTF{nongshim.shrimp.crackers}`
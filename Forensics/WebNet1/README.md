# WebNet1

## Problem

> We found this packet capture and key. Recover the flag. You can also find the file in /problems/webnet1_0_d63b267c607b8fedbae100068e010422.

* [Packet Capture](./capture.pcap)
* [Key](./picopico.key)

## Solution

1. Open in Wireshark
2. Go to Edit > Preferences > Protocols > TLS > RSA keys list
3. Add the key to the list (don't worry about ip and other columns)
4. Flag is in JPEG JFIF packet Reassembled SSL section

```
TTP/1.1 200 OK
Date: Fri, 23 Aug 2019 16:27:04 GMT
Server: Apache/2.4.29 (Ubuntu)
Last-Modified: Fri, 23 Aug 2019 16:26:33 GMT
ETag: "112fb-590cb44f2cbe6"
Accept-Ranges: bytes
Content-Length: 70395
Pico-Flag: picoCTF{this.is.not.your.flag.anymore}
Keep-Alive: timeout=5, max=99
Connection: Keep-Alive
Content-Type: image/jpeg

ÿØÿàJFIFÿáExifMM*JR(;ZpicoCTF{honey.roasted.peanuts}ÿâICC_PROFILElcmsmntrRGB XYZ Ü)9acspAPPLöÖÓ-lcms
```

### Flag

`picoCTF{honey.roasted.peanuts}`
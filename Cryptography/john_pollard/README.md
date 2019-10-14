# john_pollard

## Problem

> Sometimes RSA certificates are breakable

* [Certificate](./cert)

## Solution

1. Decode the RSA certificate at <https://8gwifi.org/PemParserFunctions.jsp> or <https://www.sslchecker.com/certdecoder>
2. Find the modulus value in the decoded certificate: `Modulus: 4966306421059967 (0x11a4d45212b17f)`
3. Use Yafu to factor into p and q: `factor(0x11a4d45212b17f)`

### Flag

`picoCTF{73176001,67867967}`

from pwn import *
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    return x % m

c=9269536699699265669063996876183449426013023677812466440967814837350617037900282049804005999606452069607905278585144126284214604776352007320206242204584678688193210013471159890997627680894954392533996753013235462393207156304765379157505543533999626350532305370043389542585404146727701112755189936869897137546125841974367010960937950133678397726 
n=53023048477898510482458653811989372419218837371063796289274915809338617743188682925802500284507148707878032855317656447646692819864000830091917098096680351826491670941475242192145621534512908814094787326864206640218221584804721345600283196760492110735337736483640934843900303550921096343394960797997930911828100786536812962014994852325098611681 
e=65537
# found using website called factor integer calculator
phi=53023048335246805045263902588277367243733349787523896861318320379844306217894137393307492110281545353482791830787759811990757076441455478676561380339536463963148230377730560633862349756925674479178326659697115611873713605510278346046421297996353347316312417563100454746195357154805237797895779329168041136568228904743245266997477376000000000000

d=modinv(e, phi)
m=pow(c, d, n)
print (m)

print(hex(m))


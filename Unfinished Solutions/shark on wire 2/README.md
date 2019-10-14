Problem:
We are given another packet capture. Find the flag.

Solution:
This problem was difficult in that the way the flag was stored was very arbitrary.
Digging through the data, we notice two very interesting packets:

![](https://github.com/bleh05/pico19writeup/blob/master/shark%20on%20wire%202/start.png)

![](https://github.com/bleh05/pico19writeup/blob/master/shark%20on%20wire%202/end.png)

From here it's just trial and error. We notice that the two packets have the same destination port, port 22.
We filter by this port in the top bar that says "Apply a display filter". This gives us a particular conversation:
udp.dstport==22
![](https://github.com/bleh05/pico19writeup/blob/master/shark%20on%20wire%202/udpdstport.png)


The info bar is giving us the source port, the destination port, and the length of the data. The source ports look very interesting.
Turns out, if we take all the source ports, subtract 5000 from all of them, and then plot their corresponding ASCII values, we get the flag.
For example, the first source port(after the "start" packet) is 5112. 5112 - 5000 = 112, which corresponds to an ASCII value of 'p'.
Then, 5105 corresponds to 'i'.
Then, 5099 = 'c'.
5111 = 'o'.
If we continue doing this, we get the flag: picoCTF{p1LLf3r3d_data_v1a_st3g0}

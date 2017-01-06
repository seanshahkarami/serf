# serf
serf is a utility for bridging a TCP/IP connection over a serial connection.

After a lot of searching, more classic methods such as PPP or SLIP just weren't working with my configuration. I decided to hack together something that could be deployed using nothing more than a minicom or screen session.

Maybe this whole thing is better designed as a listener while gives up after
getting a connection to a piper + encoding filter.

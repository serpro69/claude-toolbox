# Evidence capture retry

The first editor completed, but its saved prompt file contained two trailing
newlines while the dispatched plaintext had one. Although the submitted plaintext
also appeared in the coordinator's pre-dispatch output, the required saved-file
hash did not identify identical bytes. This attempt is invalid for acceptance.
Its complete editor trace and resulting artifact remain here.

The fixture was restored byte-for-byte from `../before/`. A fresh editor reruns
the same current canonical instructions and unchanged eval request with a prompt
file read and hashed before dispatch and identical submitted bytes. This is an
evidence capture retry, not an observed behavioral failure.

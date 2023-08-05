# desktop-encrypt

very simple tool to encrypt/decrypt folders on the desktop utilizing ecies

## Install

`pip3 install desktop-encrypt`

prerequisites: python 3; xcode (OS X)

for more detailed information about installation see [here](https://0000000000.org/desktop-encrypt/)

## Usage

Once installed there are only three simple commands available at any command line:

#### desktop-keygen

`desktop-keygen`

Executing this command derives a public key from two passphrases (you will prompted to enter the passphrases).

#### desktop-lock

`desktop-lock <name of folder>`

Executing this command will take a folder on the desktop and "lock" it leaving only an encrypted file on the desktop. It will prompt you for an encryption key (a public key in standard DER format, as in the output of `dekstop-keygen`).

**IMPORTANT: The folder on the desktop is destroyed and only the encryption remains with this command. Verify the encryption key you use (that you or whoever you are communicating with actually has the decryption key) before locking the folder or you could lock yourself out of your data forever!**

#### desktop-unlock

`desktop-unlock <name of encrypted file>`

Executing this command will take an encrypted file on the desktop and decrypt it leaving a zip of your folder on the desktop.
You will be prompted for the two decryption passphrases. Only the passphrases corresponding to the exact encryption key used will be able to decrypt the file.


`

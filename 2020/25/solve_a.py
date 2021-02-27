#!/usr/bin/env python3
def transformation(subject_num, loop_size):
    """
    This is the transformation that is used to get a public key
    from a subject number and a loop size, or to get an encryption
    key from a public key and a loop size.
    """
    value = 1
    for i in range(loop_size):
        value = value * subject_num
        value = value % 20201227

    return value


def find_loop_size(subject_num, pub_key):
    """
    Given a subject number and a public key, find the loop size that
    produces the given encryption key.
    """
    result = 1
    loop_size = 0
    while result != pub_key:
        result = result * subject_num
        result = result % 20201227
        loop_size = loop_size + 1
        
    return loop_size


def main():
    pub_key1 = 12320657
    pub_key2 = 9659666

    subj_num = 7
    loop_size1 = find_loop_size(subj_num, pub_key1)
    loop_size2 = find_loop_size(subj_num, pub_key2)
    
    print('Loop size 1 is {0}'.format(loop_size1))
    print('Loop size 2 is {0}'.format(loop_size2))

    # Now we have the public key and loop size of device 1 and device 2.
    # We will use device 1's public key as the subject number and device 2's
    # loop size to get the encryption key. We will validate it by doing
    # the same using device 2's public key as the subject number and device
    # 1's loop size. The encryption keys should turn out to be the same.
    enc_key1 = transformation(pub_key1, loop_size2)
    enc_key2 = transformation(pub_key2, loop_size1)
    print('Encryption keys should match: {0} & {1}'.format(enc_key1, enc_key2))
    

if __name__ == '__main__':
    main()

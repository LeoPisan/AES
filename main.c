#include <stdio.h>
#include <stdlib.h>

#include "rijndael.h"

void print_block(unsigned char *block, aes_block_size_t block_size) {
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            unsigned char value = block_access(block, i, j, block_size);

            // Print spaces before small numbers to ensure that everything is aligned
            // and looks nice
            if (value < 10) printf(" ");

            if (value < 100) printf(" ");

            printf("%d", value);
        }
        printf("\n");
    }
}

int main() {
    unsigned char plaintext[16] = {
        1, 2, 3, 4, 5, 6, 7, 8,
        9, 10, 11, 12, 13, 14, 15, 16
    };
    unsigned char key[16] = {
        50, 20, 46, 86, 67, 9, 70, 27,
        75, 17, 51, 17, 4, 8, 6, 99
    };

    unsigned char *ciphertext = aes_encrypt_block(plaintext, key, AES_BLOCK_128);
    unsigned char *recovered_plaintext = aes_decrypt_block(ciphertext, key, AES_BLOCK_128);

    printf("############ ORIGINAL PLAINTEXT ###########\n");
    print_block(plaintext, AES_BLOCK_128);

    printf("\n\n################ CIPHERTEXT ###############\n");
    print_block(ciphertext, AES_BLOCK_128);

    printf("\n\n########### RECOVERED PLAINTEXT ###########\n");
    print_block(recovered_plaintext, AES_BLOCK_128);

    free(ciphertext);
    free(recovered_plaintext);

    return 0;
}

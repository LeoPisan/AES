/*
 * TODO: Add your name and student number here, along with
 *       a brief description of this code.
 */

#ifndef RIJNDAEL_H
#define RIJNDAEL_H

typedef enum {
  AES_BLOCK_128,
  AES_BLOCK_256,
  AES_BLOCK_512
} aes_block_size_t;

unsigned char block_access(unsigned char *block,
                           size_t row, size_t col,
                           aes_block_size_t block_size);

/*
 * These should be the main encrypt/decrypt functions (i.e. the main
 * entry point to the library for programmes hoping to use it to
 * encrypt or decrypt data)
 */
unsigned char *aes_encrypt_block(
    unsigned char *plaintext,
    unsigned char *key,
    aes_block_size_t block_size);
unsigned char *aes_decrypt_block(
    unsigned char *ciphertext,
    unsigned char *key,
    aes_block_size_t block_size);

#endif

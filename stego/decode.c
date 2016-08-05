#include <stdio.h>
#include <string.h>
#include <math.h>
#include "cdjpeg.h"       /* Common decls for jpeg files */

// adapted from code from: http://www.cs.odu.edu/~cs772/demos/steganography/sshettyLinux/
//USAGE: ./decode <watermarkedimage> <decodedmessage>

#define MAX_MSG_BITS 132000
#define MAX_MSG_BYTES 33000

void JPEG_extractbits( const char * input_filename, char **message, size_t *message_len) { // returns a null-terminating string that must be freed
  struct jpeg_decompress_struct srcinfo;
  struct jpeg_error_mgr jsrcerr, jdsterr;
  jvirt_barray_ptr *coef_arrays;
  JDIMENSION i, compnum, rownum, blocknum;
  size_t block_row_size;
  JBLOCKARRAY row_ptrs[MAX_COMPONENTS];

  FILE * input_file;

  char mask[MAX_MSG_BITS];
  char * decode_int = calloc( MAX_MSG_BYTES, sizeof(char)); 

  int text = 0, length, length_set = 0, data_set = 0 , count_bits = 0, test_mask = 0, l = 0;
  int get_a = 0, get_b = 0, val_a = 0, val_b = 0;

  srcinfo.err = jpeg_std_error(&jsrcerr);
  jpeg_create_decompress(&srcinfo);
  jsrcerr.trace_level = jdsterr.trace_level;

  input_file = fopen(input_filename, "rb");

  jpeg_stdio_src(&srcinfo, input_file);
  (void) jpeg_read_header(&srcinfo, TRUE);

  coef_arrays = jpeg_read_coefficients(&srcinfo);
  for (compnum = 0; compnum < srcinfo.num_components; compnum++)
  {
    block_row_size = (size_t) SIZEOF(JCOEF) * DCTSIZE2
                     * srcinfo.comp_info[compnum].width_in_blocks;
    for (rownum = 0; rownum < srcinfo.comp_info[compnum].height_in_blocks; rownum++)
    {
      int k , l, j;
      row_ptrs[compnum] = ((&srcinfo)->mem->access_virt_barray)
                          ((j_common_ptr) &srcinfo, coef_arrays[compnum],
                           rownum, (JDIMENSION) 1, FALSE);
      for (blocknum = 0; blocknum < srcinfo.comp_info[compnum].width_in_blocks;
           blocknum++)
      {
        k = -1; l = 0;
        for (i = 0; i < DCTSIZE2; i++)
        {
          if (!length_set)
          {
            if ( (i > 0  )  && ( row_ptrs[compnum][0][blocknum][i] != 0) && (abs(row_ptrs[compnum][0][blocknum][i]) > 15))
            {
              int test_amask = 0x08, k = 0;
              int test = abs (row_ptrs[compnum][0][blocknum][i]);
              if (get_a == 1 && get_b == 1 )
              {
                val_b *= 8;
                length_set = 1;
              }
              if (!get_a )
              {
                get_a = 1;

                for ( k = 0 ; k < 4; k++)
                {
                  if (test & test_amask)
                    val_a   += test_amask;
                  test_amask = test_amask >> 1;
                }
              }
              else
              {

                if (test & 0x01) val_b += pow(2, val_a);
                val_a -= 1;
                if (val_a == 0 ) get_b = 1;
              }

            }
          }
          else
          {
            if (!data_set)
            {
              if ( (i > 0  )  && ( row_ptrs[compnum][0][blocknum][i] != 0) && (abs(row_ptrs[compnum][0][blocknum][i]) > 1))
              {
                int test_mask = 2, k = 0;
                int test = abs (row_ptrs[compnum][0][blocknum][i]);
                if ( test >= 4)
                {
                  while (test_mask)
                  {
                    if (test & test_mask)
                      mask[count_bits] = mask[count_bits] | test_mask;
                    test_mask = test_mask >> 1;
                  }
                  count_bits++;
                  if ( count_bits == (val_b / 2) ) data_set = 1;
                }
              }
            }
          }

        }
      }

    }
  }

  i = 0;
  l = 0;
  while ( i < count_bits)
  {
    int k;
    int decode_mask = 0x80;
    if (!test_mask) test_mask = 0x02;
    while (decode_mask)
    {
      if ( mask[i] & test_mask)
        decode_int[l] += decode_mask;
      test_mask >>= 1;
      if (!test_mask) { i++; test_mask = 0x02; }

      decode_mask >>= 1;
    }
    l++;
  }
  (void) jpeg_finish_decompress(&srcinfo);
  jpeg_destroy_decompress(&srcinfo);
  fclose (input_file);
  decode_int[l] = 0; // null terminating

  *message_len = l;
  *message = decode_int;
};


int main (int argc, char **argv)
{
  if ( argc == 2)
  {
    char * message;
    size_t message_len;
    JPEG_extractbits( argv[1], &message, &message_len);
    printf("%s\n", message);
    free(message);
  }

  else

  {
    printf ("USAGE : \n");
    printf ("./decode <watermarkedimage>\n");
  }

  return 0;      /* suppress no-return-value warnings */
}


#include "bitmap.h"

/* CAREFUL WITH pos AND BITMAP SIZE! */

bool bitmapGet(const byte *bitmap, int pos) {
/* gets the value of the bit at pos */
    return get(bitmap[pos/BIT], pos%BIT);
}

void bitmapSet(byte *bitmap, int pos) {
/* sets bit at pos to 1 */
    set(&bitmap[pos/BIT], pos%BIT);
}

void bitmapClear(byte *bitmap, int pos) {
/* sets bit at pos to 0 */
    clear(&bitmap[pos/BIT], pos%BIT);
}

void bitmapFlip  (byte *bitmap, int pos) {
    xor( &bitmap[pos/BIT], pos%BIT );
}


void bitmapAssign( byte *bitmap, int pos, bool bit) {
/* essentially performs: bitmap[pos]=bit */
    assign( &bitmap[pos/BIT], pos%BIT, bit ? 1 : 0 );
}


int bitmapSearch(byte *bitmap, bool n, int size, int start) {
/* Finds the first n value in bitmap after start */
/* size is the Bitmap size in bytes */
    int i;
    /* size is now the Bitmap size in bits */
    for(i = start+1, size *= BIT; i < size; i++)
        if(bitmapGet(bitmap,i) == n)
            return i;
    return BITMAP_NOTFOUND;
}

bool get(byte a, byte pos) {
/* pos is something from 0 to 7*/
    return (a >> pos) & 1;
}

void set(byte *a, byte pos) {
/* pos is something from 0 to 7*/
/* sets bit to 1 */
    *a |= 1 << pos;
}


void assign(byte *a, byte pos, byte bitval) {
    byte assign = bitval << pos;
    byte bitnum = 1 << pos;
    *a = ( *a & (0xff ^ bitnum)) | assign;
}


void xor(byte *a, byte pos) {
    *a ^= 1<< pos;
}

void clear(byte *a, byte pos) {
/* pos is something from 0 to 7*/
/* sets bit to 0 */
    *a &= ~(1 << pos);
}

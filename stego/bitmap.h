#ifndef _BITMAP_H
#define _BITMAP_H

#define BIT (8*sizeof(byte))
#define BITMAP_NOTFOUND -1

typedef enum{false=0, true} bool;
typedef unsigned char byte;

bool bitmapGet   (const byte *, int);
void bitmapSet   (byte *, int);
void bitmapFlip  (byte *, int);
void bitmapClear (byte *, int);
void bitmapAssign(byte *, int, bool);
int  bitmapSearch(byte *, bool, int, int);

bool get  (byte,   byte);
void set  (byte *, byte);
void clear(byte *, byte);
void assign(byte*, byte, byte);
void xor(byte *, byte);


#endif

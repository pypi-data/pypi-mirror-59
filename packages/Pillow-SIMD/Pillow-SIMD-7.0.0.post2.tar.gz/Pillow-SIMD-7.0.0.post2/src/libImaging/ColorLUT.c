#include "Imaging.h"
#include <math.h>


/* 8 bits for result. Table can overflow [0, 1.0] range,
   so we need extra bits for overflow and negative values.
   NOTE: This value should be the same as in _imaging/_prepare_lut_table() */
#define PRECISION_BITS (16 - 8 - 2)
#define PRECISION_ROUNDING (1<<(PRECISION_BITS-1))

/* 8 — scales are multiplied on byte.
   6 — max index in the table
       (max size is 65, but index 64 is not reachable) */
#define SCALE_BITS (32 - 8 - 6)
#define SCALE_MASK ((1<<SCALE_BITS) - 1)

#define SHIFT_BITS (16 - 1)


/*
 Transforms colors of imIn using provided 3D lookup table
 and puts the result in imOut. Returns imOut on success or 0 on error.

 imOut, imIn — images, should be the same size and may be the same image.
    Should have 3 or 4 channels.
 table_channels — number of channels in the lookup table, 3 or 4.
    Should be less or equal than number of channels in imOut image;
 size1D, size_2D and size3D — dimensions of provided table;
 table — flat table,
    array with table_channels × size1D × size2D × size3D elements,
    where channels are changed first, then 1D, then​ 2D, then 3D.
    Each element is signed 16-bit int where 0 is lowest output value
    and 255 << PRECISION_BITS (16320) is highest value.
*/
Imaging
ImagingColorLUT3D_linear(Imaging imOut, Imaging imIn, int table_channels,
                         int size1D, int size2D, int size3D,
                         INT16* table)
{
    /* This float to int conversion doesn't have rounding
       error compensation (+0.5) for two reasons:
       1. As we don't hit the highest value,
          we can use one extra bit for precision.
       2. For every pixel, we interpolate 8 elements from the table:
          current and +1 for every dimension and their combinations.
          If we hit the upper cells from the table,
          +1 cells will be outside of the table.
          With this compensation we never hit the upper cells
          but this also doesn't introduce any noticeable difference. */
    int y, size1D_2D = size1D * size2D;
    ImagingSectionCookie cookie;
    __m128i scale = _mm_set_epi32(0,
        (size3D - 1) / 255.0 * (1<<SCALE_BITS),
        (size2D - 1) / 255.0 * (1<<SCALE_BITS),
        (size1D - 1) / 255.0 * (1<<SCALE_BITS));
    __m128i scale_mask = _mm_set1_epi32(SCALE_MASK);
    __m128i index_mul = _mm_set_epi32(
        0, size1D_2D*table_channels, size1D*table_channels, table_channels);
    __m128i shuffle3 = _mm_set_epi8(-1,-1, -1,-1, 11,10, 5,4, 9,8, 3,2, 7,6, 1,0);
    __m128i shuffle4 = _mm_set_epi8(15,14, 7,6, 13,12, 5,4, 11,10, 3,2, 9,8, 1,0);
#if defined(__AVX2__)
    __m256i scale256 = _mm256_set_epi32(
        0,
        (size3D - 1) / 255.0 * (1<<SCALE_BITS),
        (size2D - 1) / 255.0 * (1<<SCALE_BITS),
        (size1D - 1) / 255.0 * (1<<SCALE_BITS),
        0,
        (size3D - 1) / 255.0 * (1<<SCALE_BITS),
        (size2D - 1) / 255.0 * (1<<SCALE_BITS),
        (size1D - 1) / 255.0 * (1<<SCALE_BITS));
    __m256i scale_mask256 = _mm256_set1_epi32(SCALE_MASK);
    __m256i index_mul256 = _mm256_set_epi32(
        0, size1D_2D*table_channels, size1D*table_channels, table_channels,
        0, size1D_2D*table_channels, size1D*table_channels, table_channels);
    __m256i shuffle3_256 = _mm256_set_epi8(
        -1,-1, -1,-1, 11,10, 5,4, 9,8, 3,2, 7,6, 1,0,
        -1,-1, -1,-1, 11,10, 5,4, 9,8, 3,2, 7,6, 1,0);
    __m256i shuffle4_256 = _mm256_set_epi8(
        15,14, 7,6, 13,12, 5,4, 11,10, 3,2, 9,8, 1,0,
        15,14, 7,6, 13,12, 5,4, 11,10, 3,2, 9,8, 1,0);
#endif

    if (table_channels < 3 || table_channels > 4) {
        PyErr_SetString(PyExc_ValueError, "table_channels could be 3 or 4");
        return NULL;
    }

    if (imIn->type != IMAGING_TYPE_UINT8 ||
        imOut->type != IMAGING_TYPE_UINT8 ||
        imIn->bands < 3 ||
        imOut->bands < table_channels
    ) {
        return (Imaging) ImagingError_ModeError();
    }

    /* In case we have one extra band in imOut and don't have in imIn.*/
    if (imOut->bands > table_channels && imOut->bands > imIn->bands) {
        return (Imaging) ImagingError_ModeError();
    }

    ImagingSectionEnter(&cookie);
    for (y = 0; y < imOut->ysize; y++) {
        UINT32* rowIn = (UINT32 *)imIn->image[y];
        UINT32* rowOut = (UINT32 *)imOut->image[y];
        UINT8* rowIn8 = (UINT8 *)imIn->image[y];
        UINT8* rowOut8 = (UINT8 *)imOut->image[y];
        int x = 0;

    #if defined(__AVX2__)
    {
        __m256i index = _mm256_mullo_epi32(scale256, mm256_cvtepu8_epi32(&rowIn[x]));
        __m256i idxs = _mm256_hadd_epi32(_mm256_hadd_epi32(
            _mm256_madd_epi16(index_mul256, _mm256_srli_epi32(index, SCALE_BITS)),
            _mm256_setzero_si256()), _mm256_setzero_si256());
        int idx1 = _mm_cvtsi128_si32(_mm256_castsi256_si128(idxs));
        int idx2 = _mm256_extract_epi32(idxs, 4);

        for (; x < imOut->xsize - 1; x += 2) {
            __m256i next_index = _mm256_mullo_epi32(scale256, mm256_cvtepu8_epi32(&rowIn[x + 2]));
            __m256i next_idxs = _mm256_hadd_epi32(_mm256_hadd_epi32(
                _mm256_madd_epi16(index_mul256, _mm256_srli_epi32(next_index, SCALE_BITS)),
                _mm256_setzero_si256()), _mm256_setzero_si256());
            int next_idx1 = _mm_cvtsi128_si32(_mm256_castsi256_si128(next_idxs));
            int next_idx2 = _mm256_extract_epi32(next_idxs, 4);

            __m256i shift = _mm256_srli_epi32(
                _mm256_and_si256(scale_mask256, index), (SCALE_BITS - SHIFT_BITS));

            __m256i shift1D, shift2D, shift3D;
            __m256i source, left, right, result;
            __m256i leftleft, leftright, rightleft, rightright;

            shift = _mm256_or_si256(
                _mm256_sub_epi32(_mm256_set1_epi32((1<<SHIFT_BITS)-1), shift),
                _mm256_slli_epi32(shift, 16));

            shift1D = _mm256_shuffle_epi32(shift, 0x00);
            shift2D = _mm256_shuffle_epi32(shift, 0x55);
            shift3D = _mm256_shuffle_epi32(shift, 0xaa);

            if (table_channels == 3) {
                source = _mm256_shuffle_epi8(
                    _mm256_inserti128_si256(_mm256_castsi128_si256(
                        _mm_loadu_si128((__m128i *) &table[idx1 + 0])),
                        _mm_loadu_si128((__m128i *) &table[idx2 + 0]), 1),
                    shuffle3_256);
                leftleft = _mm256_srai_epi32(_mm256_madd_epi16(
                    source, shift1D), SHIFT_BITS);

                source = _mm256_shuffle_epi8(
                    _mm256_inserti128_si256(_mm256_castsi128_si256(
                        _mm_loadu_si128((__m128i *) &table[idx1 + size1D*3])),
                        _mm_loadu_si128((__m128i *) &table[idx2 + size1D*3]), 1),
                    shuffle3_256);
                leftright = _mm256_slli_epi32(_mm256_madd_epi16(
                    source, shift1D), 16 - SHIFT_BITS);

                source = _mm256_shuffle_epi8(
                    _mm256_inserti128_si256(_mm256_castsi128_si256(
                        _mm_loadu_si128((__m128i *) &table[idx1 + size1D_2D*3])),
                        _mm_loadu_si128((__m128i *) &table[idx2 + size1D_2D*3]), 1),
                    shuffle3_256);
                rightleft = _mm256_srai_epi32(_mm256_madd_epi16(
                    source, shift1D), SHIFT_BITS);
                
                source = _mm256_shuffle_epi8(
                    _mm256_inserti128_si256(_mm256_castsi128_si256(
                        _mm_loadu_si128((__m128i *) &table[idx1 + size1D_2D*3 + size1D*3])),
                        _mm_loadu_si128((__m128i *) &table[idx2 + size1D_2D*3 + size1D*3]), 1),
                    shuffle3_256);
                rightright = _mm256_slli_epi32(_mm256_madd_epi16(
                    source, shift1D), 16 - SHIFT_BITS);

                left = _mm256_srai_epi32(_mm256_madd_epi16(
                    _mm256_blend_epi16(leftleft, leftright, 0xaa), shift2D),
                    SHIFT_BITS);

                right = _mm256_slli_epi32(_mm256_madd_epi16(
                    _mm256_blend_epi16(rightleft, rightright, 0xaa), shift2D),
                    16 - SHIFT_BITS);

                result = _mm256_madd_epi16(
                    _mm256_blend_epi16(left, right, 0xaa), shift3D);

                result = _mm256_srai_epi32(_mm256_add_epi32(
                    _mm256_set1_epi32(PRECISION_ROUNDING<<SHIFT_BITS), result),
                    PRECISION_BITS + SHIFT_BITS);

                result = _mm256_packs_epi32(result, result);
                result = _mm256_packus_epi16(result, result);
                rowOut[x + 0] = _mm_cvtsi128_si32(_mm256_castsi256_si128(result));
                rowOut[x + 1] = _mm256_extract_epi32(result, 4);
                rowOut8[x*4 + 3] = rowIn8[x*4 + 3];
                rowOut8[x*4 + 7] = rowIn8[x*4 + 7];
            }

            if (table_channels == 4) {
                source = _mm256_shuffle_epi8(
                    _mm256_inserti128_si256(_mm256_castsi128_si256(
                        _mm_loadu_si128((__m128i *) &table[idx1 + 0])),
                        _mm_loadu_si128((__m128i *) &table[idx2 + 0]), 1),
                    shuffle4_256);
                leftleft = _mm256_srai_epi32(_mm256_madd_epi16(
                    source, shift1D), SHIFT_BITS);

                source = _mm256_shuffle_epi8(
                    _mm256_inserti128_si256(_mm256_castsi128_si256(
                        _mm_loadu_si128((__m128i *) &table[idx1 + size1D*4])),
                        _mm_loadu_si128((__m128i *) &table[idx2 + size1D*4]), 1),
                    shuffle4_256);
                leftright = _mm256_slli_epi32(_mm256_madd_epi16(
                    source, shift1D), 16 - SHIFT_BITS);

                source = _mm256_shuffle_epi8(
                    _mm256_inserti128_si256(_mm256_castsi128_si256(
                        _mm_loadu_si128((__m128i *) &table[idx1 + size1D_2D*4])),
                        _mm_loadu_si128((__m128i *) &table[idx2 + size1D_2D*4]), 1),
                    shuffle4_256);
                rightleft = _mm256_srai_epi32(_mm256_madd_epi16(
                    source, shift1D), SHIFT_BITS);
                
                source = _mm256_shuffle_epi8(
                    _mm256_inserti128_si256(_mm256_castsi128_si256(
                        _mm_loadu_si128((__m128i *) &table[idx1 + size1D_2D*4 + size1D*4])),
                        _mm_loadu_si128((__m128i *) &table[idx2 + size1D_2D*4 + size1D*4]), 1),
                    shuffle4_256);
                rightright = _mm256_slli_epi32(_mm256_madd_epi16(
                    source, shift1D), 16 - SHIFT_BITS);

                left = _mm256_srai_epi32(_mm256_madd_epi16(
                    _mm256_blend_epi16(leftleft, leftright, 0xaa), shift2D),
                    SHIFT_BITS);

                right = _mm256_slli_epi32(_mm256_madd_epi16(
                    _mm256_blend_epi16(rightleft, rightright, 0xaa), shift2D),
                    16 - SHIFT_BITS);

                result = _mm256_madd_epi16(
                    _mm256_blend_epi16(left, right, 0xaa), shift3D);

                result = _mm256_srai_epi32(_mm256_add_epi32(
                    _mm256_set1_epi32(PRECISION_ROUNDING<<SHIFT_BITS), result),
                    PRECISION_BITS + SHIFT_BITS);

                result = _mm256_packs_epi32(result, result);
                result = _mm256_packus_epi16(result, result);
                rowOut[x+0] = _mm_cvtsi128_si32(_mm256_castsi256_si128(result));
                rowOut[x+1] = _mm256_extract_epi32(result, 4);
            }
            index = next_index;
            idx1 = next_idx1;
            idx2 = next_idx2;
        }
    }
    #endif

        __m128i index = _mm_mullo_epi32(scale, mm_cvtepu8_epi32(&rowIn[x]));
        int idx = _mm_cvtsi128_si32(
            _mm_hadd_epi32(_mm_hadd_epi32(
                _mm_madd_epi16(index_mul, _mm_srli_epi32(index, SCALE_BITS)),
                _mm_setzero_si128()), _mm_setzero_si128()));

        for (; x < imOut->xsize; x++) {
            __m128i next_index = _mm_mullo_epi32(scale, mm_cvtepu8_epi32(&rowIn[x + 1]));
            int next_idx = _mm_cvtsi128_si32(
                _mm_hadd_epi32(_mm_hadd_epi32(
                    _mm_madd_epi16(index_mul, _mm_srli_epi32(next_index, SCALE_BITS)),
                    _mm_setzero_si128()), _mm_setzero_si128()));

            __m128i shift = _mm_srli_epi32(
                _mm_and_si128(scale_mask, index), (SCALE_BITS - SHIFT_BITS));

            __m128i shift1D, shift2D, shift3D;
            __m128i source, left, right, result;
            __m128i leftleft, leftright, rightleft, rightright;

            shift = _mm_or_si128(
                _mm_sub_epi32(_mm_set1_epi32((1<<SHIFT_BITS)-1), shift),
                _mm_slli_epi32(shift, 16));

            shift1D = _mm_shuffle_epi32(shift, 0x00);
            shift2D = _mm_shuffle_epi32(shift, 0x55);
            shift3D = _mm_shuffle_epi32(shift, 0xaa);

            if (table_channels == 3) {
                source = _mm_shuffle_epi8(
                    _mm_loadu_si128((__m128i *) &table[idx + 0]), shuffle3);
                leftleft = _mm_srai_epi32(_mm_madd_epi16(
                    source, shift1D), SHIFT_BITS);

                source = _mm_shuffle_epi8(
                    _mm_loadu_si128((__m128i *) &table[idx + size1D*3]), shuffle3);
                leftright = _mm_slli_epi32(_mm_madd_epi16(
                    source, shift1D), 16 - SHIFT_BITS);

                source = _mm_shuffle_epi8(
                    _mm_loadu_si128((__m128i *) &table[idx + size1D_2D*3]), shuffle3);
                rightleft = _mm_srai_epi32(_mm_madd_epi16(
                    source, shift1D), SHIFT_BITS);
                
                source = _mm_shuffle_epi8(
                    _mm_loadu_si128((__m128i *) &table[idx + size1D_2D*3 + size1D*3]), shuffle3);
                rightright = _mm_slli_epi32(_mm_madd_epi16(
                    source, shift1D), 16 - SHIFT_BITS);

                left = _mm_srai_epi32(_mm_madd_epi16(
                    _mm_blend_epi16(leftleft, leftright, 0xaa), shift2D),
                    SHIFT_BITS);

                right = _mm_slli_epi32(_mm_madd_epi16(
                    _mm_blend_epi16(rightleft, rightright, 0xaa), shift2D),
                    16 - SHIFT_BITS);

                result = _mm_madd_epi16(
                    _mm_blend_epi16(left, right, 0xaa), shift3D);

                result = _mm_srai_epi32(_mm_add_epi32(
                    _mm_set1_epi32(PRECISION_ROUNDING<<SHIFT_BITS), result),
                    PRECISION_BITS + SHIFT_BITS);

                result = _mm_packs_epi32(result, result);
                rowOut[x] = _mm_cvtsi128_si32(_mm_packus_epi16(result, result));
                rowOut8[x*4 + 3] = rowIn8[x*4 + 3];
            }

            if (table_channels == 4) {
                source = _mm_shuffle_epi8(
                    _mm_loadu_si128((__m128i *) &table[idx + 0]), shuffle4);
                leftleft = _mm_srai_epi32(_mm_madd_epi16(
                    source, shift1D), SHIFT_BITS);

                source = _mm_shuffle_epi8(
                    _mm_loadu_si128((__m128i *) &table[idx + size1D*4]), shuffle4);
                leftright = _mm_slli_epi32(_mm_madd_epi16(
                    source, shift1D), 16 - SHIFT_BITS);

                source = _mm_shuffle_epi8(
                    _mm_loadu_si128((__m128i *) &table[idx + size1D_2D*4]), shuffle4);
                rightleft = _mm_srai_epi32(_mm_madd_epi16(
                    source, shift1D), SHIFT_BITS);
                
                source = _mm_shuffle_epi8(
                    _mm_loadu_si128((__m128i *) &table[idx + size1D_2D*4 + size1D*4]), shuffle4);
                rightright = _mm_slli_epi32(_mm_madd_epi16(
                    source, shift1D), 16 - SHIFT_BITS);

                left = _mm_srai_epi32(_mm_madd_epi16(
                    _mm_blend_epi16(leftleft, leftright, 0xaa), shift2D),
                    SHIFT_BITS);

                right = _mm_slli_epi32(_mm_madd_epi16(
                    _mm_blend_epi16(rightleft, rightright, 0xaa), shift2D),
                    16 - SHIFT_BITS);

                result = _mm_madd_epi16(
                    _mm_blend_epi16(left, right, 0xaa), shift3D);

                result = _mm_srai_epi32(_mm_add_epi32(
                    _mm_set1_epi32(PRECISION_ROUNDING<<SHIFT_BITS), result),
                    PRECISION_BITS + SHIFT_BITS);

                result = _mm_packs_epi32(result, result);
                rowOut[x] = _mm_cvtsi128_si32(_mm_packus_epi16(result, result));
            }
            index = next_index;
            idx = next_idx;
        }
    }
    ImagingSectionLeave(&cookie);

    return imOut;
}

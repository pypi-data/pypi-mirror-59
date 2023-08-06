#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include <emmintrin.h>
#include <mmintrin.h>
#include <smmintrin.h>
#if defined(__AVX2__)
    #include <immintrin.h>
#endif


static __m128i __attribute__((always_inline)) inline
mm_cvtepu8_epi32(int32_t* ptr) {
    __m128i x;
    __asm__ volatile ("pmovzxbd %1, %0" : "=x"(x) : "m"(*ptr) );
    return x;
}


__m128i __attribute__ ((noinline))
test_block(int size) {
    void *ptr = malloc(size);
    *(int32_t *)(ptr + size - 3) = 1;
    // return _mm_cvtepu8_epi32(*(__m128i *)(ptr + size - 4));
    return mm_cvtepu8_epi32((int32_t *)(ptr + size - 4));
}


int
main(int argc, char* argv[]) {
    int i;
    __m128i acc = _mm_setzero_si128();
    for (int i = 0; i < 50; ++i) {
        acc = _mm_add_epi32(acc, test_block(4096));
    }
    printf("%d\n", _mm_cvtsi128_si32(_mm_srli_si128(acc, 4)));
    return 0;
}

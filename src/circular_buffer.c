/*
 Name: Or Levy, Daniel Rabinovitsch
 Date: 14/10/26
 File: circular_buffer.c
 */

#include "peripherals.h"
#include "filter_taps.h"

struct buffer idata cbuffer;

void cbuffer_reset(struct buffer *cbrptr) // clear the buffer
{
    unsigned char i;
    for (i = 0; i < FILTER_LENGTH; i++)
    {
        cbrptr->sample[i] = 0;
    }
    cbrptr->oldest_index = 0;
    cbrptr->length = FILTER_LENGTH;
}

unsigned int update_cbuffer(struct buffer *cbrptr, unsigned int newsample)
{
    unsigned int t_oldest;
    t_oldest = cbrptr->sample[cbrptr->oldest_index];
    cbrptr->sample[cbrptr->oldest_index] = newsample;
    if (cbrptr->oldest_index < (cbrptr->length) - 1) 
    {
        cbrptr->oldest_index++;
    }
    else
    {
        cbrptr->oldest_index = 0;
    }
    return t_oldest;
}
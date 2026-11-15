/*
 Name: Or Levy 322273640, Daniel Rabinovitsch 34504688
 Date: 14/10/26
 File: peripherals.h 
 */

#ifndef PERIPHERALS_H
#define PERIPHERALS_H

#include "filter_taps.h"

sfr16 ADCDATA = 0xD9;
sfr16 DAC0DATA = 0xF9;
sfr16 DAC1DATA = 0xFB;

struct buffer
{
    unsigned int sample[FILTER_LENGTH];
    unsigned char oldest_index;
    unsigned char length;
};

extern struct buffer idata cbuffer;
extern bit ADCflag;
extern unsigned int newsample;

void T2_Init(void);
void ADC_Init(void);
void DAC_Init(void);
void GlobalINT(void);  
void cbuffer_reset(struct buffer *cbrptr);
unsigned int update_cbuffer(struct buffer *cbrptr, unsigned int newsample);

#endif
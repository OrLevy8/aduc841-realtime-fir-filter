/*
 Name: Or Levy, Daniel Rabinovitsch
 Date: 14/10/26
 File: peripherals.c
 */

#include <aduc841.h>
#include <stdio.h>
#include "peripherals.h"
#include "filter_taps.h"

bit ADCflag = 0;
unsigned int newsample = 0;

void T2_Init(void) 
{
    TR2 = 1;
    RCAP2H = 0xD4;   
    RCAP2L = 0xCC;   
}

void ADC_Init(void) // ADC ON
{
    ADCCON1 = 0xBA;
    ADCCON2 = 0x00;
    EADC = 1;
}

void DAC_Init(void) // DAC0 ON
{
    DACCON = 0x1F;
}

void GlobalINT(void) // Global Interrup 
{	
    EA = 1;
}

void ADC_ISR(void) interrupt 6 // ADC ISR
{ 
    newsample = ADCDATA;
    ADCflag = 1;
}
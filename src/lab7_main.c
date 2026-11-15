/*
 Name: Or Levy, Daniel Rabinovitsch
 Date: 14/10/26
 DESCRIPTION: FIR LPF filter implementation
 File: lab7_main.c

 OBSERVATION / PICOSCOPE RESULTS (Section 22.4):
 When examining the filter's operation using the oscilloscope (PicoScope) across 0 - 200 Hz:
 1. DC (0 Hz): Exact baseline preservation (1.25V offset maintained, Gain = 0.0 dB).
 2. Passband (10 Hz): Full signal transmission (Vpp = 2.08V vs 2.15V in, Gain = -0.3 dB),
    with a clear linear phase group delay of exactly 5.0 ms (tau = (11 - 1) / (2 * 1000 Hz)).
 3. Cutoff Knee (70 Hz): Output amplitude drops to 1.53V (Gain = -2.8 dB, close to nominal
    -3 dB cutoff point of ~64 Hz) with a phase shift of approximately -90 degrees.
 4. Deep Stopband (200 Hz): Strong attenuation of high-frequency components down to 
    0.38V (Gain = -14.1 dB), heavily suppressing noise and harmonics down to the DAC/ADC noise floor.
 */

#include <aduc841.h>
#include <stdio.h>
#include "filter_taps.h"
#include "peripherals.h"

unsigned char m;
long int sum;
long int filtered;
unsigned int oldest;
unsigned char buffer_index;

void main(void)
{
    T2_Init();
    ADC_Init();
    DAC_Init();
    GlobalINT();  
    cbuffer_reset(&cbuffer); 

    while (1)
    {
        if (ADCflag) 
        {
            ADCflag = 0;
            oldest = update_cbuffer(&cbuffer, newsample);
            if (cbuffer.oldest_index == 0) // Start at newest sample every cycle
            {
                buffer_index = FILTER_LENGTH - 1;
            }
            else
            {
                buffer_index = cbuffer.oldest_index - 1;
            }

            sum = 0;
            for (m = 0; m < FILTER_LENGTH; m++)  // m = 0 to 2N
            {
                sum += (long int)filter_taps[m] * (long int)cbuffer.sample[buffer_index];  
                if (buffer_index == 0) // move to the next sample back in time
                {
                    buffer_index = FILTER_LENGTH - 1;
                }
                else
                {
                    buffer_index--;
                }
            }

            filtered = sum / SCALING_FACTOR;
            DAC0DATA = newsample;    

            // Clamp negative filtered output to zero (prevent DAC underflow, Section 22.3)
            if (filtered < 0) 
            {
                filtered = 0;
            }

            DAC1DATA = (unsigned int)filtered;
        }
    }
}
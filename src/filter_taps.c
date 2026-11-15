/*
 Name: Or Levy, Daniel Rabinovitsch
 Date: 14/10/26
 File: filter_taps.c
 */

#include "filter_taps.h"

const signed char code filter_taps[FILTER_LENGTH] = {
    0, 30, 64, 96, 119, 127, 119, 96, 64, 30, 0
};

/* Copyright 2014, Mariano Cerdeiro
 * Copyright 2014, Pablo Ridolfi
 * Copyright 2014, Juan Cecconi
 * Copyright 2014, Gustavo Muro
 * Copyright 2016, Alvaro Alonso Bivou <alonso.bivou@gmail.com>
 * All rights reserved.
 *
 * This file is part of CIAA Firmware.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 * 1. Redistributions of source code must retain the above copyright notice,
 *    this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright notice,
 *    this list of conditions and the following disclaimer in the documentation
 *    and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 *    contributors may be used to endorse or promote products derived from this
 *    software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 *
 */

/** \brief Simon Says game implementation for EDU-CIAA
 **
 ** This is the Simon Says game. The light sequence must be
 ** replicated by the user pressing the buttons.
 **/

/** \addtogroup CIAA_Firmware CIAA Firmware
 ** @{ */
/** \addtogroup Examples CIAA Firmware Examples
 ** @{ */
/** \addtogroup Games Simon example source file
 ** @{ */

/*
 * Initials     Name
 * ---------------------------
 * AA         Alvaro Alonso
 */

 /*
 * modification history (new versions first)
 * -----------------------------------------------------------
 * 20160611 v0.0.2   AA   random sequence option
 * 20160607 v0.0.1   AA   first functional version
 */

/*==================[inclusions]=============================================*/
#include "tp.h"

/*==================[macros and definitions]=================================*/

/*==================[internal data declaration]==============================*/

/*==================[internal functions declaration]=========================*/

/*==================[internal data definition]===============================*/
/** \brief File descriptor for digital output ports
 *
 * Device path /dev/dio/out/0
 */
static int32_t leds_fd;
/** \brief File descriptor for digital input ports
 *
 * Device path /dev/dio/in/0
 */
static int32_t buttons_fd;
/** \brief Current state of the States Machine
 * Initial State or state after reset is IDLE
 * IDLE: The machine is waiting for an input
 */
static states state = SEQUENCE;
/** \brief Array of the sequence to be displayed by the leds **/

static uint8_t sequence[100];

/** \brief Initial level of the game **/
static uint8_t level=0;
static int32_t fd_out;
static int32_t N = 1;
static int32_t P5 = 0;

/*==================[external data definition]===============================*/

/*==================[internal functions definition]==========================*/

/*==================[external functions definition]==========================*/
/** \brief Main function
 *
 * This is the main entry point of the software.
 *
 * \returns 0
 *
 * \remarks This function never returns. Return value is only to avoid compiler
 *          warnings or errors.
 */
int main(void)
{
   /* Starts the operating system in the Application Mode 1 */
   /* This example has only one Application Mode */
   StartOS(Normal);

   /* StartOs shall never returns, but to avoid compiler warnings or errors
    * 0 is returned */
   return 0;
}

/** \brief Error Hook function
 *
 * This fucntion is called from the os if an os interface (API) returns an
 * error. Is for debugging proposes. If called this function triggers a
 * ShutdownOs which ends in a while(1).
 *
 * The values:
 *    OSErrorGetServiceId
 *    OSErrorGetParam1
 *    OSErrorGetParam2
 *    OSErrorGetParam3
 *    OSErrorGetRet
 *
 * will provide you the interface, the input parameters and the returned value.
 * For more details see the OSEK specification:
 * http://portal.osek-vdx.org/files/pdf/specs/os223.pdf
 *
 */
void ErrorHook(void)
{
   ShutdownOS(0);
}

/** \brief Initial task
 *
 * This task is started automatically in the application mode Normal.
 */
TASK(InitTask)
{
   ciaak_start();
   leds_fd = ciaaPOSIX_open(OUTPUTS, ciaaPOSIX_O_RDWR);
   buttons_fd = ciaaPOSIX_open(INPUTS, ciaaPOSIX_O_RDONLY);
   SetRelAlarm(ActivateTaskT1, 0, 400); //Se ejecuta la led 1 cada 400ms
   SetRelAlarm(ActivateTaskT2, 0, 600); //Se ejecuta la led 2 cada 600ms
   SetRelAlarm(ActivateTaskT3, 0, 800); //Se ejecuta la led 3 cada 800ms);
   SetRelAlarm(ActivateOutputTask,START_DELAY_OUTPUT_MS, REFRESH_RATE_OUTPUT_MS);
   SetRelAlarm(ActivateInputTask, 0, 50);
   TerminateTask();
}

TASK(T1)
{
   uint8_t outputs;

   ciaaPOSIX_read(fd_out, &outputs, 1);

   outputs ^= 0b00001000;
   ciaaPOSIX_write(fd_out, &outputs, 1);
   printf("T1, N es %d", N);

   TerminateTask();
}

TASK(T2)
{
   uint8_t outputs;

   /* write blinking message */

   /* blink output */
   ciaaPOSIX_read(fd_out, &outputs, 1);

   outputs ^= 0b00010000;
   ciaaPOSIX_write(fd_out, &outputs, 1);
   printf("T2, N es %d", N * 10);

   TerminateTask();
}

TASK(T3)
{
   uint8_t outputs;
   ciaaPOSIX_read(fd_out, &outputs, 1);

   outputs ^= 0b00100000;
   ciaaPOSIX_write(fd_out, &outputs, 1);
   printf("T3, N es %d", N * 100);

   TerminateTask();
}

// imprime N * 1000 y prende la led 4
TASK(T5){
   uint8_t outputs;

   /* write blinking message */

   /* blink output */
   ciaaPOSIX_read(fd_out, &outputs, 1);

   if(P5 == 0){
	   outputs = outputs + 1;
	   P5 = 1;
	   ciaaPOSIX_write(fd_out, &outputs, 1);
	   printf("N es %d", N * 1000);
   }

   TerminateTask();
}

// eleva N
TASK(T4){
	N = N + 1;
	TerminateTask();
}

TASK(InputTask)
{
   uint8_t inputs_now;

   (void)ciaaPOSIX_read(1, &inputs_now, 1);
   inputs_now = ~inputs_now;
   switch(state)
    {
      case LISTEN:
		if (inputs_now == 241){
			ActivateTask(T4);
    	}
		if (inputs_now == 248){
			ActivateTask(T5);
    	}


		if (inputs_now == 240 && P5 == 1){
		   uint8_t outputs;
		   ciaaPOSIX_read(fd_out, &outputs, 1);

		   outputs = outputs - 1;
		   P5 = 0;
		   ciaaPOSIX_write(fd_out, &outputs, 1);
		}
    }
   TerminateTask();
}

TASK(OutputTask)
{
   static uint8_t outputs=0x00;
   static uint8_t index=0;

   switch(state)
      {
      case SEQUENCE:
         state =  (index > (level*2)) ? LISTEN : SEQUENCE;
         index = (state == LISTEN) ? 0 : (index+1);
         break;
   }
   TerminateTask();
}

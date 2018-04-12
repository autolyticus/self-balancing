#include "phy.h"
#include <fcntl.h>
#include <pigpiod_if2.h>
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define stepAngle 1.8

int piNum = -1;

const int maxrpm = 375;
const int minrpm = 60;

const double conversionFactor = 60.0 * (stepAngle / 360.0);

unsigned short currentStep = 0;
int rpm = 0;

short pins[4];
const short stepSignal[][4] = {
    {1, 0, 1, 0}, {0, 1, 1, 0}, {0, 1, 0, 1}, {1, 0, 0, 1}};

void stop(int signum) {
  rpm = 0;
  /* gpioTerminate(); */
  for (int i = 0; i < 4; i++) {
    printf("setting pin %d as input", i);
    set_mode(piNum, pins[i], PI_INPUT);
  }
  pigpio_stop(piNum);
  exit(1);
}

void *updaterpm(void *);

void stepWrite(unsigned short stepNumber);

int main(int argc, char *argv[]) {
  if (argc != 5) {
    return -1;
  }
  if ((piNum = pigpio_start(NULL, NULL)) < 0)
    return -1;
  /* printf("%d", piNum); */
  signal(SIGINT, stop);
  signal(SIGTERM, stop);

  for (int i = 0; i < (argc - 1); i++) {
    printf("setting pin %d as output", i);
    pins[i] = phytogpio[atoi(argv[i + 1])];
    set_mode(piNum, pins[i], PI_OUTPUT);
  }

  pthread_t inputThread;
  pthread_create(&inputThread, NULL, updaterpm, NULL);

  while (1) {
    double currpm = rpm;
    if (currpm > 0) {
      stepWrite(currentStep);
      currentStep = (currentStep + 1) % 4;
      time_sleep(conversionFactor / currpm);
      /* printf("%s\n", (char *)ptr); */
      /* fflush(stdout); */
    } else if (currpm < 0) {
      stepWrite(currentStep);
      currentStep = (currentStep + 3) % 4;
      time_sleep(conversionFactor / -currpm);
      /* printf("%s\n", (char *)ptr); */
      /* fflush(stdout); */
    }
  }
  /* Stop DMA, release resources */

  return 0;
}

void stepWrite(unsigned short stepNumber) {
  /* printf("Writing (%d, ", stepSignal[currentStep][0]); */
  /* printf("%d, ", stepSignal[currentStep][1]); */
  /* printf("%d, ", stepSignal[currentStep][2]); */
  /* printf("%d)", stepSignal[currentStep][3]); */
  /* printf("to pins (%d, %d, %d, %d)\n", pins[0], pins[1], pins[2], pins[3]);
   */
  for (int i = 0; i < 4; i++) {
    gpio_write(piNum, pins[i], stepSignal[currentStep][i]);
  }
}

void *updaterpm(void *param) {
  int readrpm;
  while (1) {
    /* Read the rpm from SHM */
    scanf("%d", &readrpm);

    /* if there's no change in the rpm do nothing */
    if (readrpm == rpm)
      continue;

    if (readrpm > 0) {
      if (readrpm > maxrpm)
        rpm = maxrpm;
      else if (readrpm < minrpm)
        rpm = 0;
      else
        rpm = readrpm;
    }

    else if (readrpm < 0) {
      if (readrpm < -maxrpm)
        rpm = -maxrpm;
      else if (readrpm > -minrpm)
        rpm = 0;
      else
        rpm = readrpm;
    }

    else
      rpm = 0;
  }
}

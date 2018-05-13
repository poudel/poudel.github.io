---
date: 2017-12-22
location: Kathmandu, Nepal
title: I learn to C and adjust the brightness
description: A small C application to adjust brightness of a Lenovo running ArchLinux
draft: false
code: true
---

I have ArchLinux installed on my work laptop, a Lenovo machine. One
thing that has been a constant bother is adjusting the brightness. It
is desirable to adjust the brightness as the day progresses.

Somehow, the provided hot keys did not work and I have to resort to
updating the `/sys/class/backlight/intel_backlight/brightness` file
manually. I could tried to fix the hotkeys but haven't gotten around
to doing that yet, as I am not very familiar with that side of linux
administration. I am sure I will get around to doing it some day.

At first, I used to run the `tee` command from my bash history, which
I grew tired of very soon. Then I wrote the function below and put it
in a `.sh` file. I would run this everytime after booting.

```shell
bright (){
    # set the screen brightness
    if [ "$#" -eq  "0" ]; then
        ness=450
    else
        ness=$1
    fi
    sudo tee /sys/class/backlight/intel_backlight/brightness <<< $ness
}
```

Then last week, I started dabbling with some C. I realized that I
could implement something similar in C that would help me adjust the
brightness and teach me the language. I know that this problem can be
solved much easily without writing a C program. But, where's the fun
in that?

Here is the the C code that I put together in about an hour.

```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>

/* Adjust brightness in lenevo ideapad

`./bright` Print current brightness
`sudo ./bright <number>` Set the brightness to any arbitrary number
`sudo ./bright d` Set brightness to 300 (for the day)
`sudo ./bright n` Set brightness to 150 (for the night)

*/

int main (int argc, char** cx){

  int count;
  char* brightness;
  FILE * fp;

  char filepath[] = "/sys/class/backlight/intel_backlight/brightness";


  if (argc == 1){

    fp = fopen(filepath, "r");

    if (fp) {
      printf("Current brightness: ");
      while ((count = getc(fp)) != EOF){
	putchar(count);
      }
    }

  } else {

    if (geteuid() != 0){
      printf("Need to run this as root!\n");
      return 0;
    }

    if (strcmp(cx[1], "d") == 0){
      brightness = "300";
    } else if (strcmp(cx[1], "n") == 0) {
      brightness = "150";
    } else {
      brightness = cx[1];
    }

    fp = fopen(filepath, "w");
    fprintf(fp, brightness);
    printf("Successfully set brightness to: %s\n", brightness);
  }

  fclose(fp);

  return 0;
}
```


This is the first time that I have written something useful in the C
language. This gave me a significant sense of satisfaction.

One thing I want to improve is to check the current time and adjust
brightness accordingly if called without an argument. I'll leave that
exercise for the future.

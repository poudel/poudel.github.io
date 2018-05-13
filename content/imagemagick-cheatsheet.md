---
date: 2018-02-21
location: Lalitpur, Nepal
title: ImageMagick commands cheatsheet
description: ImageMagick commands for quick command-line image manipulations
draft: false
code: true
---

Here are some of the commands that might be useful for quick and dirty
image manipulation from the command line. I grew tired of having to
look them up all the time.

ImageMagick is required, of course. Type `convert` to see if it has
been installed.


## One image format to another

For converting to another format, for example `.png` to `.jpg`, use
this command.

```bash
convert file.png file.jpg
```

See [this document](https://www.imagemagick.org/script/convert.php)
for more.

## Image to PDF

Use this command to print one or more image files in a PDF.

```bash
convert file1.jpg -quality 100 output.pdf
```

For multiple files, separate filenames by space. Like this:

```bash
convert file1.jpg file2.jpg -quality 100 output.pdf
```

This produces a single PDF with each image file in a page. Patterns
can be used in lieu of file names as shown below.

```bash
convert "*.{png,jpeg}" -quality 100 output.pdf
```

Taken from this [AskUbuntu](https://askubuntu.com/a/557975) answer.


## Creating collage/montage

To concat multiple images into a single png.

```bash
convert -append *.jpg out.jpg
```

To make a collage of passport-sized photo.

```bash
montage -duplicate 5,0 <filename.jpg> output.jpg
```

See [more](http://www.imagemagick.org/script/montage.php) for answer.
http://www.imagemagick.org/Usage/montage/

https://scottlinux.com/2011/08/13/create-photo-collage-in-linux/
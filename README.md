Hexpaint
===
Hexpaint takes the machine code of a file and creates an image out of it. The script takes the hexdump of a file and converts the hex values into RGB values, and reshapes the hexdump into an image. For smaller files it looks interesting, as you get to larger files it starts to look like noise, though maybe there are more interesting hex dumps out there.

Usage:
```shell
python hex2im.py FILE_NAME
```

Built on top of numpy and PIL.

Some examples:

**My Machine Learning textbook**:
![](https://i.imgur.com/30NYFqm.jpg)


**zip binary**:
![](https://i.imgur.com/9A7PmJM.png)


If you have any ideas on making the visualizations more interesting, let me know!

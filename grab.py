import os
import select

import v4l2capture
from PIL import Image


def capture_frame(width, height, device='/dev/video0'):
    video = v4l2capture.Video_device(device)
    size = video.set_format(width, height)
    video.create_buffers(1)
    video.queue_all_buffers()
    video.start()
    select.select((video,), (), ())
    data = video.read()
    video.close()
    return size, data

def grab_image(filename, width=640, height=480, device='/dev/video0'):
    size, data = capture_frame(width, height, device)
    image = Image.fromstring("RGB", (size), data)
    image.save(filename)
    return True


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        if grab_image(sys.argv[1]):
            print 'Saved image to', sys.argv[1]
            sys.exit(0)
    else:
        print 'Must provide output filename as second parameter'
    sys.exit(1)

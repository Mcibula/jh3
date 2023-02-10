from vidgear.gears import VideoGear
from vidgear.gears import NetGear

stream = VideoGear(
    enablePiCamera=False,
    source=4,
    resolution=(352, 240),
    framerate=10,
    colorspace='COLOR_BGR2RGB'
).start()

server = NetGear(
    address='192.168.241.223',
    port='65433',
    # protocol='tcp',
    pattern=2,
    logging=True
)

while True:
    try:
        frame = stream.read()

        if frame is None:
            break

        server.send(frame)

    except KeyboardInterrupt:
        break

stream.stop()
server.close()

from vidgear.gears import VideoGear
from vidgear.gears import NetGear

stream = VideoGear(
    enablePiCamera=False,
    source=0,
    resolution=(352, 240),
    colorspace='COLOR_BGR2RGB'
).start()

server = NetGear(
    # address='127.0.0.1',
    # port=(65433, 65434),
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

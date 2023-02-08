from vidgear.gears import VideoGear
from vidgear.gears import NetGear

stream = VideoGear(
    source=0,
    resolution=(352, 240),
    colorspace='COLOR_BGR2RGB'
).start()

options = {
    # 'multiclient_mode': True,
    'request_timeout': 60,
    'max_retries': 20
}
server = NetGear(
    # address='127.0.0.1',
    # port=(65433, 65434),
    # protocol='tcp',
    # pattern=1,
    logging=True,
    **options
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

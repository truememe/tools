import can
import asyncio
from typing import List
from can.notifier import MessageRecipient
import signal

running = True

def send_one():
    bus = can.Bus(bustype='pcan', channel="PCAN_USBBUS1", bitrate=500000)
    listener = can.Listener()

    msg = bus.recv()
    listener(msg)

    listener.stop()

def print_message(msg: can.Message) -> None:
    print(msg)

async def main() -> None:
    with can.Bus(
        bustype='pcan',
        channel='PCAN_USBBUS1',
        bitrate=500000
    ) as bus:
        reader = can.AsyncBufferedReader()
        logger = can.Logger("logfile.asc")

        listeners: List[MessageRecipient] = [
            print_message,
            reader,
            logger,
        ]
        loop = asyncio.get_running_loop()
        notifier = can.Notifier(bus, listeners=listeners, loop=loop)
        while running:
            msg = await reader.get_message()

        notifier.stop()

def handler(signum, frame):
    global running
    running = False


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)
    asyncio.run(main())
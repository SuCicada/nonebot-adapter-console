import asyncio
import threading
from typing import List
import websocket
import _thread
import time
import rel
from threading import Thread

from websocket import WebSocketApp


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)
    print("Retry : %s" % time.ctime())
    time.sleep(1)
    connect_websocket()


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")
    print("------------------")


ws: WebSocketApp = None


def connect_websocket():
    # websocket.enableTrace(True)
    global ws
    print("start connect ....")
    ws = websocket.WebSocketApp("ws://127.0.0.1:8765/console",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header={"x-self-id": "2342"}
                                )
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()


def client():
    try:
        connect_websocket()
    except Exception as err:
        print(err)
        print("connect failed")
    # ws.run_forever()
    # ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    # rel.signal(2, rel.abort)  # Keyboard Interrupt
    # rel.dispatch()


def input_line():
    while True:
        s = input("")
        ws.send(s)


def main():
    thread_list = [
        input_line,
    ]

    thread_list = [Thread(target=f) for f in thread_list]
    for t in thread_list:
        t.start()

    client()
    for t in thread_list:
        t.join()


if __name__ == "__main__":
    main()

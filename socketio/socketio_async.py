import socketio
import uvicorn

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[])
app = socketio.ASGIApp(sio, static_files={'/': 'index.html'})


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)


@sio.on('msg')
async def message(sid, data):
    print('message ', data)
    await sio.emit('msg', "ur gayyy")


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=5000)
    # asgi_thread = Thread(target=run)
    # asgi_thread.daemon = True
    # asgi_thread.start()

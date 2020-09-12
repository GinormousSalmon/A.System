import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins=[])
app = socketio.WSGIApp(sio, static_files={'/': 'index.html', '/static/': 'script.js'})


# app = socketio.WSGIApp(sio, static_files={'/': {'content_type': 'text/html', 'filename': 'index.html'}})


@sio.on('connect')
def connect(sid, environ):
    print('connect ', sid)


@sio.on('msg')
def message(sid, data):
    print('message ', data)


@sio.on('disconnect')
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)

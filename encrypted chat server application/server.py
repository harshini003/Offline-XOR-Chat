from flask import Flask, request, jsonify, render_template_string
import time
import threading

app = Flask(__name__)

# --- RAM STORAGE (Wipes on restart) ---
sessions = {}

# --- THE INTERFACE ---
html_code = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Secure Offline Chat</title>
    <style>
        body { background: #000; color: #00ff00; font-family: monospace; padding: 20px; }
        .box { border: 1px solid #00ff00; height: 300px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; }
        input { width: 100%; padding: 10px; background: #111; color: #fff; border: 1px solid #333; margin-bottom: 5px; }
        button { width: 100%; padding: 10px; background: #004400; color: #fff; border: none; font-weight: bold; }
    </style>
</head>
<body>
    <h2>SECURE ROOM: {{ room_id }}</h2>
    <input type="password" id="key" placeholder="SHARED SECRET KEY (Required)">
    <div class="box" id="chatbox"></div>
    <input type="text" id="msg" placeholder="Type message...">
    <button onclick="send()">ENCRYPT & SEND</button>

    <script>
        const roomId = "{{ room_id }}";
        
        // XOR Encryption
        function xorProcess(text, key) {
            let res = "";
            for (let i = 0; i < text.length; i++) {
                res += String.fromCharCode(text.charCodeAt(i) ^ key.charCodeAt(i % key.length));
            }
            return res;
        }

        async function send() {
            let key = document.getElementById("key").value;
            let msg = document.getElementById("msg").value;
            if (!key) { alert("Enter a Key!"); return; }
            
            await fetch('/send/' + roomId, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ message: xorProcess(msg, key) })
            });
            document.getElementById("msg").value = "";
            load();
        }

        async function load() {
            let key = document.getElementById("key").value;
            let res = await fetch('/get/' + roomId);
            let data = await res.json();
            document.getElementById("chatbox").innerHTML = data.msgs.map(m => 
                `<p>${key ? xorProcess(m, key) : m}</p>`
            ).join("");
        }
        setInterval(load, 2000);
    </script>
</body>
</html>
"""

# --- SERVER LOGIC ---
@app.route('/chat/<room_id>')
def chat_ui(room_id):
    if room_id not in sessions:
        sessions[room_id] = {'msgs': [], 'ts': time.time()}
    return render_template_string(html_code, room_id=room_id)

@app.route('/send/<room_id>', methods=['POST'])
def receive(room_id):
    if room_id in sessions:
        sessions[room_id]['msgs'].append(request.json['message'])
    return jsonify({"status": "ok"})

@app.route('/get/<room_id>')
def get_msg(room_id):
    return jsonify(sessions.get(room_id, {"msgs": []}))

if __name__ == '__main__':
    # Listen on Port 8080 (Safe from Apple/AirPlay conflicts)
    app.run(host='0.0.0.0', port=8080)
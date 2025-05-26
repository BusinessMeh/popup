from flask import Flask, render_template_string
import threading
import webbrowser

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Locked Fullscreen</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #222;
            color: white;
            font-family: Arial, sans-serif;
            overflow: hidden;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        #lock-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.9);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .key-combo {
            background-color: #444;
            color: #0f0;
            padding: 5px 10px;
            border-radius: 4px;
            font-family: monospace;
            margin: 5px;
        }
    </style>
</head>
<body>
    <div id="content">
        <h1>LOCKED FULLSCREEN MODE</h1>
        <p>All exit methods disabled</p>
        <p>Press <span class="key-combo">Ctrl</span> + <span class="key-combo">Shift</span> + <span class="key-combo">X</span> to exit</p>
    </div>

    <script>
        // Immediately enter fullscreen
        function enterFullscreen() {
            const elem = document.documentElement;
            if (!document.fullscreenElement) {
                elem.requestFullscreen().catch(err => {
                    console.error("Fullscreen error:", err);
                });
            }
        }
        
        // Disable ALL keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            // Allow only Ctrl+Shift+X (exit combo)
            if (e.ctrlKey && e.shiftKey && e.key === 'X') {
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                }
                return;
            }
            
            // Block everything else
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            return false;
        }, true);
        
        // Disable right click
        document.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            return false;
        }, true);
        
        // Disable F11, Escape, etc.
        window.addEventListener('keydown', function(e) {
            if ([9, 27, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123].includes(e.keyCode)) {
                e.preventDefault();
                return false;
            }
        }, true);
        
        // Prevent exiting fullscreen via browser UI
        document.addEventListener('fullscreenchange', function() {
            if (!document.fullscreenElement) {
                enterFullscreen();
            }
        });
        
        // Start in fullscreen
        enterFullscreen();
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

def open_browser():
    webbrowser.open_new('http://localhost:5000')

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(port=5000)
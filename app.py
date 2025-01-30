import yt_dlp
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the yt-dlp Video Info API!"

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')  # Get URL from the query string
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    # Options for yt-dlp to extract metadata
    ydl_opts = {
        'quiet': True,  # Suppress normal output
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=False)  # Don't download, just extract info
            # Prepare the response with video details
            video_info = {
                'title': info_dict.get('title'),
                'uploader': info_dict.get('uploader'),
                'description': info_dict.get('description'),
                'duration': info_dict.get('duration'),
                'thumbnail': info_dict.get('thumbnail'),
                'view_count': info_dict.get('view_count'),
                'formats': info_dict.get('formats'),
            }
            return jsonify(video_info)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

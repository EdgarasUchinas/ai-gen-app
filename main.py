
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


# Developers will soon be able to generate images with GPT‑4o via the API, with access rolling out in the next few weeks.

open_ai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    
    message = open_ai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        temperature=1,
        messages=[
            {"role": "system", "content": "You generate dnd 5e character descriptions. Provide a name, race, class, description, and a few key traits. and abilities."},
            {"role": "user", "content": "Generate a character description"}
        ]
    )

    print(message.choices[0].message.content)


    speech_file_path = "character_description.mp3"

    # TODO: Generate speech

    with open_ai_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="ash",
        input=message.choices[0].message.content,
        instructions="Speak in a dark and mysterious tone, filled with warmth like a old storyteller in a fantasy movie.",
    ) as response:
        response.stream_to_file(speech_file_path)



    response = open_ai_client.images.generate(
        model="dall-e-3",
        prompt= "Using the provided description of a DnD character, generate a character sheet image. Please fit everything into the image. All the text descriptions will be provided for you to put into the image. " + message.choices[0].message.content,
        size="1024x1024",
        quality="standard",
        n=1
    )

    # Save the image URL to a file
    with open('image_url.txt', 'w') as f:
        f.write(response.data[0].url)

    # Start a simple HTTP server
    import http.server
    import socketserver
    import socket

    def find_free_port(start_port=8000, max_port=8999):
        for port in range(start_port, max_port + 1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        raise RuntimeError('No free ports available')

    PORT = find_free_port()
    Handler = http.server.SimpleHTTPRequestHandler

    print(f"\nStarting web server at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    main()

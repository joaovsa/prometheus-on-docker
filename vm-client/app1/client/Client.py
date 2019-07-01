from flask import request
import requests
import json

SERVER_URL = 'http://localhost:5000'

class Client:
    def menu(self):
        while True:
            print('1. Get file')
            print('2. Post file')
            print('3. Exit')
            opc = int(input(''))
            
            if opc == 1:
                print('Getting file...')
                response = requests.get(SERVER_URL)
                if response.status_code == 200:
                    print('Success! Check your files folder')
                    # Saving the image in files folder
                    with open('files/cute-dog.jpg', 'wb') as fd:
                        for chunk in response.iter_content(chunk_size=128):
                            fd.write(chunk)
                else:
                    print('Deu ruim')
            if opc == 2:
                print('Sending file...')
                files = {'files': open('./files/tiny-puppy.jpg', 'rb')}
                response = self.postRequest(files, SERVER_URL)
                print(response)

            if opc == 3:
                return 0

    def postRequest(self, files, url):
        headers = {'Content-Type': 'image/jpeg',}
        post = requests.post(url=url, files=files)

        return post.text


if __name__ == '__main__':
    c = Client()
    c.menu()

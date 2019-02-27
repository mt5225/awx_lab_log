'''
curl -X POST -H 'Content-type: text/xml' -d @req.xml http://localhost:7800
'''
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

_DIX_END_POINT = '''http://localhost:7800'''

class Watcher:
    DIRECTORY_TO_WATCH = "/tmp/fetched"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Error"

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print "Received created event - %s." % event.src_path
            post_xml(event.src_path)

        # elif event.event_type == 'modified':
        #     # Taken any action here when a file is modified.
        #     print "Received modified event - %s." % event.src_path

def post_xml(xml_file):
    headers = {'Content-Type':'text/xml'}

    # Open the XML file.
    with open(xml_file) as xml:
        # Give the object representing the XML file to requests.post.
        r = requests.post(_DIX_END_POINT, data=xml, headers=headers)
        print (r.content)

if __name__ == '__main__':
    w = Watcher()
    w.run()
#!/usr/bin/env python
# use Chrome extension: [Host name rewriter](https://chrome.google.com/webstore/detail/host-name-rewriter/kgkjmljnaneinhnbbdhigejjffonhffb)
# "Original host"  "Rewrite to"
# "extract"        "localhost:13131"
# "pr"             "localhost:13131"

import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self, url_request_path: str):
        print(f">>>{url_request_path}")
        target_number: int = MainHandler.convert_to_number(url_request_path)
        while True:
            if target_number < 0:
                # error
                break
            if target_number < 9999:
                print(f"extract {target_number}")
                self.redirect(f"https://group.net/jira/browse/EXTRACT-{target_number}")
                break
            if target_number < 90000:
                print(f"pr {target_number}")
                self.redirect(f"https://group.net/swh/management/pull/{target_number}/files")
                break
            print(f"snow {target_number}")
            self.redirect(
                f"google.com/{target_number}")
            break

    @staticmethod
    def convert_to_number(value: str) -> int:
        try:
            return int(value.split(" ")[0])
        except:
            return -1


def make_app():
    return tornado.web.Application([(r"/(.*)", MainHandler), ])


if __name__ == "__main__":
    app = make_app()
    app.listen(13131)
    tornado.ioloop.IOLoop.instance().start()

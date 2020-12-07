from bs4 import BeautifulSoup
from mitmproxy import ctx


def response(flow):
    with open('injected-test-bypasses.js', 'r') as f:
        content_js = f.read()
        # only process 200 responses of html content
        if flow.response.headers['Content-Type'] != 'text/html':
            return
        if not flow.response.status_code == 200:
            return

        # inject the script tag
        html = BeautifulSoup(flow.response.text, 'lxml')
        container = html.head or html.body
        if container:
            script = html.new_tag('script', type='text/javascript')
            script.string = content_js
            container.insert(0, script)
            flow.response.text = str(html)

            ctx.log.info('Successfully injected the content.js script.')
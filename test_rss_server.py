import time
from flask import Flask, Response

app = Flask(__name__)

RSS_FEED_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>Test RSS Feed</title>
    <link>http://localhost:5000/rss_feed.xml</link>
    <description>A test RSS feed for the Twitter bot app.</description>
    {items}
</channel>
</rss>
'''

ITEM_TEMPLATE = '''
<item>
    <title>Sample Blog Post {post_id}</title>
    <link>http://localhost:5000/sample-post/{post_id}</link>
    <description>This is a sample blog post with "おつかれさまです" in the description.</description>
    <guid>{post_id}</guid>
</item>
'''

def generate_rss_feed():
    current_time = int(time.time())
    post_interval = 5
    post_count = current_time // post_interval
    items = "".join(ITEM_TEMPLATE.format(post_id=i) for i in range(post_count, post_count - 5, -1))
    return RSS_FEED_TEMPLATE.format(items=items)

@app.route('/rss_feed.xml')
def rss_feed():
    return Response(generate_rss_feed(), content_type='application/rss+xml')

if __name__ == '__main__':
    app.run(debug=True)


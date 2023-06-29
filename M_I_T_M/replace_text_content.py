from mitmproxy import http


def response(flow: http.HTTPFlow) -> None:
    # if flow.request.pretty_url == "https://example.com/path":
    #     flow.response = http.HTTPResponse.make(
    #         200, # (optional) status code
    #         b"Hello World" , # (optional) content
    #         {"Content-Type" : "text/html"} # ( optional) content
    #     )
    if flow.request.pretty_url == "testphp.vulnweb.com":
        # b is byte  or other wise you put .encode()
        # text we convert into number
        # To add n number of changes 
        flow.response.content=flow.response.content.replace(b"artists",b"sanjaykumar")
        flow.response.content = flow.response.content.replace(b"Apache2", b"Pulsar2")




# run $: mitmproxy -s filename.py

#  after you find any error : run  in mitmproxy : console.view.eventlog
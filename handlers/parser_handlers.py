import handlers
from tools import youku_parser

class YoukuParserHandler(handlers.BasePageHandler):

    def get(self):
        elements = youku_parser.parse_url( None )
        for element in elements:
            self.response.out.write(element)
        
            

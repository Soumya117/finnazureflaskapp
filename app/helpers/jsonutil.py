class JsonUtil:
    def __init__(self, result, data):
        self.result = result
        self.data = data
        self.result['link'] = self.data['link']

    def prepare_json(self, output=None, price=None):
        if output is None:
            output = self.result
        if price:
            self.result['price'] = price
        output['text'] = self.data['text']
        output['address'] = self.data['address']
        output['geocode'] = self.data['geocode']
        output['area'] = self.data['area']

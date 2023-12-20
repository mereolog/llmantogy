import re


class Symbol:
    def __init__(self, origin_value:object, origin_type=str):
        self.origin = origin_value
        self.origin_type = origin_type
        self.__set_symbol_letter()
        
    def __set_symbol_letter(self):
        self.value = str(self.origin)

    def to_tptp(self):
        pass
    
    @staticmethod
    def escape_tptp_chars(text: str):
        text = text.replace('-', '_')
        text = text.replace('+', '_')
        text = text.replace('.', '_')
        text = text.replace('/', '_')
        text = text.replace('!', '_')
        text = text.replace(':', '_')
        text = text.replace(';', '_')
        text = text.replace('?', '_')
        text = text.replace('=', '_')
        text = text.replace('%', '_')
        text = text.replace('&', '_')
        text = text.replace('$', '_')
        text = text.replace('@', '_')
        text = text.replace('|', '_')
        text = text.replace("'", '_')
        text = text.replace('"', '_')
        text = text.replace(' ', '_')
        text = text.replace('(', '_')
        text = text.replace(')', '_')
        text = text.replace('>', '_')
        text = text.replace('~', '_')
        text = text.replace('#', '_')
        text = text.replace(',', '_')
        text = text.replace('*', '_')
        text = text.replace('^', '_')
        text = text.replace('{', '_')
        text = text.replace('}', '_')
        text = text.replace('[', '_')
        text = text.replace(']', '_')
        text = text.replace('\n', '')
        text = text.replace('\t', '')
        text = re.sub(r'[^\x00-\x7F]+', '_', text)
        if text[0] == '<=':
            text = 'leq' + text[1:]
        if text[0] == '>=':
            text = 'geq' + text[1:]
        if text[0] == '<':
            text = 'le' + text[1:]
        if text[0] == '>':
            text = 'ge' + text[1:]
        if not text[0].isalpha():
            text = 's' + text
        return text
        
    def __repr__(self):
        return self.value
    
    def __eq__(self, other):
        if not isinstance(other, Symbol):
            return False
        if isinstance(other, Symbol):
            return self.value == other.value and self.origin_type == self.origin_type
    
    def __hash__(self):
        return (str(self.value)+str(self.origin_type)).__hash__()
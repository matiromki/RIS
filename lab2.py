class Tokenizer:
    def __init__(self, input_string):
        self.tokens = self._generate_tokens(input_string)
        self.current_position = 0

    def _generate_tokens(self, input_string):
        reserved_symbols = {";", ")", "(", "&&", "||", "true", "false", "*", "/", "+", "-", "int", "bool", "char", "end", "const", "function"}
        words = input_string.split()
        return [self.get_token_type(word, reserved_symbols) for word in words] + ["end"]

    def get_token_type(self, word, reserved_symbols):
        return {True: "const", False: "var:"}.get(word.isdigit(), word if word in reserved_symbols else "var:")

    def current_token(self):
        return self.tokens[self.current_position] if self.current_position < len(self.tokens) else None

    def accept(self, expected_token):
        return {True: lambda: setattr(self, "current_position", self.current_position + 1)}.get(self.tokens[self.current_position] == expected_token, lambda: None)()

    def raise_error(self, token, valid_tokens):
        {True: lambda: (_ for _ in ()).throw(ValueError(f"Ошибка синтаксиса: Неожиданный токен '{token}'. Допустимые токены: {valid_tokens}"))}.get(token not in valid_tokens, lambda: None)()

    def is_valid(self, token, valid_tokens):
        return token in valid_tokens


class StateHandler:
    def __init__(self, current_state, token, next_state, stack, tokenizer, valid_tokens):
        self.current_state = current_state
        self.token = token
        self.next_state = next_state
        self.stack = stack
        self.tokenizer = tokenizer
        self.valid_tokens = valid_tokens

    def execute(self, action):
        return {
            "handle_0_0_0_0": lambda: self.next_state,
            "handle_0_0_0_1": lambda: self.tokenizer.raise_error(self.token, self.valid_tokens) or self.next_state,
            "handle_0_1_0_1": lambda: self.stack.append(self.current_state + 1) or self.next_state,
            "handle_0_0_1_1": lambda: self.tokenizer.accept(self.token) or self.next_state,
            "handle_1_0_0_1": lambda: self.stack.pop() if self.stack else self.next_state,
            "handle_1_0_1_1": lambda: self.tokenizer.accept(self.token) or (self.stack.pop() if self.stack else self.next_state)
        }[action]()


class LL1:
    def __init__(self, transition_table):
        self.transition_table = transition_table
        self.current_state = 1
        self.stack = []
        self.tokenizer = None
        self.action_map = {
            (info[2], info[3], info[4], info[5]): f"handle_{info[2]}_{info[3]}_{info[4]}_{info[5]}"
            for state, info in transition_table.items()
        }

    def analyze(self, tokens):
        self.tokenizer = Tokenizer(" ".join(tokens))
        current_token = self.tokenizer.current_token()
        
        while current_token:
            {True: lambda: print("Парсинг завершен успешно.") or exit()}.get(current_token == 'end' and not self.stack, lambda: None)()
            
            state_info = self.transition_table[self.current_state]
            valid_tokens, next_state = state_info[:2]
            
            self.current_state = {
                True: lambda: self.current_state + 1,
                False: lambda: StateHandler(self.current_state, current_token, next_state, self.stack, self.tokenizer, valid_tokens).execute(self.action_map[(state_info[2], state_info[3], state_info[4], state_info[5])])
            }[not self.tokenizer.is_valid(current_token, valid_tokens) and state_info[5] == 0]()
            
            current_token = self.tokenizer.current_token()
        
        print("Грамматика верна")

transitions = {
    1: ['end ) ( const var: true false function && number', 19, 0, 0, 0, 1],
    2: ['* /', 22, 0, 0, 0, 0],
    3: ['end ) && ', 25, 0, 0, 0, 1],
    4: ['( const var: true false function number', 26, 0, 0, 0, 1],
    5: ['+ -', 28, 0, 0, 0, 0],
    6: ['* / ) && end', 31, 0, 0, 0, 1],
    7: ['(', 32, 0, 0, 0, 0],
    8: ['const', 35, 0, 0, 0, 0],
    9: ['true false', 36, 0, 0, 0, 0],
    10: ['var:', 37, 0, 0, 0, 0],
    11: ['function', 38, 0, 0, 0, 1],
    12: ['function', 39, 0, 0, 0, 1],
    13: [';', 43, 0, 0, 0, 0],
    14: ['):', 46, 0, 0, 0, 1],
    15: ['var:', 48, 0, 0, 0, 1],
    16: ['int bool char', 50, 0, 0, 0, 1],
    17: ['&& ', 51, 0, 0, 0, 0],
    18: ['&& * / + - ) end', 53, 0, 0, 0, 1],
    19: ['( const var: true false function number', 4, 0, 1, 0, 1],
    20: ['* / ) end', 2, 0, 1, 0, 1],
    21: ['&& * / + - ) end', 17, 0, 0, 0, 1],
    22: ['* /', 23, 0, 0, 1, 1],
    23: ['( const var: true false function number', 4, 0, 1, 0, 1],
    24: ['* / ) && end', 2, 0, 0, 0, 1],
    25: ['end ) && ', -1, 1, 0, 0, 1],
    26: ['( const var: true false function number', 7, 0, 1, 0, 1],
    27: ['+ - * / ) && end', 5, 0, 0, 0, 0],
    28: ['+ -', 29, 0, 0, 1, 1],
    29: ['( const var: true false function number', 7, 0, 1, 0, 1],
    30: ['+ - * / ) end', 5, 0, 0, 0, 1],
    31: ['* / ) && end', -1, 1, 0, 0, 1],
    32: ['(', 33, 0, 0, 1, 1],
    33: ['end ) ( const var: true false function && number', 1, 0, 1, 0, 1],
    34: [')', -1, 1, 0, 1, 1],
    35: ['const', -1, 1, 0, 1, 1],
    36: ['true false', -1, 1, 0, 1, 1],
    37: ['var:', 15, 0, 0, 0, 1],
    38: ['function', 12, 0, 0, 0, 1],
    39: ['function', 40, 0, 0, 1, 1],
    40: ['(', 41, 0, 0, 1, 1],
    41: ['var:', 15, 0, 1, 0, 1],
    42: ['; ):', 13, 0, 0, 0, 1],
    43: [';', 44, 0, 0, 1, 1],
    44: ['var:', 15, 0, 1, 0, 1],
    45: ['; ):', 13, 0, 0, 0, 1],
    46: ['):', 47, 0, 0, 1, 1],
    47: ['int bool char', 16, 0, 0, 0, 1],
    48: ['int bool char', 49, 0, 0, 1, 1],
    49: ['int bool char', 16, 0, 0, 0, 1],
    50: ['int bool char', -1, 1, 0, 1, 1],
    51: ['&& ', 52, 0, 0, 1, 1],
    52: ['end ) ( const var: true false function && number', 1, 0, 0, 0, 1],
    53: ['&& * / + - ) end', -1, 1, 0, 0, 1]
}

# Запуск парсера
input_expression = "( 5 ) + 1"
tokenizer_instance = Tokenizer(input_expression)
tokens = tokenizer_instance.tokens

parser_instance = LL1(transitions)
parser_instance.analyze(tokens)

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum TokenType {
    // Single-character tokens.
    TOKEN_LEFT_PAREN, TOKEN_RIGHT_PAREN,
    TOKEN_LEFT_BRACE, TOKEN_RIGHT_BRACE,
    TOKEN_COMMA, TOKEN_DOT, TOKEN_MINUS, TOKEN_PLUS,
    TOKEN_SEMICOLON, TOKEN_SLASH, TOKEN_STAR,
    // One or two character tokens.
    TOKEN_BANG, TOKEN_BANG_EQUAL,
    TOKEN_EQUAL, TOKEN_EQUAL_EQUAL,
    TOKEN_GREATER, TOKEN_GREATER_EQUAL,
    TOKEN_LESS, TOKEN_LESS_EQUAL,
    // Literals.
    TOKEN_IDENTIFIER, TOKEN_STRING, TOKEN_NUMBER,
    // Keywords.
    TOKEN_AND, TOKEN_CLASS, TOKEN_ELSE, TOKEN_FALSE,
    TOKEN_FOR, TOKEN_FUN, TOKEN_IF, TOKEN_NIL, TOKEN_OR,
    TOKEN_PRINT, TOKEN_RETURN, TOKEN_SUPER, TOKEN_THIS,
    TOKEN_TRUE, TOKEN_VAR, TOKEN_WHILE,

    TOKEN_ERROR, TOKEN_EOF
}

pub struct Token {
    pub token_type: TokenType,
    pub line: i32,
    pub start: usize,
    pub length: usize,
}

pub struct Scanner {
    source_code: Vec<char>,
    start: usize,
    current: usize,
    line: i32,
}

static keyword_array:[(&str, TokenType);16] = [
    ("and", TokenType::TOKEN_AND),
    ("class", TokenType::TOKEN_CLASS),
    ("else", TokenType::TOKEN_ELSE),
    ("if", TokenType::TOKEN_IF),
    ("nil", TokenType::TOKEN_NIL),
    ("or", TokenType::TOKEN_OR),
    ("print", TokenType::TOKEN_PRINT),
    ("return", TokenType::TOKEN_RETURN),
    ("super", TokenType::TOKEN_SUPER),
    ("var", TokenType::TOKEN_VAR),
    ("while", TokenType::TOKEN_WHILE),
    ("false", TokenType::TOKEN_FALSE),
    ("for", TokenType::TOKEN_FOR),
    ("fun", TokenType::TOKEN_FUN),
    ("this", TokenType::TOKEN_THIS),
    ("true", TokenType::TOKEN_TRUE),
];

impl Scanner {
    pub fn init(source_code: &String) -> Self {
        Scanner {
            source_code: source_code.chars().collect(),
            start: 0,
            current: 0,
            line: 1,
        }
    }

    pub fn token_chars(&self, length: usize) -> String {
        let mut s = String::new();
        for i in self.current..self.current + length {
            s.push(self.source_code[i]);
        }
        return s
    }

    fn is_at_end(&self) -> bool {
        self.source_code[self.current] == '\0'
    }

    fn error_token(&self, error_message:&str) -> Token {
        print!("FAILURE: line={:?} error={:?}", self.line, error_message);
        Token {
            token_type: TokenType::TOKEN_ERROR,
            line: self.line,
            start: self.start,
            length: 0,
        }
    }

    fn make_token(&self, token_type: TokenType) -> Token {
        Token {
            token_type: token_type,
            line: self.line,
            start: self.start,
            length: self.current - self.start,
        }
    }

    fn match_char(&mut self, expected: char) -> bool {
        if self.is_at_end() {
            return false;
        }

        if self.source_code[self.current] != expected {
            return false;
        }

        self.current += 1;
        return true;
    }

    fn is_digit(&self, c: char) -> bool {
        c >= '0' && c <= '9'
    }

    fn is_alpha(&self, c: char) -> bool {
        (c >= 'a' && c <= 'z') ||
        (c >= 'A' && c <= 'Z') ||
         c == '_'
    }

    fn peek(&self) -> char {
        self.source_code[self.current]
    }

    fn peek_next(&self) -> char {
        if self.is_at_end() {
            return '\0';
        }
        self.source_code[self.current + 1]
    }

    fn number(&mut self) -> Token {
        while self.is_digit(self.peek()) {
            self.advance();
        }

        if self.peek() == '.' && self.is_digit(self.peek_next()) {
            self.advance();
            while self.is_digit(self.peek()) { self.advance(); };
        }

        return self.make_token(TokenType::TOKEN_NUMBER);
    }

    fn check_keyword(
        &self,
        start: usize,
        length: usize,
        word:&str,
        expected_type: TokenType) -> bool
    {
        let l = word.chars();
        let r = self.source_code[start..start + length].iter();
        std::iter::zip(l, r).fold(true, |acc, x| acc && match x {
            (a, b) => a == *b,
        })
    }

    fn identifier_type(&mut self, start: usize) -> TokenType {
        for (keyword, token) in keyword_array.iter() {
            if self.check_keyword(start, keyword.len(), keyword, *token) {
                return *token;
            }
        }
        TokenType::TOKEN_IDENTIFIER
    }

    fn identifier(&mut self) -> Token {
        let start = self.current;
        while self.is_alpha(self.peek()) || self.is_digit(self.peek()) {
            self.advance();
        }
        let id_type = self.identifier_type(start);
        return self.make_token(id_type);
    }

    fn string(&mut self) -> Token {
        while self.peek() != '"' && !self.is_at_end() {
            if self.peek() == '\n' {
                self.line += 1;
            }
            self.advance();
        }

        if self.is_at_end() {
            return self.error_token("Unterminated string");
        }

        self.advance();
        return self.make_token(TokenType::TOKEN_STRING);
    }

    fn skip_whitespace(&mut self) -> () {
        loop {
            match self.peek() {
                ' ' | '\r' | '\t' => { self.advance(); },
                '\n' => {
                    self.line += 1;
                    self.advance();
                },
                // Treat comments as whitespace
                '/' => {
                    if self.peek_next() == '/' {
                        while self.peek() != '\n' && !self.is_at_end() {
                            self.advance();
                        }
                    } else {
                        return;
                    }
                },
                _ => return,
            };
        }
    }

    fn advance(&mut self) -> char {
        self.current += 1;
        self.source_code[self.current - 1]
    }

    pub fn scan_token(&mut self) -> Token {
        self.start = self.current;
        if self.is_at_end() {
            return self.make_token(TokenType::TOKEN_EOF);
        }

        if self.is_alpha(self.peek()) {
            return self.identifier();
        }

        if self.is_digit(self.peek()) {
            return self.number();
        }

        match self.advance() {
            '(' => return self.make_token(TokenType::TOKEN_LEFT_PAREN),
            ')' => return self.make_token(TokenType::TOKEN_RIGHT_PAREN),
            '{' => return self.make_token(TokenType::TOKEN_LEFT_BRACE),
            '}' => return self.make_token(TokenType::TOKEN_RIGHT_BRACE),
            ';' => return self.make_token(TokenType::TOKEN_SEMICOLON),
            ',' => return self.make_token(TokenType::TOKEN_COMMA),
            '.' => return self.make_token(TokenType::TOKEN_DOT),
            '-' => return self.make_token(TokenType::TOKEN_MINUS),
            '+' => return self.make_token(TokenType::TOKEN_PLUS),
            '/' => return self.make_token(TokenType::TOKEN_SLASH),
            '*' => return self.make_token(TokenType::TOKEN_STAR),
            '"' => return self.string(),
            '!' => {
                let t = if self.match_char('=') { TokenType::TOKEN_BANG_EQUAL } else { TokenType::TOKEN_BANG };
                return self.make_token(t);
            },
            '=' => {
                let t = if self.match_char('=') { TokenType::TOKEN_EQUAL_EQUAL } else { TokenType::TOKEN_EQUAL};
                return self.make_token(t);
            },
            '<' =>{
                let t = if self.match_char('=') { TokenType::TOKEN_LESS_EQUAL } else { TokenType::TOKEN_LESS };
                return self.make_token(t);
            }
            '>' =>{
                let t = if self.match_char('=') { TokenType::TOKEN_GREATER_EQUAL } else { TokenType::TOKEN_GREATER };
                return self.make_token(t);
            }
            _ => (),
        }

        self.error_token("Unexpected character.")
   }
}

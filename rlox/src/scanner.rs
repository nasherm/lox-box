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

#[derive(Debug)]
pub struct Token {
    pub token_type: TokenType,
    pub line: i32,
    pub start: usize,
    pub length: usize,
    pub option_string: Option<String>,
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
        for i in self.current-length..self.current {
            s.push(self.source_code[i]);
        }
        return s
    }

    fn is_at_end(&self) -> bool {
        if self.current >= self.source_code.len() {
            return true
        }
        self.source_code[self.current] == '\0'
    }

    fn error_token(&self, error_message:&str) -> Token {
        Token {
            token_type: TokenType::TOKEN_ERROR,
            line: self.line,
            start: self.start,
            length: 0,
            option_string: Some(String::from(error_message)),
        }
    }

    fn make_token(&self, token_type: TokenType) -> Token {
        let option_string = match token_type {
            TokenType::TOKEN_STRING |
            TokenType::TOKEN_NUMBER |
            TokenType::TOKEN_IDENTIFIER => Some(self.token_chars(self.current - self.start)),
            _ => None,
        };
        Token {
            token_type: token_type,
            line: self.line,
            start: self.start,
            length: self.current - self.start,
            option_string: option_string,
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
        if self.is_at_end() {
            return '\0';
        }
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
        if self.start + length >= self.source_code.len() {
            return false
        }
        let l = word.chars();
        let r = self.source_code[start..start + length].iter();
        std::iter::zip(l, r).fold(true, |acc, x| acc && match x {
            (a, b) => a == *b,
        })
    }

    fn identifier_type(&mut self, start: usize) -> Option<(TokenType, usize)> {
        for (keyword, token) in keyword_array.iter() {
            if self.check_keyword(start, keyword.len() - 1, keyword, *token) {
                return Some((*token, keyword.len()));
            }
        }
        None
    }

    fn identifier(&mut self) -> Token {
        let start = self.current;
        let token = match self.identifier_type(start) {
            Some((token, len)) => {
                self.current += len;
                token
            },
            _ => {
                while self.is_alpha(self.peek()) { self.advance(); }
                TokenType::TOKEN_IDENTIFIER
            }
        };

        return self.make_token(token);
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

#[cfg(test)]
mod tests {
    use crate::scanner::{Scanner, Token, TokenType};
    fn drive_tokens(test_string:&str) -> Vec<Token> {
        let input_string = String::from(test_string);
        let mut scanner = Scanner::init(&input_string);
        let mut scanned_tokens: Vec<Token> = Vec::new();
        loop {
            let token = scanner.scan_token();
            if token.token_type == TokenType::TOKEN_EOF {
                break
            }
            scanned_tokens.push(token);
        }
        scanned_tokens
    }

    #[test]
    fn simple_tokens() {
        let scanned_tokens = drive_tokens("(){};,.-+/*");
        assert_eq!(scanned_tokens[0].token_type, TokenType::TOKEN_LEFT_PAREN);
        assert_eq!(scanned_tokens[1].token_type, TokenType::TOKEN_RIGHT_PAREN);
        assert_eq!(scanned_tokens[2].token_type, TokenType::TOKEN_LEFT_BRACE);
        assert_eq!(scanned_tokens[3].token_type, TokenType::TOKEN_RIGHT_BRACE);
        assert_eq!(scanned_tokens[4].token_type, TokenType::TOKEN_SEMICOLON);
        assert_eq!(scanned_tokens[5].token_type, TokenType::TOKEN_COMMA);
        assert_eq!(scanned_tokens[6].token_type, TokenType::TOKEN_DOT);
        assert_eq!(scanned_tokens[7].token_type, TokenType::TOKEN_MINUS);
        assert_eq!(scanned_tokens[8].token_type, TokenType::TOKEN_PLUS);
        assert_eq!(scanned_tokens[9].token_type, TokenType::TOKEN_SLASH);
        assert_eq!(scanned_tokens[10].token_type, TokenType::TOKEN_STAR);
    }

    #[test]
    fn conditional_tokens() {
        let scanned_tokens = drive_tokens("!!=><>=<====");
        assert_eq!(scanned_tokens[0].token_type, TokenType::TOKEN_BANG);
        assert_eq!(scanned_tokens[1].token_type, TokenType::TOKEN_BANG_EQUAL);
        assert_eq!(scanned_tokens[2].token_type, TokenType::TOKEN_GREATER);
        assert_eq!(scanned_tokens[3].token_type, TokenType::TOKEN_LESS);
        assert_eq!(scanned_tokens[4].token_type, TokenType::TOKEN_GREATER_EQUAL);
        assert_eq!(scanned_tokens[5].token_type, TokenType::TOKEN_LESS_EQUAL);
        assert_eq!(scanned_tokens[6].token_type, TokenType::TOKEN_EQUAL_EQUAL);
        assert_eq!(scanned_tokens[7].token_type, TokenType::TOKEN_EQUAL);
    }

    #[test]
    fn string_tokens() {
        let scanned_tokens = drive_tokens("\"Hello, world!\"");
        assert_eq!(scanned_tokens[0].token_type, TokenType::TOKEN_STRING);
        assert_eq!(scanned_tokens[0].option_string, Some(String::from("\"Hello, world!\"")));
    }

    #[test]
    fn numeric_tokens() {
        let scanned_tokens = drive_tokens("3.14159542");
        assert_eq!(scanned_tokens[0].token_type, TokenType::TOKEN_NUMBER);
        assert_eq!(scanned_tokens[0].option_string, Some(String::from("3.14159542")));
    }

    #[test]
    fn identifier_tokens() {
        let scanned_tokens = drive_tokens("my_random_func");
        assert_eq!(scanned_tokens[0].token_type, TokenType::TOKEN_IDENTIFIER);
        assert_eq!(scanned_tokens[0].option_string, Some(String::from("my_random_func")));
    }

    #[test]
    fn keyword_tokens() {
        let test_string ="andclasselseifnilorprintreturnsupervarwhilefalseforfunthistrue";
        let scanned_tokens = drive_tokens(test_string);
        assert_eq!(scanned_tokens[0].token_type, TokenType::TOKEN_AND);
        assert_eq!(scanned_tokens[1].token_type, TokenType::TOKEN_CLASS);
        assert_eq!(scanned_tokens[2].token_type, TokenType::TOKEN_ELSE);
        assert_eq!(scanned_tokens[3].token_type, TokenType::TOKEN_IF);
        assert_eq!(scanned_tokens[4].token_type, TokenType::TOKEN_NIL);
        assert_eq!(scanned_tokens[5].token_type, TokenType::TOKEN_OR);
        assert_eq!(scanned_tokens[6].token_type, TokenType::TOKEN_PRINT);
        assert_eq!(scanned_tokens[7].token_type, TokenType::TOKEN_RETURN);
        assert_eq!(scanned_tokens[8].token_type, TokenType::TOKEN_SUPER);
        assert_eq!(scanned_tokens[9].token_type, TokenType::TOKEN_VAR);
        assert_eq!(scanned_tokens[10].token_type, TokenType::TOKEN_WHILE);
        assert_eq!(scanned_tokens[11].token_type, TokenType::TOKEN_FALSE);
        assert_eq!(scanned_tokens[12].token_type, TokenType::TOKEN_FOR);
        assert_eq!(scanned_tokens[13].token_type, TokenType::TOKEN_FUN);
        assert_eq!(scanned_tokens[14].token_type, TokenType::TOKEN_THIS);
        assert_eq!(scanned_tokens[15].token_type, TokenType::TOKEN_TRUE);
    }
}

#[derive(Debug, PartialEq)]
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
    pub line: i32,
    pub token_type: TokenType,
    pub start: u32,
    pub string: String,
}

pub struct Scanner {
    source_code: String,
    start: u32,
    current: u32,
    line: i32,
}

impl Scanner {
    pub fn init(source_code: &String) -> Self {
        Scanner {
            source_code: source_code.clone(),
            start: 0,
            current: 0,
            line: 1,
        }
    }

    pub fn scan_token(&self) -> Token {
        Token {
            line: 0,
            token_type: TokenType::TOKEN_EOF,
            start: 0,
            string: String::from(""),
        }
    }
}

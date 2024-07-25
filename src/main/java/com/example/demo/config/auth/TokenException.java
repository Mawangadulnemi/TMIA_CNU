package com.example.demo.config.auth;

import com.example.demo.exception.CustomException;
import com.example.demo.exception.ErrorCode;

public class TokenException extends CustomException {

    public TokenException(ErrorCode errorCode) {
        super(errorCode);
    }
}

package com.example.demo.controller;

import com.example.demo.dto.request.auth.LoginForm;
import com.example.demo.dto.request.auth.SignUpForm;
import com.example.demo.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseCookie;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @ResponseStatus(HttpStatus.CREATED)
    @PostMapping("/signup")
    public void signUp(@Valid SignUpForm signUpForm) {
        authService.signUp(signUpForm);
    }

    @PostMapping("/login")
    public ResponseEntity<Void> login(@Valid LoginForm loginForm) {
        String token = authService.login(loginForm);
        ResponseCookie cookie = ResponseCookie.from("token", token)
            .httpOnly(true)
            .maxAge(2 * 60 * 60)
            .path("/")
            .build();
        return ResponseEntity.ok()
//            .header(HttpHeaders.AUTHORIZATION, token)
            .header(HttpHeaders.SET_COOKIE, cookie.toString())
            .build();
    }
}

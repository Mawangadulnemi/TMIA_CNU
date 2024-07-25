package com.example.demo.config.auth;

import com.example.demo.util.JwtProvider;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseCookie;
import org.springframework.security.core.Authentication;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

@RequiredArgsConstructor
@Component
public class OAuth2SuccessHandler implements AuthenticationSuccessHandler {

    private final JwtProvider jwtProvider;

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request, HttpServletResponse response,
        Authentication authentication) throws IOException {
        String accessToken = jwtProvider.generateToken(authentication);

        ResponseCookie cookie = ResponseCookie.from("token", accessToken)
            .httpOnly(true)
            .maxAge(2 * 60 * 60)
            .path("/")
            .build();
        response.setHeader(HttpHeaders.AUTHORIZATION, accessToken);
        response.setHeader(HttpHeaders.SET_COOKIE, cookie.toString());
        response.sendRedirect("/");
    }
}

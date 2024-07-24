package com.example.demo.service;

import com.example.demo.dto.request.auth.LoginForm;
import com.example.demo.dto.request.auth.SignUpForm;
import com.example.demo.entity.Role;
import com.example.demo.entity.User;
import com.example.demo.repository.UserRepository;
import com.example.demo.util.JwtProvider;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtProvider jwtProvider;

    public AuthService(UserRepository userRepository, PasswordEncoder passwordEncoder,
        JwtProvider jwtProvider) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtProvider = jwtProvider;
    }

    public void signUp(SignUpForm signUpForm) {

        signUpForm.setRole(Role.GUEST);

        userRepository.save(signUpForm.toEntity());
    }

    public String login(LoginForm loginForm) {

        User user = userRepository.findByEmail(loginForm.getEmail())
            .orElseThrow(IllegalArgumentException::new);

        if (!passwordEncoder.matches(loginForm.getPassword(), user.getPassword())) {
            throw new IllegalArgumentException();
        }

        return null;
        //return jwtProvider.generateToken(user.getId(), user.getRole());
    }
}

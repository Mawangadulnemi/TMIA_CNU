package com.example.demo.service;

import com.example.demo.dto.request.auth.LoginForm;
import com.example.demo.dto.request.auth.SignUpForm;
import com.example.demo.entity.Member;
import com.example.demo.entity.MemberRole;
import com.example.demo.repository.MemberRepository;
import com.example.demo.util.JwtProvider;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {

    private final MemberRepository memberRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtProvider jwtProvider;

    public AuthService(MemberRepository memberRepository, PasswordEncoder passwordEncoder,
        JwtProvider jwtProvider) {
        this.memberRepository = memberRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtProvider = jwtProvider;
    }

    public void signUp(SignUpForm signUpForm) {

        if (signUpForm.getRole() == MemberRole.ADMIN) {
            throw new IllegalArgumentException();
        }

        memberRepository.save(signUpForm.toEntity());
    }

    public String login(LoginForm loginForm) {

        Member member = memberRepository.findByEmail(loginForm.getEmail())
            .orElseThrow(IllegalArgumentException::new);

        if (!passwordEncoder.matches(loginForm.getPassword(), member.getPassword())) {
            throw new IllegalArgumentException();
        }

        return jwtProvider.generateToken(member.getId(), member.getRole());
    }
}

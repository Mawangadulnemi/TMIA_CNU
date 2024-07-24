package com.example.demo.dto.request.auth;

import com.example.demo.entity.Role;
import com.example.demo.entity.User;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class SignUpForm {

    @NotBlank
    @Email
    private String email;

    @NotBlank
    private String password;


    @Size(min = 1, max = 15)
    @NotBlank
    private String name;

    private Role role;

    public void setRole(Role role) {
        this.role = role;
    }

    public User toEntity() {
        return User.builder()
            .email(this.email)
            .password(this.password)
            .name(this.name)
            .role(this.role).build();
    }
}

package com.example.demo.dto.request.auth;

import com.example.demo.entity.Member;
import com.example.demo.entity.MemberRole;
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

    @NotNull
    private MemberRole role;

    public Member toEntity() {
        return new Member(this.email, this.password, this.name, this.role);
    }
}

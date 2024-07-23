package com.example.demo.config.auth.dto;

import com.example.demo.entity.Role;
import com.example.demo.entity.User;
import lombok.Getter;

@Getter
public class UserDto {

    private Long id;
    private String name;
    private String email;
    private Role role;

    public UserDto(User user) {
        this.id = user.getId();
        this.name = user.getName();
        this.email = user.getEmail();
        this.role = user.getRole();
    }

}

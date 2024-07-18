package com.example.demo.dto.request.conversation;

import jakarta.validation.constraints.NotNull;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import org.springframework.web.multipart.MultipartFile;

@Getter
@Setter
@NoArgsConstructor
public class UploadVoiceRequestDto {

    @NotNull
    private MultipartFile file;
}

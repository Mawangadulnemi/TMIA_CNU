package com.example.demo.dto.response.conversation;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class SimilarityResponseDto {
    String text;
    Integer index;

}

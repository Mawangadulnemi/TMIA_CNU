package com.example.demo.dto.response.conversation;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.ToString;

@Getter
@AllArgsConstructor
@ToString
public class SimilarityResponseDto {
    String text;
    Integer index;

}

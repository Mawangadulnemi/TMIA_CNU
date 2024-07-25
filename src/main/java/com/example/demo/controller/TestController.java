package com.example.demo.controller;

import static org.springframework.http.MediaType.APPLICATION_JSON;

import com.example.demo.dto.request.conversation.SimilarityRequestDto;
import com.example.demo.dto.response.conversation.STTResponseDto;
import com.example.demo.dto.response.conversation.SimilarityResponseDto;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.nio.file.Path;
import lombok.extern.slf4j.Slf4j;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.HttpStatusCode;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.server.ResponseStatusException;

@Slf4j
@RestController
public class TestController {

    @GetMapping("/api-test")
    public String test() {
        Resource resource = new ClassPathResource("static/video/아이유.wav");
        System.out.println("resource.exists() = " + resource.exists());

        RestTemplate restTemplate = new RestTemplate();

        String url = "http://3.34.227.229:5001/transcribe/";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", resource);


        HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(body, headers);

        ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.POST, entity, String.class);
        System.out.println("response.getStatusCode() = " + response.getStatusCode());

        String text = response.getBody();

        if (text == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        }
        return text;
    }

    @GetMapping("/api-test2/{q}")
    public String test2(@PathVariable String q) {
        System.out.println("q = " + q);
        RestClient restClient = RestClient.create();
        SimilarityResponseDto similarityResponseDto = restClient.post()
            .uri("http://3.39.170.111:8001/speaking-style")
            .contentType(APPLICATION_JSON)
            .body(new SimilarityRequestDto(q))
            .retrieve()
            .onStatus(HttpStatusCode::is4xxClientError, ((request, response) -> {
                throw new ResponseStatusException(HttpStatus.NOT_FOUND, q);
            }))
            .body(SimilarityResponseDto.class);

        log.info("유사도검사 결과: {}", similarityResponseDto);
        return similarityResponseDto != null ? similarityResponseDto.getText() : "null";
    }
}

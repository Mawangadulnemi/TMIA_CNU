package com.example.demo.controller;

import com.example.demo.dto.request.conversation.SimilarityRequestDto;
import com.example.demo.dto.request.conversation.UploadVoiceRequestDto;
import com.example.demo.dto.response.conversation.STTResponseDto;
import com.example.demo.dto.response.conversation.SimilarityResponseDto;
import com.example.demo.service.ConversationService;
import jakarta.validation.Valid;
import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.FileSystemResource;
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
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.server.ResponseStatusException;

@Slf4j
@RestController
@RequestMapping("/api/conversation")
public class conversationController {

    private final ConversationService conversationService;

    public conversationController(ConversationService conversationService) {
        this.conversationService = conversationService;
    }

    @GetMapping
    public List<Character> getCharacterList() {
        return new ArrayList<>();
    }

//    @GetMapping("/{id}")
//    public ResponseEntity<Resource> getDefaultVideo(@PathVariable Long id) {
//        return ResponseEntity.ok()
//            .header(HttpHeaders.CONTENT_TYPE, "video/mp4")
//            .body(resource);
//    }

    @GetMapping("/{id}")
    public ResponseEntity<Resource> getResponseVideo(@RequestParam Integer q) {

        Resource video = new ClassPathResource("static/video/" + q + ".mp4");

        if (!video.exists()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        }

        return ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_TYPE, "video/mp4")
            .body(video);
    }

    @PostMapping("/{id}")
    public ResponseEntity<Resource> uploadVoiceFile(
        @Valid @ModelAttribute UploadVoiceRequestDto requestDto) {

        MultipartFile requestVoice = requestDto.getFile();
        Path questionVoice;
        try {
            Path tempDir = conversationService.getTempDir();
            questionVoice = conversationService.saveFile(tempDir, requestVoice);
        } catch (IOException e) {
            log.warn("파일 업로드 실패: {}", e.getMessage());
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
        }

        RestTemplate restTemplate = new RestTemplate();

        String url = "http://3.34.227.229:5001/transcribe/";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        Resource voice = new FileSystemResource(questionVoice);
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", voice);


        HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(body, headers);

        STTResponseDto sttResponse = restTemplate.postForObject(url, entity, STTResponseDto.class);

        if (sttResponse == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        }

        String voiceText = sttResponse.getText();

        if (voiceText.isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "빈 질문 음성입니다");
        }

        log.info("STT 결과: {}", voiceText);

        RestClient restClient = RestClient.create();

        SimilarityResponseDto similarityResponseDto = restClient.get()
            .uri("http://localhost:8000/speaking-style?question="+voiceText)
            .retrieve()
            .onStatus(HttpStatusCode::is4xxClientError, ((request, response) -> {
                throw new ResponseStatusException(HttpStatus.NOT_FOUND, voiceText);
            }))
            .body(SimilarityResponseDto.class);

        if (similarityResponseDto == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        }

        log.info("유사도검사 결과: {}", similarityResponseDto);


        int videoNum = similarityResponseDto.getIndex();
        Resource video = new ClassPathResource("static/video/" + videoNum +  ".mp4");

        
        if (!video.exists()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, similarityResponseDto.toString());
        }

        return ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_TYPE, "video/mp4")
            .body(video);
    }
}

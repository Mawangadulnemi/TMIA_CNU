package com.example.demo.controller;

import static org.springframework.http.MediaType.APPLICATION_JSON;

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
import lombok.Value;
import lombok.extern.slf4j.Slf4j;
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
        Resource defaultVideo = new ClassPathResource("static/video/1.mp4");
        ResponseEntity<Resource> defaultResponse = ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_TYPE, "video/mp4")
            .body(defaultVideo);

        MultipartFile requestVoice = requestDto.getFile();
        Path questionVoice;
        try {
            Path tempDir = conversationService.getTempDir();
            questionVoice = conversationService.saveFile(tempDir, requestVoice);
        } catch (IOException e) {
            log.warn("파일 업로드 실패: {}", e.getMessage());
            return defaultResponse;
        }

        RestTemplate restTemplate = new RestTemplate();

        String url = "http://3.34.227.229:5001/transcribe/";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        Resource voice = new FileSystemResource(questionVoice);
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", voice);


        HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(body, headers);

        STTResponseDto sttResponse;

        try {
            sttResponse = restTemplate.postForObject(url, entity, STTResponseDto.class);
        } catch (Exception e) {
            log.warn("stt서버 에러");
            return defaultResponse;
        }

        if (sttResponse == null) {
            log.warn("stt서버에서 응답 받기 실패 없음");
            return defaultResponse;
        }

        String voiceText = sttResponse.getText();

        if (voiceText.isBlank()) {
            log.warn("빈 질문 음성");
            return defaultResponse;
        }

        log.info("STT 결과: {}", voiceText);

        RestClient restClient = RestClient.create();

        SimilarityResponseDto similarityResponseDto = restClient.post()
            .uri("http://localhost:8001/api/speaking-style")
            .contentType(APPLICATION_JSON)
            .body(new SimilarityRequestDto(voiceText))
            .retrieve()
            .onStatus(HttpStatusCode::is4xxClientError, ((request, response) -> {
                log.warn("유사도분석 서버 에러");
            }))
            .body(SimilarityResponseDto.class);


        if (similarityResponseDto == null) {
            log.warn("유사도검사 결과 null");
            return defaultResponse;
        }

        log.info("유사도검사 결과: {}", similarityResponseDto.toString());

        if (similarityResponseDto.getIndex() < 0) {
            log.info("비슷한 질문 없음");
            return defaultResponse;
        }


        int videoNum = similarityResponseDto.getIndex();
        Resource video = new ClassPathResource("static/video/" + videoNum +  ".mp4");

        
        if (!video.exists()) {
            log.warn("비디오 없음. 유사도겸사 결과: {}, 비디오: {}", similarityResponseDto.toString(), video);
            return defaultResponse;
        }

        return ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_TYPE, "video/mp4")
            .body(video);
    }
}

package com.example.demo.controller;

import com.example.demo.dto.request.conversation.UploadVoiceRequestDto;
import com.example.demo.service.ConversationService;
import jakarta.validation.Valid;
import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
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

        try {
            Path tempDir = conversationService.getTempDir();
            conversationService.saveFile(tempDir, requestVoice);
        } catch (IOException e) {
            log.warn("파일 업로드 실패: {}", e.getMessage());
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR);
        }

        String requestText = conversationService.getRequestText(requestVoice);

        String responseText = conversationService.getResponseText(requestText);

        MultipartFile responseVoice = conversationService.getResponseVoice(responseText);

        // stt에 요청해서 텍스트 받아오고
        // 너한테 보내서 응답 받아오고 10초
        // tts+sts에 보내서 음성 받아오기 2분
        // 음성을 채묵이 모델에 보내서 받아오는게 n분

        Resource video = new ClassPathResource("static/video/1.mp4");

        
        if (!video.exists()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST);
        }

        return ResponseEntity.ok()
            .header(HttpHeaders.CONTENT_TYPE, "video/mp4")
            .body(video);
    }
}

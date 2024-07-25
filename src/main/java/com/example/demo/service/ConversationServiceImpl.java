package com.example.demo.service;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Service
public class ConversationServiceImpl implements ConversationService {

    @Override
    public Path getTempDir() throws IOException {
        return Files.createTempDirectory("TMIA");
    }

    @Override
    public Path saveFile(Path tempDir, MultipartFile file) throws IOException {
        Path tempFile = tempDir.resolve("uploaded.wav");
        Files.copy(file.getInputStream(), tempFile, StandardCopyOption.REPLACE_EXISTING);
        log.info("파일 업로드 성공: {}", tempFile);
        return tempFile;
    }

    @Override
    public MultipartFile openFile(Path path) {
        return null;
    }

    @Override
    public String getRequestText(MultipartFile requestVoice) {
        return null;
    }

    @Override
    public String getResponseText(String requestText) {
        return null;
    }

    @Override
    public MultipartFile getResponseVoice(String responseText) {
        return null;
    }

    @Override
    public MultipartFile getResponseVideo(MultipartFile responseVoice) {
        return null;
    }

    @Override
    public MultipartFile combineVoiceAndVideo(MultipartFile responseVoice,
        MultipartFile responseVideo) {
        return null;
    }

    @Override
    public MultipartFile getResponse(MultipartFile inputVoice) {
        return null;
    }
}

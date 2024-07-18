package com.example.demo.service;

import java.io.IOException;
import java.nio.file.Path;
import org.springframework.web.multipart.MultipartFile;

public interface ConversationService {

    public Path getTempDir() throws IOException;

    public void saveFile(Path tempDir, MultipartFile file) throws IOException;

    public MultipartFile openFile(Path path);

    public String getRequestText(MultipartFile inputVoice);

    public String getResponseText(String inputText);

    public MultipartFile getResponseVoice(String responseText);

    public MultipartFile getResponseVideo(MultipartFile responseVoice);

    public MultipartFile combineVoiceAndVideo(MultipartFile responseVoice,
        MultipartFile responseVideo);

    public MultipartFile getResponse(MultipartFile inputVoice);
}

package com.example.rag.controller;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@RestController
@CrossOrigin(origins = "http://localhost:5173")
public class RagController {
    @PostMapping("/ask")
    public Map<String, String> askQuestion(@RequestBody Map<String,String> body) {

        String question = body.get("question");

        RestTemplate restTemplate = new RestTemplate();

        String pythonapi = "http://127.0.0.1:5000/chat";

        Map<String,String> request = new HashMap<>();
        request.put("question", question);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<Map<String,String>> entity =
                new HttpEntity<>(request, headers);

        ResponseEntity<Map> response =
                restTemplate.postForEntity(pythonapi, entity, Map.class);
        System.out.println(response.getBody());
        return response.getBody();
    }
}

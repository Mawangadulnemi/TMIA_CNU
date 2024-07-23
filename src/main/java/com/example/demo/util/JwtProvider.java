package com.example.demo.util;

import static com.example.demo.exception.ErrorCode.INVALID_JWT_SIGNATURE;
import static com.example.demo.exception.ErrorCode.INVALID_TOKEN;
import static com.example.demo.exception.ErrorCode.TOKEN_EXPIRED;

import com.example.demo.config.auth.TokenException;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.Jwts.SIG;
import io.jsonwebtoken.MalformedJwtException;
import java.time.Instant;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;
import javax.crypto.SecretKey;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

@Component
public class JwtProvider {

    private final SecretKey secretKey = SIG.HS256.key().build();

    public String generateToken(Authentication authentication) {

        Date now = Date.from(Instant.now());
        Date expiredDate = new Date(now.getTime() + 1000 * 60 * 60 * 2L);

        String authorities = authentication.getAuthorities().stream()
            .map(GrantedAuthority::getAuthority)
            .collect(Collectors.joining());

        return Jwts.builder()
            .subject(authentication.getName())
            .claim("role", authorities)
            .issuedAt(now)
            .expiration(expiredDate)
            .signWith(secretKey)
            .compact();
    }

    public Authentication getAuthentication(String token) {
        Claims claims = parseClaims(token);
        List<SimpleGrantedAuthority> authorities = getAuthorities(claims);

        User principal = new User(claims.getSubject(), "", authorities);
        return new UsernamePasswordAuthenticationToken(principal, token, authorities);
    }

    private List<SimpleGrantedAuthority> getAuthorities(Claims claims) {
        return Collections.singletonList(new SimpleGrantedAuthority(
            claims.get("role").toString()));
    }


    public boolean validateToken(String token) {
        if (!StringUtils.hasText(token)) {
            return false;
        }

        Claims claims = parseClaims(token);
        return claims.getExpiration().after(new Date());
    }

    private Claims parseClaims(String token) {
        try {
            return Jwts.parser().verifyWith(secretKey).build()
                .parseSignedClaims(token).getPayload();
        } catch (ExpiredJwtException e) {
            throw new TokenException(TOKEN_EXPIRED);
        } catch (MalformedJwtException e) {
            throw new TokenException(INVALID_TOKEN);
        } catch (SecurityException e) {
            throw new TokenException(INVALID_JWT_SIGNATURE);
        }
    }

}

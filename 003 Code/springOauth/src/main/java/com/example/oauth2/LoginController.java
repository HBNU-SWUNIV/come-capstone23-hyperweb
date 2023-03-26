package com.example.oauth2;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class LoginController {
	
	private final OauthService oauthService;

    public LoginController(OauthService oauthService) {
        this.oauthService = oauthService;
    }
    
	@GetMapping("/login")
	public String login() {
		return "login.html";
	}
	
//	@GetMapping("/loginSuccess")
//	public String loginSuccess() {
//		return "loginSuccess.html";
//	}
	
	@GetMapping("/login/oauth2/code/{provider}")
	  public String login(@PathVariable String provider, @RequestParam String code, Model model) {
	      LoginResponse loginResponse = oauthService.login(provider, code);
	      model.addAttribute("loginResponse", loginResponse);
	      return "loginSuccess";
	  }
}

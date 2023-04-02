package naverSearch;

import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;

public class StringConverter {

	static public String encodeString(String input) {
		String encodedString = null;
        try {
            String utf8String = new String(input.getBytes("UTF-8"), "UTF-8");
            encodedString = URLEncoder.encode(utf8String, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return encodedString;
	}
}

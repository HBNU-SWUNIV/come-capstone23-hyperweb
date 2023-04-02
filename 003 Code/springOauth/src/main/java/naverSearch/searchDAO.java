package naverSearch;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class searchDAO {

	public static String getSearchData(String searchQuery) {
		try {
			String query = StringConverter.encodeString(searchQuery);
			System.out.println(query);
			String urlData = "https://openapi.naver.com/v1/search/local.xml?display=5&" + "query=" + query;
			
            // 요청 URL 설정
            URL url = new URL(urlData);

            // HttpURLConnection 객체 생성 및 설정
            HttpURLConnection con = (HttpURLConnection) url.openConnection();
            con.setRequestMethod("GET");
            con.setRequestProperty("User-Agent", "curl/7.49.1");
            con.setRequestProperty("Accept", "*/*");
            con.setRequestProperty("X-Naver-Client-Id", "764T8YG0q604YOxSJj_K");
            con.setRequestProperty("X-Naver-Client-Secret", "qPxiVaKqF5");

            // 응답 코드 확인
            int responseCode = con.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                // 응답 데이터 읽기
                BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
                String inputLine;
                StringBuffer response = new StringBuffer();
                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();

                // 응답 데이터 출력
                return response.toString();
            } else {
                return "HTTP 요청 실패 : " + responseCode;
            }
        } catch (Exception e) {
            return "에러 발생 : " + e.getMessage();
        }
    }
	
	public static void main(String[] args) throws Exception{
		String data;
		try {
			data = searchDAO.getSearchData("애완동물 동반");
			System.out.println(data);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}


}

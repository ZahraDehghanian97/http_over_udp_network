/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package proxy;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.ProtocolException;
import java.net.URL;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author hamed
 */
public class HTTPGET {
    public static HTTPGETANSWER getHTML(String urlToRead) {
      
        try {
            StringBuilder result = new StringBuilder();
            URL url = new URL(urlToRead);
            
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setInstanceFollowRedirects(true);  //you still need to handle redirect manully.
            HttpURLConnection.setFollowRedirects(true);

            int status = conn.getResponseCode();

            while(status != HttpURLConnection.HTTP_OK ){ // 200

                if(status == HttpURLConnection.HTTP_NOT_FOUND) {//404
                    return new HTTPGETANSWER(404, "");
                }

                if (status == HttpURLConnection.HTTP_MOVED_TEMP // 302
                 || status == HttpURLConnection.HTTP_MOVED_PERM // 301
                      )
                {
                      url = new URL(conn.getHeaderField("Location")); // new location
                      conn = (HttpURLConnection) url.openConnection(); //reopen
                      conn.setRequestMethod("GET");
                      conn.setInstanceFollowRedirects(true);  
                      HttpURLConnection.setFollowRedirects(true);

                      status = conn.getResponseCode();
                }
            }
      
            BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));

            String line;
            while ((line = rd.readLine()) != null) {
               result.append(line);
            }
            rd.close();
            return new HTTPGETANSWER(200, result.toString());

        } catch (MalformedURLException ex) {
            Logger.getLogger(HTTPGET.class.getName()).log(Level.SEVERE, null, ex);
        } catch (ProtocolException ex) {
            Logger.getLogger(HTTPGET.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(HTTPGET.class.getName()).log(Level.SEVERE, null, ex);
        }
      
        
        return new HTTPGETANSWER(0, "");
   }
    public String get(String url){
        String content = "";
        
        
        
        
        
        return content;
    }
    
}

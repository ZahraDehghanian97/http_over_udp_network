/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package clienttooldns;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Proxy;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author hamed
 */
public class ClientToolDNS {

   
    static ClientToolDNS listenerInstance = new ClientToolDNS();
    
    public static void InvalidParameters(){
       System.out.println("Invalid parameters") ; 
    }
    public static void w(String str){
       System.out.println(str) ;  
    }
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        String inputA = "";
        String inputB = "";
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        
        
        
        Thread th=new Thread(new Runnable() {
            @Override
            public void run() {
                int port = 59;
                listenerInstance.run(port);
            }
        });
        
        th.start();
                 
        try {

            while(true){
                inputA    = br.readLine();

                //inputA = "type=A server=4.2.2.4 target=yahoo.com";
                
                String inputs[] = inputA.split(" ");
                
                String type="",server="",target="";
                
                for(int i=0;i<inputs.length;i++){
                    String key_value [] = inputs[i].split("=");
                    String key = key_value[0];
                    String val = key_value[1];
                    
                    if("type"   .equals(key))      type = val;
                    if("server" .equals(key))    server = val;
                    if("target" .equals(key))    target = val;
                }
               
                if("".equals(type) || "".equals(server) || "".equals(target)) {
                    w("Input string is not in correct format !");
                    break;
                }
                UDPSender.Send("get-dns" , type+";"+server+";"+target);
                inputA    = br.readLine();//pause loop


            }

        } catch (IOException ex) {
            Logger.getLogger(Proxy.class.getName()).log(Level.SEVERE, null, ex);
        }
        

        
    }
    
    
    public void run(int port) {    
      try {
        DatagramSocket serverSocket = new DatagramSocket(port);
        byte[] receiveData = new byte[4096];
        DatagramPacket receivePacket = new DatagramPacket(receiveData,
                           receiveData.length);

        while(true)
        {
              serverSocket.receive(receivePacket);
              String sentence = new String( receivePacket.getData(), 0,receivePacket.getLength() );
          
             
              if("answer_dns_query".equals(sentence)){
                  
                  //is autherative :
                  serverSocket.receive(receivePacket);
                  sentence = new String( receivePacket.getData(), 0,receivePacket.getLength() );
                  
                  w(sentence);
                  
                  //answer :
                  serverSocket.receive(receivePacket);
                  sentence = new String( receivePacket.getData(), 0,receivePacket.getLength() );
                  
                  if(sentence.equals("")) w("Not found a CName");
                  w(sentence);
              }
              
//              if("sending-html-content".equals(sentence)){
//                  //get code :
//                  serverSocket.receive(receivePacket);
//                  sentence = new String( receivePacket.getData(), 0,receivePacket.getLength() );
//                  
//                  if("200".equals(sentence)){
//                      //get html :
//                      serverSocket.receive(receivePacket);
//                      sentence = new String( receivePacket.getData(), 0,receivePacket.getLength() );
//                      
//                      System.out.println("HTML :: " + sentence);
//                  }
//                  if("404".equals(sentence)){
//                      System.out.println("Not found.");
//                  }
//                  
//                  
//              }
              
        }
      } catch (IOException e) {
              System.out.println(e);
      }
      // should close serverSocket in finally block
    }
    
    
}

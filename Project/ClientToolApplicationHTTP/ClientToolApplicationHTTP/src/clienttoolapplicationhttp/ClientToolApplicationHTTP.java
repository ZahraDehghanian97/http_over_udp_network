/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package clienttoolapplicationhttp;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Proxy;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author hamed
 */
public class ClientToolApplicationHTTP {
    
    static ClientToolApplicationHTTP listenerInstance = new ClientToolApplicationHTTP();
    
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
               inputB   = br.readLine();

                //inputA = "GET / HTTP/1.1";
                //inputB = "Host: google.com";
               
               int inputA_last_index = inputA.toLowerCase().indexOf("http/1.1");
               int inputB_last_index = inputB.toLowerCase().indexOf("host:");
               
               
               if(inputB_last_index == -1 || inputA_last_index == -1 || !inputA.toLowerCase().startsWith("get") || !inputB.toLowerCase().startsWith("host:")){
                   w("Invalid Request Format !");
                   w("You need to follow a specific format :");
                   w("---------------------------------------------");
                   w("GET / HTTP/1.1");
                   w("Host: google.com");
                   w("---------------------------------------------");

               }else{
                   
                   
                   String url_part_1 = inputA.substring(3,inputA_last_index).trim();
                   String url_part_2 = inputB.substring(5).trim();
                   
                   String urlAddress="http://" + url_part_2 + url_part_1;
                   
                   
                   w("---------------------------------------------");
                   w("You've requested following address : ");
                   w(urlAddress);
                   w("trying to connect to the Proxy server ..");
                   w("---------------------------------------------");
                   
                   UDPSender.Send("get-url" , urlAddress);
                   inputA    = br.readLine();//pause loop
                   
                   

               }



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
              String sentence = new String( receivePacket.getData(), 0,
                                 receivePacket.getLength() );
              
              
              if("sending-html-content".equals(sentence)){
                  //get code :
                  serverSocket.receive(receivePacket);
                  sentence = new String( receivePacket.getData(), 0,receivePacket.getLength() );
                  
                  if("200".equals(sentence)){
                      //get html :
                      serverSocket.receive(receivePacket);
                      sentence = new String( receivePacket.getData(), 0,receivePacket.getLength() );
                      
                      BufferedWriter writer = new BufferedWriter(new FileWriter("output.html"));
                      writer.append(sentence);
                      writer.flush();
                      writer.close();
                      System.out.println("Saved in html file (output.html)");
                  }
                  if("404".equals(sentence)){
                      System.out.println("Not found.");
                  }
                  
                  
              }
              
        }
      } catch (IOException e) {
              System.out.println(e);
      }
      // should close serverSocket in finally block
    }
    
    
    
}

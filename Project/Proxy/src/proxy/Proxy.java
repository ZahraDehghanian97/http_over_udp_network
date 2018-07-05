/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package proxy;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.xbill.DNS.Type;

/**
 *
 * @author hamed
 */
public class Proxy {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        
        int port = 58;
        new Proxy().run(port);
    }
    
    public void run(int port) {    
      try {
        DatagramSocket serverSocket = new DatagramSocket(port);
        byte[] receiveData = new byte[512];

        System.out.printf("Listening on udp:%s:%d%n",
                InetAddress.getLocalHost().getHostAddress(), port);     
        DatagramPacket receivePacket = new DatagramPacket(receiveData,
                           receiveData.length);

        while(true)
        {
              serverSocket.receive(receivePacket);
              String sentence = new String( receivePacket.getData(), 0,
                                 receivePacket.getLength() );
              System.out.println("RECEIVED: " + sentence);
              
              if("get-url".equals(sentence)){
                  //next param :
                  serverSocket.receive(receivePacket);
                  sentence = new String( receivePacket.getData(), 0,receivePacket.getLength() );
                  System.out.println("URL To Recieve: " + sentence);
                  sendDataBack(serverSocket,receivePacket.getAddress(),59,"sending-html-content");
                  HTTPGETANSWER answer = HTTPGET.getHTML(sentence);
                  if(answer.code == 404){
                      sendDataBack(serverSocket,receivePacket.getAddress(),59,"404");
                  }else{
                      sendDataBack(serverSocket,receivePacket.getAddress(),59,"200");
                      sendDataBack(serverSocket,receivePacket.getAddress(),59,answer.html);
                  }
              }
              if("get-dns".equals(sentence)){
                  serverSocket.receive(receivePacket);
                  sentence = new String( receivePacket.getData(), 0,receivePacket.getLength() );
                  
                  String sentenceArr [] = sentence.split(";");
                  String type=sentenceArr[0],server=sentenceArr[1],target=sentenceArr[2];
                  
                  w("DNS Requested ..");
                  w("Type = " + type);
                  w("Server = " + server);
                  w("Target = " + target);
                  
                  
                  int type_ = Type.A;
                  if(type.toLowerCase().equals("cname")) type_ = Type.CNAME;
                  
                  ResolveAnswer answ=DNSResolver.Resolve(target, type_, server);
                  
                  sendDataBack(serverSocket,receivePacket.getAddress(),59,"answer_dns_query");
                  if(answ.isAuthorityAnswer) sendDataBack(serverSocket,receivePacket.getAddress(),59,"Is authrative answer . ");
                  if(!answ.isAuthorityAnswer) sendDataBack(serverSocket,receivePacket.getAddress(),59,"Is not authrative answer . ");
                  
                  
                  String allAddress = "";
                  for(int i=0;i<answ.list.size();i++) allAddress += answ.list.get(i) + ",";
                      
                  sendDataBack(serverSocket,receivePacket.getAddress(),59,allAddress);
              }

              // now send acknowledgement packet back to sender     
              
        }
      } catch (IOException e) {
              System.out.println(e);
      }
      // should close serverSocket in finally block
    }
    
    static void sendDataBack(DatagramSocket serverSocket,InetAddress IPAddress,int port,String sendString){
      
        byte[] sendData;
        try {
            sendData = sendString.getBytes("UTF-8");
            DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length,IPAddress, 59);
            serverSocket.send(sendPacket);
        } catch (UnsupportedEncodingException ex) {
            Logger.getLogger(Proxy.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(Proxy.class.getName()).log(Level.SEVERE, null, ex);
        }
        
    }
    
    static String getKey(String input){
        String[] arr = input.split("=");
        if(arr.length == 2){
           return arr[0] ;
        }else{
           return null ;
        }
    }
    static String getValue(String input){
        String[] arr = input.split("=");
        if(arr.length == 2){
           return arr[1] ;
        }else{
           return null ;
        }
    }
    static String findInArguments(ArrayList<String> arr,String name){
       String found = null;
       for (String arg : arr) {
           String key = getKey(arg);
           if(key.equals(name)) return getValue(arg);
       } 
       
       
       return found;
    }
    public static void InvalidParameters(){
       System.out.println("Invalid parameters") ; 
    }
    public static void w(String str){
       System.out.println(str) ;  
    }
    private static void analyzeCommand(String[] args) {
        //Make a list from args :
        ArrayList<String> arr=new ArrayList();
        arr.addAll(Arrays.asList(args));
        
        for (String arg : arr) {
            if(arg.startsWith("type")){
                //DNS Request :
                String DNS_TYPE     = getValue(arg);
                String DNS_SERVER   = findInArguments(arr,"server");
                String DNS_TARGET   = findInArguments(arr,"target");
                
                if(DNS_SERVER == null || DNS_TARGET == null){
                    InvalidParameters();
                }else{
                    //DNS Request Processing : 
                    do_dns(DNS_TYPE,DNS_SERVER,DNS_TARGET);
                }
                break;
            }
            
        }
      
        
    }

    
    private static void do_dns(String DNS_TYPE, String DNS_SERVER, String DNS_TARGET) {
        
        int MAX_RETRY = 3;
        int RETRY_COUNTER=0;
            
        if(DNS_TYPE.toUpperCase().equals("A")){
            
            ResolveAnswer answer=null;
            do {                
                if(RETRY_COUNTER == MAX_RETRY) break;
                
                answer = DNSResolver.Resolve(DNS_TARGET,Type.A,DNS_SERVER);
                if(answer.list!=null && !answer.list.isEmpty() ) break;//found then break retry
                
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException ex) {
                    Logger.getLogger(Proxy.class.getName()).log(Level.SEVERE, null, ex);
                }
                RETRY_COUNTER ++ ;
            } while (true);
            
            
            
            ArrayList<String> mmm = answer.list;
            if(mmm == null || mmm.isEmpty()){
                w("[A] Record Not found !"); 
            }else{
                w("[A] Records found :");
                if(answer.isAuthorityAnswer) w("((Authoritative answer))");else w("((Non-authoritative answer))"); 
                for (int i = 0; i < mmm.size(); i++) {
                    w(mmm.get(i)) ; 
                }  
            }
            
        }
        
        if(DNS_TYPE.toUpperCase().equals("CNAME")){
             
            ResolveAnswer answer=null;
            do {                
                if(RETRY_COUNTER == MAX_RETRY) break;
                
                answer = DNSResolver.Resolve(DNS_TARGET,Type.CNAME,DNS_SERVER);
                if(answer.list!=null && !answer.list.isEmpty() ) break;//found then break retry
                
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException ex) {
                    Logger.getLogger(Proxy.class.getName()).log(Level.SEVERE, null, ex);
                }
                RETRY_COUNTER ++ ;
            } while (true);
            
            
            
            ArrayList<String> mmm = answer.list;
            if(mmm == null || mmm.isEmpty()){
               w("[CNAME] Record Not found !"); 
            }else{
                
                w("CNAME Record found :");
                if(answer.isAuthorityAnswer) w("((Authoritative answer))");else w("((Non-authoritative answer))"); 
                for (int i = 0; i < mmm.size(); i++) {
                    w(mmm.get(i)) ; 
                }  
            }
        }
        
        
    }
    
    
}

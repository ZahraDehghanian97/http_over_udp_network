/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package clienttooldns;

import java.io.IOException;
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
public class UDPSender {
    static int port=58;
    
   
    public static boolean Send(String Command,String data){
        
        

        try {
            byte [] IP= { (byte)127, (byte)0, 0, 1 };
            InetAddress address = InetAddress.getByAddress(IP);

            byte[] bufferCommand = Command.getBytes();
            byte[] buffer = data.getBytes();
            
            DatagramSocket datagramSocket = new DatagramSocket();
            
            //Send Command : 
            DatagramPacket packetCommand = new DatagramPacket(bufferCommand, bufferCommand.length, address, port);
            datagramSocket.send(packetCommand);

            //Send Data :
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length, address, port);
            datagramSocket.send(packet);
            
            
            
            //System.out.println(InetAddress.getLocalHost().getHostAddress());
            
            return true;
            
        } catch (UnknownHostException ex) {
            Logger.getLogger(Proxy.class.getName()).log(Level.SEVERE, null, ex);
            
        } catch (SocketException ex) {
            Logger.getLogger(Proxy.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(Proxy.class.getName()).log(Level.SEVERE, null, ex);
        }
        return false;
    }
}

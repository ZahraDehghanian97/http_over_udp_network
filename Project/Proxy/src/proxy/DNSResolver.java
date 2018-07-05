/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package proxy;

import java.io.IOException;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.xbill.DNS.ARecord;
import org.xbill.DNS.CNAMERecord;
import org.xbill.DNS.DClass;
import org.xbill.DNS.Flags;
import org.xbill.DNS.Message;
import org.xbill.DNS.Name;
import org.xbill.DNS.Record;
import org.xbill.DNS.Section;
import org.xbill.DNS.SimpleResolver;
import org.xbill.DNS.TextParseException;
import org.xbill.DNS.Type;

/**
 *
 * @author hamed
 */
public class DNSResolver {
    
    public static ResolveAnswer Resolve(String host, int addrType,String DnsServer){
        ArrayList<String> list=new ArrayList<>(); 
        Record query;
        boolean isAuthorityAnswer = false;
        try {
            SimpleResolver resolver = new SimpleResolver(DnsServer);
            
            query = Record.newRecord(Name.fromString(host + ".") , addrType, DClass.ANY);
            Message question = Message.newQuery(query);
            Message response = resolver.send(question);
            Record responses[] = response.getSectionArray(Section.ANSWER);
            isAuthorityAnswer = response.getHeader().getFlag(Flags.AA);
            for (Record record : responses) {
             
             if (record.getType() == Type.A) {
                 list.add(((ARecord) record).getAddress().getHostAddress());
             }
             if(record.getType() == Type.CNAME){
               list.add(((CNAMERecord) record).getAlias().toString());  
             }
         }
            
            
        } catch (TextParseException ex) {
            Logger.getLogger(Proxy.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(Proxy.class.getName()).log(Level.SEVERE, null, ex);
        }
        return new ResolveAnswer(list,isAuthorityAnswer);
    }
}

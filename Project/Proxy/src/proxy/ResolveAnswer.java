/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package proxy;

import java.util.ArrayList;

/**
 *
 * @author hamed
 */
public class ResolveAnswer {
    public ArrayList<String> list; 
    public boolean isAuthorityAnswer;

    public ResolveAnswer(ArrayList<String> list2,boolean isAuthorityAnswer2){
        this.list = list2;
        this.isAuthorityAnswer = isAuthorityAnswer2;
    }
}

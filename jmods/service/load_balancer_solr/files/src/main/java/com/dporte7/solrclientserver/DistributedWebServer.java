/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.dporte7.solrclientserver;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import org.apache.solr.client.solrj.SolrQuery;
import org.apache.solr.client.solrj.impl.CloudSolrClient;
import org.apache.solr.client.solrj.response.QueryResponse;

import java.util.*;

/**
 *
 * @author dporter
 */
public class DistributedWebServer {

    private static String defaultCollection = "reviews";
    protected static CloudSolrClient instance;
    // need to get clustersize here and pass to optional

    public static void main(String[] args) throws Exception {
        // try passing just one instance of cloudsolrclient to thread generator class
        // one instance proved to perform the same as multiple instance on different ports that
        // the python script would load balance requrests across. Solr has aknowledged this shortcoming
        // in their forum, and I think they will implement an asynchronous solrcloud clinet with
        // http2 in an upcomming release.
        System.out.println("starting Server");
        final Optional<String> znode = Optional.of(args[0]);
        // need to get clustersize here and pass to optional
        List<String> zesty = new ArrayList<>(Arrays.asList("10.10.1.1:2181","10.10.1.2:2181","10.10.1.3:2181"));

        instance = new CloudSolrClient.Builder(zesty,znode).build();
        final int zkClientTimeout = 9999;
        final int zkConnectTimeout = 9999;
        instance.setDefaultCollection(defaultCollection);
        instance.setZkClientTimeout(zkClientTimeout);
        instance.setZkConnectTimeout(zkConnectTimeout);
        MultiThreadedServer server4 = new MultiThreadedServer(9444, instance);

        new Thread(server4).start();

        try {
            Thread.sleep(20000 * 1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Stopping Server");
        //stops multithreded server loop

        server4.stop();
    }

}

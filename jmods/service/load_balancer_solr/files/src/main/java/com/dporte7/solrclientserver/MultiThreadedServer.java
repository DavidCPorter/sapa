package com.dporte7.solrclientserver;
import org.apache.solr.client.solrj.impl.CloudSolrClient;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.IOException;
/**
 *
 * @author dporter
 */
public class MultiThreadedServer implements Runnable{
    private int          serverPort;
    private ServerSocket pyServer = null;
    private boolean      isStopped    = false;
    private Thread       runningThread= null;
    private CloudSolrClient solrAPI;

    public MultiThreadedServer(int port, CloudSolrClient solrAPI){
        this.serverPort = port;
        this.solrAPI = solrAPI;
    }

    public void run(){
        // creates pyServer socket

        this.solrAPI.connect();

        openServerSocket();

        // listens for connections then hands to another thread - WorkerRunnable
        // so each request from the pyServer (traffic_gen.py) is passed to a new thread.
        while(!isStopped()){
            //creates new socket variable and assigns it to a new connection.

            Socket pySocket = new Socket();

            try {
                System.out.println("listening for new connections");
                pySocket = this.pyServer.accept();
                System.out.println("accepted connection."+ String.valueOf(serverPort));
            } catch (IOException e) {
                if(isStopped()) {
                    System.out.println("Server Stopped.") ;
                    return;
                }
                throw new RuntimeException(
                        "Error accepting client connection", e);
            }
            // passes socket object and a solrj connection to a new thread to handle request
            new Thread(
                    new WorkerRunnable(
                            this.isStopped, pySocket, this.solrAPI, "Multithreaded Server")
            ).start();

        }
        System.out.println("Server Stopped.") ;
    }

    private synchronized boolean isStopped() {
        return this.isStopped;
    }

    public synchronized void stop(){
        this.isStopped = true;
        try {
            this.pyServer.close();
        } catch (IOException e) {
            throw new RuntimeException("Error closing server", e);
        }
    }

    private void openServerSocket() {
        try {
            //serversocket just creates a server
            this.pyServer = new ServerSocket(this.serverPort);
        } catch (IOException e) {
            throw new RuntimeException("Cannot open serverPort", e);
        }
    }

}

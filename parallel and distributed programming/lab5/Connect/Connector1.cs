using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using Parser;

namespace Connector {
    public class Connector1 {
        public void communicate(System.IAsyncResult ar){
            Socket socket = ((Socket)((Object[])ar.AsyncState)[0]);
            String uri = ((String)((Object[])ar.AsyncState)[1]);
            
            var ip = ((System.Net.IPEndPoint) socket.RemoteEndPoint).Address.ToString();

            byte[] message = Encoding.ASCII.GetBytes("GET " + uri + " HTTP/1.1\r\nHost:" + ip +
                             "\r\nConnection: keep-alive\r\nAccept: text/html\r\nUser-Agent: CSharpTests\r\n\r\n");
            Console.WriteLine("Mesage to send: {0}", Encoding.ASCII.GetString(message));
            IAsyncResult asyncSendResult = socket.BeginSend(message, 0, message.Length, SocketFlags.None, null, null);
            while(!asyncSendResult.IsCompleted) {
                Thread.Sleep(1000);
            }
            socket.EndSend(asyncSendResult);
            byte[] file = new byte[256];
            IAsyncResult asyncReceiveResult = socket.BeginReceive(file, 0, file.Length, SocketFlags.None, null, null);
            while(!asyncReceiveResult.IsCompleted) {
                Thread.Sleep(1000);
            }
            socket.EndReceive(asyncReceiveResult);
            Console.WriteLine("Result: {0}", Encoding.ASCII.GetString(file));
            socket.EndConnect(ar);
        }
        public IAsyncResult asyncFetch(string host, int port, string uri) {
            Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            return socket.BeginConnect(host, port, new System.AsyncCallback(this.communicate), new Object[]{socket, uri});
        }
    }
}
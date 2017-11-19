using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Connector {
    public class Connector2 {
        public void communicate(IAsyncResult ar) {
            Socket socket = ((Socket)((Object[])ar.AsyncState)[0]);
            String uri = ((String)((Object[])ar.AsyncState)[1]);
            TaskCompletionSource<string> tcs = ((TaskCompletionSource<string>)((Object[])ar.AsyncState)[2]);

            byte[] message = Encoding.ASCII.GetBytes("GET " + uri + " HTTP/1.1\r\n");
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
            tcs.SetResult(string.Format("Result(size: {1}): {0}", Encoding.ASCII.GetString(file), Encoding.ASCII.GetString(file).Length));
            socket.EndConnect(ar);
        }

        public async void asyncFetch(string host, int port, string uri) {
            Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            TaskCompletionSource<string> tcs = new TaskCompletionSource<string>();
            Task<string> task = tcs.Task;
            await Task.Factory.StartNew(() => {
                socket.BeginConnect(host, port, new System.AsyncCallback(this.communicate), new Object[]{socket, uri, tcs});
            });
            Console.WriteLine(task.Result);            
        }
    }
}
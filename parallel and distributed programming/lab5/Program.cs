using System;
using System.Threading;
using Connector;
using Parser;

namespace lab5
{
    class Program
    {
        static void Main(string[] args)
        {
            Connector1 connector = new Connector1();
            //IAsyncResult result = connector.asyncFetch("ipv4.download.thinkbroadband.com", 80, "/5MB.zip");
            Connector2 connector2 = new Connector2();
            connector2.asyncFetch("ipv4.download.thinkbroadband.com", 80, "/5MB.zip");
            /*while (!result.IsCompleted) {
                Thread.Sleep(1000);
            }*/
            Thread.Sleep(1000000);
        }
    }
}

- 我们之前接触的五层、七层架构都是逻辑上的，真正在Linux中是怎样的？

- 逻辑抽象层级：

        物理层：主要提供各种连接的物理设备，如各种网卡，串口卡等。
        
        链路层：主要提供对物理层进行访问的各种接口卡的驱动程序，如网卡驱动等。
        
        网路层：是负责将网络数据包传输到正确的位置，最重要的网络层协议是 IP 协议，此外还有如 ICMP，ARP，RARP 等协议。
        
        传输层：为应用程序之间提供端到端连接，主要为 TCP 和 UDP 协议。
        
        应用层：顾名思义，主要由应用程序提供，用来对传输数据进行语义解释的 “人机交互界面层”，比如 HTTP，SMTP，FTP 等协议。

- 协议栈实现层级：

        硬件层（Physical device hardware）：又称驱动程序层，提供连接硬件设备的接口。
        
        设备无关层（Device agnostic interface）：又称设备接口层，提供与具体设备无关的驱动程序抽象接口。这一层的目的主要是为了统一不同的接口卡的驱动程序与网络协议层的接口，它将各种不同的驱动程序的功能统一抽象为几个特殊的动作，如 open，close，init 等，这一层可以屏蔽底层不同的驱动程序。
        
        网络协议层（Network protocols）：对应 IP layer 和 Transport layer。毫无疑问，这是整个内核网络协议栈的核心。这一层主要实现了各种网络协议，最主要的当然是 IP，ICMP，ARP，RARP，TCP，UDP 等。
        
        协议无关层（Protocol agnostic interface），又称协议接口层，本质就是 SOCKET 层。这一层的目的是屏蔽网络协议层中诸多类型的网络协议（主要是 TCP 与 UDP 协议，当然也包括 RAW IP， SCTP 等等），以便提供简单而同一的接口给上面的系统调用层调用。简单的说，不管我们应用层使用什么协议，都要通过系统调用接口来建立一个 SOCKET，这个 SOCKET 其实是一个巨大的 sock 结构体，它和下面的网络协议层联系起来，屏蔽了不同的网络协议，通过系统调用接口只把数据部分呈献给应用层。
        
        BSD（Berkeley Software Distribution）socket：BSD Socket 层，提供统一的 SOCKET 操作接口，与 socket 结构体关系紧密。
        
        INET（指一切支持 IP 协议的网络） socket：INET socket 层，调用 IP 层协议的统一接口，与 sock 结构体关系紧密。
        
        系统调用接口层（System call interface），实质是一个面向用户空间（User Space）应用程序的接口调用库，向用户空间应用程序提供使用网络服务的接口。

# JVM 运行时数据区



- 相关的JVM运行时参数

    ```
    -Xmx10m // 设置堆内存为10M
    ```

    





## 程序计数器 PC Register

- 底层Java使用物理的寄存器来充当程序计数器，其中保存下一条JVM指令的地址
- 程序计数器是线程私有的





## 虚拟机栈 JVM Stack

- 以栈帧为基本元素，每个栈帧对应一次方法的调用，栈帧是每个方法运行时需要的内存

- 垃圾回收是否涉及栈内存？

    不用，因为栈内存会自动回收掉

- 栈内存分配越大越好吗？

    可以通过虚拟机参数指定`-Xss size`栈帧大小，但是栈越大，线程数越少

- 方法内的局部变量是否线程安全？

    看一个变量是否线程安全，只要看这个变量是线程共享的还是线程私有的，因为栈是线程私有的，所有局部变量肯定也是线程私有的，所以是安全的。但注意如果局部变量是方法的参数，或者被方法返回，即“逃离”了方法的作用域，那么这个局部变量不一定是线程安全的。

- 栈内存溢出（线程栈不够用了）

    栈帧过多导致栈内存溢出

- 线程运行诊断

    top命令只能查看进程

    ```
    top
    ```

    ps命令可以查看线程

    ```
    ps H -eo pid,tid,%cpu | grep "使用top查看的进程id"
    ```

    JDK提供jstack命令可以查看

    ```
    jstack 进程id
    ```

    该命令也会自动检测是否死锁

    

    

    

## 本地方法栈

- 本地方法：用C/C++编写的和操作系统打交道的代码，不论是在基础类库还是JVM内部都会调用本地方法





## 堆

- 通过new关键词创建的对象都会使用堆内存

- 堆是线程共享的，而且有垃圾回收机制

- 堆内存诊断

    jps查看当前系统中有哪些Java进程

    jmap 查看堆内存占用情况，只能每次做快照

    ```
    jmap -heap 进程id
    ```

    jconsole工具，图形化界面，连续监测

    jvisualvm，需要额外安装

    ```
    jvisualvm
    ```

    



## 方法区（Method Area）

- 所有Java虚拟机线程共享的区域，存储了和类相关的信息

- 逻辑上是堆的一部分，但不强制对其垃圾回收。Hotspot的实现（元空间）使用的是本地的内存（而不是占用堆中的内存），不由JVM管理。

- 元空间包括类、类加载器、运行时常量池，StringTable串池被放到了堆中（永久代的串池在常量池中）

- 如何实现类的加载？

    > - 以自定义类加载器为例
    >
    >     ```java
    >     public class 
    >     ```
    >
    > - 使用cglib动态产生字节码

- 运行时常量池

    - 给字节码指令提供常量符号

    - 就是一张大表，虚拟机指令根据这张表找到要执行的类名、方法名、参数类型、字面量等信息

    - 注意这里的常量池是运行时的，每个.class文件都有一个静态常量池，当该类被加载，它的常量池就会被放到内存中，把其中的#1、#2改成真实的内存地址

    - 串池相关的面试题

        > - 首先需要学会查看一个类的字节码详细信息
        >
        >     ```
        >     javap -v Xxx.class
        >     ```
        >
        > - 其次，理解字符串对象的创建过程：
        >
        >     - 字符串对象是懒惰实例化的，所以只会在用到的时候创建字符串对象，然后放入串池
        >
        >     - 如果在串池中已有该字符串，那么都是从串池中获得字符串对象
        >
        >     - 在1.6中串池是在常量池中，存的只是常量的字符串，动态拼接的字符串都在堆中
        >
        >     - 1.8的实现是把串池放到了堆中，这样就能用到垃圾回收（但也是堆中的串池，和堆中的其他new出来的对象还是不一样）
        >
        >     - 1.8的串池照样会触发垃圾回收
        >
        >     - 1.8串池的性能优化
        >
        >         - `-XX:StringTableSize=200000`，设置串池的大小，因为串池底层是哈希表，所以其实设置哈希表的大小。如果系统的字符串很多，那么应该增加串池的大小，减少哈希冲突。
        >
        >         - 字符串什么情况下应该放到串池，什么情况下应该放到堆？
        >
        >             因为串池不会记录重复的字符串，所以如果是有大量重复的字符串，应该入池（intern()），节约堆内存的使用。



## 直接内存

- 常见于NIO操作，用于数据缓冲区

    - 

- 分配回收成本较高，但读写性能高

    - 磁盘文件先被读到系统缓冲区，Java堆内存也有一块缓冲区，会将系统缓冲区中的内容读入到Java缓冲区，才能被Java代码访问
    - 对于直接内存，系统可以直接访问，Java也可以访问，少了一层缓冲，性能成倍提升

- 不受JVM内存回收管理

    - 直接内存的底层使用Unsafe类进行直接内存的申请、设置和释放。回收需要主动调用freeMemory方法

    - ByteBuffer的实现类内部，使用了Cleaner虚引用来监测ByteBuffer对象，一旦ByteBuffer对象被垃圾回收，那么就会由ReferenceHandler线程通过Cleaner的clean方法调用freeMemory来释放内存（源码里都有）

        


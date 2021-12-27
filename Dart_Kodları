import 'package:flutter/material.dart';

var b = "Balci";
void main(){
  String c = "Merba";
  print(c);

  b = "Samsun";
  print(b); //Gördüğümüz gibi global değişkeni herhangi bir keyword olmadan değiştirdik.
  var a;   //int Function({dynamic param0 = 45, required dynamic param2}) ifadesi sağdaki a referansının type'idir.
  print(a);
  a = 5;
  a = a.toString();
  method_1(4,param2: a);
  if (1 > 0){
    b = "Berke";
    print(b);
    final a = 10; //Daha da local olan a değişkeni.Yukarıdaki a ile aynı değildir.
    method_1(4, param2: a);
  }
}

method_1(param1,{required param2}) {
  final a = "Başka bir a";
  print(param2);
  method_2();
}
void method_2(){
  var b;
  b = 31;


  print("$b kadar BRONUZ VARDIR MORUQ.Sj");

}


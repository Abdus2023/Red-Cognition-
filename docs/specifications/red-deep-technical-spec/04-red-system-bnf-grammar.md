# IV. Red/System Language — BNF Grammar Core

```bnf
<program>     ::= <declaration>*

<declaration> ::= <func-decl>
                | <var-decl>
                | <struct-decl>
                | <import-decl>
                | <statement>

<func-decl>   ::= <word> ":" "func" "[" <spec> "]" "[" <body> "]"

<spec>        ::= <param>* [return: [<type>]]
<param>       ::= <word> "[" <type> "]"

<type>        ::= integer! | float! | float32! | byte! | logic!
                | pointer! "[" <type> "]"
                | struct! "[" <member>+ "]"
                | c-string!
                | <word>

<statement>   ::= <assignment>
                | <if-stmt>
                | <either-stmt>
                | <while-stmt>
                | <until-stmt>
                | <loop-stmt>
                | <func-call>
                | <return-stmt>
```
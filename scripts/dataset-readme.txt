Triple Selector Dataset
-----------------------

Columns/fields info:

0: sentence id
1: sentence text
2: triple subject (*)
3: triple predicate (*)
4: triple object (*)
5-(last-1): features (**)
last: label (0: invalid triple, 1: valid triple)

(*) : root/head token is enclosed in parenthesis
(**): current features are:
    * Universal POS tag code of subject head token
    * Universal dependency relation code of subject head token
    * Universal POS tag code of subject head token's head
    * Named entity code of subject head token
    * Number of direct children of subject head token
    * Distance (index delta) from subject head token to predicate head token
    * 0: subject head token is not a direct child of predicate head token, 1: subject head token is a direct child of predicate head token
    * Universal POS tag code of predicate head token
    * Universal dependency relation code of predicate head token
    * Universal POS tag code of predicate head token's head
    * Universal POS tag code of object head token
    * Universal dependency relation code of object head token
    * Universal POS tag code of object head token's head
    * Named entity code of object head token
    * Number of direct children of object head token
    * Distance (index delta) from predicate head token to object head token
    * 0: object head token is not a direct child of predicate head token, 1: object head token is a direct child of predicate head token

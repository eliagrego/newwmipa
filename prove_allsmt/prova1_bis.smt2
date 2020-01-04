(declare-fun x () Int)
(declare-fun y () Int)
(declare-fun z () Int)
(declare-fun w () Int)

(assert (or (> x 0) (> y 0) (> z 0) (> w 0)))

(check-allsat ((> x 0) (> y 0) (> z 0) (> w 0)))

(exit)

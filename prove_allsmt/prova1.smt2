(declare-fun x () Int)
(declare-fun y () Int)
(declare-fun z () Int)
(declare-fun w () Int)

(declare-fun a () Bool)
(declare-fun b () Bool)
(declare-fun c () Bool)
(declare-fun d () Bool)

(assert (= (> x 0) a))
(assert (= (> y 0) b))
(assert (= (> z 0) c))
(assert (= (> w 0) d))
(assert (or a b c d))

(check-allsat (a b c d))

(exit)

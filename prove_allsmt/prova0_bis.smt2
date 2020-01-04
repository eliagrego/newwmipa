(declare-fun x () Int)
(assert (> x 0) )
(check-allsat ( (> x 0) ))
(exit)

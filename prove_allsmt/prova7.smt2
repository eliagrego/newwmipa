(set-option :produce-models true)
(set-logic QF_LRA)

(declare-fun x () Real)
(declare-fun y () Real)

(declare-fun A1 () Bool)
(declare-fun A2 () Bool)
(declare-fun A3 () Bool)
(declare-fun A4 () Bool)

(assert (>= x 0))
(assert (<= x 1))

(assert (not (=

 (or
  (and A1 (= y x)) 
  (and
   (not A1)
   (or
    (and A2 (= y (* 2 x))) 
    (and
     (not A2)
     (or
      (and A3 (= y (* 3 x))) 
      (and (not A3) (= y (* 4 x)))
))))) 

 (= y
   (ite A1
     x
     (ite A2
       (* 2 x)
       (ite A3
          (* 3 x)
	  (* 4 x)
)) ) )

)))

(check-sat)
